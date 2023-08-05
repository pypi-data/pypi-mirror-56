import boto3
import docker
from docker.errors import APIError
import click


class Swarm:
    def __init__(self, ec2_client: boto3.client, docker_client: docker.APIClient):
        self.docker_client = docker_client
        self.ec2_client = ec2_client
        self.manager_nodes = []
        self.manager_instances = []
        self.nodes = []

    @staticmethod
    def running_managers(nodes):
        """Formatting the list correctly to be processed"""

        for node in nodes:
            node["managers"] = node["swarm_info"].get("Managers", 0)

        running_nodes = [
            node for node in nodes if node["swarm_info"]["LocalNodeState"] == "active"
        ]

        return sorted(running_nodes, key=lambda k: k["managers"], reverse=True)

    @staticmethod
    def format_instance_response(nodes):
        """EC2 client returns a deeply nested payload when requesting instances.
        This static helper function processes the payload and returns a list."""

        reservations = nodes["Reservations"]
        instances_list = []
        for ins in reservations:
            for obj in ins["Instances"]:
                instances_list.append(obj)
        return instances_list

    def get_ec2_manager_nodes(self):
        """Return EC2 Nodes that are tagged with Name:SwarmManager"""

        filters = [
            # {"Name": "tag:swarm-manager", "Values": ["true",]},
            {"Name": "tag:Name", "Values": ["SwarmManager",]},
            {"Name": "instance-state-name", "Values": ["running",]},
        ]
        response = self.ec2_client.describe_instances(Filters=filters)
        manager_instances = self.format_instance_response(response)

        self.manager_instances = sorted(
            manager_instances, key=lambda k: k["LaunchTime"]
        )
        self.manager_nodes.clear()

        for manager in self.manager_instances:
            addr = manager["PrivateIpAddress"]
            remote_client = docker.DockerClient(base_url=f"{addr}:2376")

            try:
                remote_node_info = remote_client.info()
                swarm_info = {
                    "PrivateIpAddress": addr,
                    "swarm_info": remote_node_info["Swarm"],
                }
                self.manager_nodes.append(swarm_info)
            except APIError:
                print("Remote Node Not Connected")

        return self.manager_nodes

    def get_max_quorum(self):

        manager_nodes = self.get_ec2_manager_nodes()
        running_nodes = self.running_managers(manager_nodes)
        manager_count = [x["managers"] for x in running_nodes]

        # return all(x == manager_count[0] for x in manager_count)
        return max(manager_count)

    def bootstrap_node(self, node):
        """Query the metastore for a list of manager nodes and join the largest swarm
        available."""

        if len(self.get_ec2_manager_nodes()) > 0:
            self.join_swarm(node)
        else:
            self.bootstrap_cluster(node)

    def join_swarm(self, node):
        """Query the metastore for a list of manager nodes and join the largest swarm
        available."""

        manager_nodes = self.get_ec2_manager_nodes()
        running_nodes = self.running_managers(manager_nodes)

        for manager in running_nodes:
            addr = manager["PrivateIpAddress"]

            remote_client = docker.DockerClient(base_url=f"{addr}:2376")

            try:
                remote_client.swarm.reload()  # get swarm details from server

                tokens = remote_client.swarm.attrs["JoinTokens"]

                if node.role == "manager":
                    node.join_swarm(addr, tokens["Manager"])
                elif node.role == "worker":
                    node.join_swarm(addr, tokens["Worker"])
                else:
                    pass

                node.add_ec2_tag("swarm-hostname", node.hostname)
                node.add_ec2_tag("swarm-bootstrap", "true")
                click.echo(f"Joined an existing Swarm at {addr}")

            except APIError as e:
                if e.status_code == 503:
                    click.echo("Node attempted to join is not part of a swarm")
                else:
                    click.echo("Error attempting to join a swarm cluster: ", e.__dict__)

                continue
            break
        else:
            # not able to join any of the manager nodes, init self
            self.bootstrap_cluster(node)

    def bootstrap_cluster(self, initial_node):

        initial_node.add_ec2_tag("bootstrap", "true")
        spec = initial_node.docker_client.create_swarm_spec()

        try:
            # creating overlay networks on aws all VPCs are restricted to
            # 10.0.0.0/16, so we use the next block for containers
            initial_node.node_id = initial_node.docker_client.init_swarm(
                advertise_addr=f"{initial_node.local_ip}:2377",
                swarm_spec=spec,
                default_addr_pool=["10.1.0.0/16"],
            )
            initial_node.refresh()

        except APIError as e:
            click.echo(e)
            click.echo("Already in a docker swarm.")

        initial_node.add_docker_label("bootstrap", "true")

        initial_node.add_ec2_tag("swarm-hostname", initial_node.hostname)
        initial_node.add_ec2_tag("swarm-bootstrap", "true")

    def prune_nodes(self, node_filter=None):
        """Cleanup dead nodes from the Docker Swarm cluster. Can specify manager
        or worker nodes."""

        filters = [
            {
                "Name": "instance-state-name",
                "Values": ["shutting-down", "stopped", "terminated", "stopping",],
            },
        ]

        if node_filter == "manager":
            filters.append({"Name": "tag:Name", "Values": ["SwarmManager"]})
        elif node_filter == "worker":
            filters.append({"Name": "tag:Name", "Values": ["SwarmWorker"]})

        response = self.ec2_client.describe_instances(Filters=filters)
        dead_nodes = self.format_instance_response(response)

        for instance in dead_nodes:
            for tag in instance["Tags"]:
                if tag["Key"] == "swarm-hostname":
                    self.docker_client.remove_node(tag["Value"])

    def cleanup(self):
        """Cleanup and prune all swarm nodes and run system maintenance on hosts."""

        # for node in self.nodes:
        #     node.cleanup()

        self.prune_nodes(node_filter="managers")
        self.prune_nodes(node_filter="workers")

    def update_labels(self):

        filters = [
            {"Name": "tag:swarm-cluster", "Values": ["true"]},
            {"Name": "instance-state-name", "Values": ["running",]},
        ]

        swarm_members = self.ec2_client.describe_instances(Filters=filters)

        for member_instance in swarm_members["Reservations"]:

            # instances are grouped into lists of one element (..?)
            ec2_tags = member_instance["Instances"][0]["Tags"]
            labels = {}
            hostname = ""

            # update nodes that have both a swarm-hostname and docker-labals tag
            for tag in ec2_tags:
                if tag["Key"] == "swarm-hostname":
                    hostname = tag["Value"]

                if tag["Key"] == "docker-labels":
                    for pair in tag["Value"].split(","):
                        key, val = pair.split("=")
                        labels = {**labels, **{key: val}}

                if tag["Key"] == "availability-zone":
                    labels = {**labels, **{"availability-zone": tag["Value"]}}

            # if there is no hostname, the node wasn't an initialized swarm node
            if hostname:

                filters = {"name": hostname}
                nodes = self.docker_client.nodes(filters=filters)

                for node in nodes:

                    node_id = node["ID"]
                    spec_version = node["Version"]["Index"]
                    node_spec = node["Spec"]

                    # add the labels from the ec2 tags to the docker node
                    node_spec["Labels"] = {**node_spec["Labels"], **labels}

                    labels = node_spec["Labels"]
                    val = self.docker_client.update_node(
                        node_id=node_id, version=spec_version, node_spec=node_spec,
                    )

                    click.echo(f"{val}- label {hostname} ({node_id}) with {labels}")
