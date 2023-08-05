import boto3
import click
import time
import docker
from docker.errors import APIError


from swarm_controller.swarm import Swarm


class SwarmNode:
    def __init__(self, docker_host, availability_zone, hostname, local_ip, instance_id):
        self.hostname = hostname
        self.local_ip = local_ip
        self.spec_version = 0
        self.instance_id = instance_id
        self.availability_zone = availability_zone
        self.region_name = self.availability_zone[:-1]

        self.docker_host = docker_host
        self.docker_client = docker.APIClient(base_url=docker_host, version="auto")
        self.docker_info = {}

        self.ec2_client = boto3.client("ec2", region_name=self.region_name)
        self.ec2_resource = boto3.resource("ec2", region_name=self.region_name)
        self.instance = self.ec2_resource.Instance(  # pylint: disable=E1101
            self.instance_id
        )

        for tag in self.instance.tags:
            if tag["Key"] == "Name":
                self.label = tag["Value"]

        # if the node is named SwarmManager it's a manger, otherwise a worker
        if self.label == "SwarmManager":
            self.role = "manager"
        else:
            self.role = "worker"

        self.swarm = Swarm(self.ec2_client, self.docker_client)
        self.node_id = ""
        self.node_info = {}
        self.node_labels = {"az": self.availability_zone}

        self.node_spec = {
            "Availability": "active",
            "Name": self.hostname,
            "Role": self.role,
            "Labels": self.node_labels,
        }

        self.refresh()

        self.add_ec2_tag("availability-zone", self.availability_zone)

    def refresh(self):
        self.docker_info = self.docker_client.info()
        self.node_id = self.docker_info["Swarm"]["NodeID"]

    def refresh_node_spec(self):
        self.node_info = self.docker_client.inspect_node(self.node_id)
        # self.node_spec = self.node_info["Spec"]
        self.spec_version = self.node_info["Version"]["Index"]

    def update_node_spec(self):
        try:
            self.docker_client.update_node(
                node_id=self.node_id,
                version=self.spec_version,
                node_spec=self.node_spec,
            )

        except APIError as e:
            if e.status_code == 503:
                click.echo("Attempted to use a swarm command - NOT a swarm manager.")
                pass
            else:
                click.echo(e)

    def join_swarm(self, addr, token):
        click.echo(f"Attempting to join {addr} with {token}")
        self.docker_client.join_swarm([addr + ":2377"], token)

    def demote(self):
        self.refresh()
        self.refresh_node_spec()
        self.node_spec["Role"] = "worker"
        self.update_node_spec()

    def promote(self):
        self.refresh()
        self.refresh_node_spec()
        self.node_spec["Role"] = "manager"
        self.update_node_spec()

    def drain(self):
        self.refresh()
        self.refresh_node_spec()
        self.node_spec["Availability"] = "Drain"
        self.update_node_spec()

    def add_docker_label(self, key, value=""):
        self.refresh()
        self.refresh_node_spec()
        self.node_spec["Labels"] = {**self.node_spec["Labels"], **{key: value}}

        self.update_node_spec()

    def add_ec2_tag(self, key, value):
        tags = [{"Key": key, "Value": value}]
        response_tags = self.ec2_client.create_tags(
            Resources=[self.instance_id], Tags=tags
        )
        if response_tags["ResponseMetadata"]["HTTPStatusCode"] == 200:
            click.echo(f"Added EC2 tag: {key}={value} to {self.instance_id}")
        else:
            click.echo("ERROR ", response_tags)

    def bootstrap(self):
        self.refresh()

        if self.docker_info["Swarm"]["LocalNodeState"] == "active":
            click.echo("Swarm mode is already active.")
            return

        if self.role == "manager":
            self.swarm.bootstrap_node(self)
        else:
            self.swarm.join_swarm(self)

        self.refresh_node_spec()
        self.update_node_spec()
        self.check_split_brain()
        click.echo("Bootstrap finished.")

    def check_split_brain(self):

        # delay for 15 seconds (in case nodes launched simulatenously)
        # check if there is a split-brain
        time.sleep(15)

        self.refresh()

        managers = self.docker_info["Swarm"].get("Managers", 0)

        if managers and self.swarm.get_max_quorum() > managers:
            self.drain()
            self.demote()
            self.docker_client.leave_swarm()

            # retry
            self.bootstrap()

    def cleanup(self):
        self.docker_client.prune_containers()
        self.docker_client.prune_images()
        self.docker_client.prune_builds()
        self.docker_client.prune_networks()
        self.docker_client.prune_volumes()
        click.echo("Cleanup finished.")
