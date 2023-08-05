import socket

import click
import requests
from swarm_controller.node import SwarmNode

az = requests.get(
    "http://169.254.169.254/latest/meta-data/placement/availability-zone"
).text

instance_id = requests.get("http://169.254.169.254/latest/meta-data/instance-id").text


@click.group()
@click.option("--debug", default=False, help="Control the verbosity of output.")
@click.option(
    "--docker-host",
    default="unix://var/run/docker.sock",
    help="The docker host for the current node",
)
@click.pass_context
def swarm_ctl(ctx, debug, docker_host):
    """A simple command line helper for automated Docker Swarm cluster
    maintenance tasks."""

    ctx.ensure_object(dict)

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    swarm_node = SwarmNode(docker_host, az, hostname, local_ip, instance_id)

    ctx.obj["DEBUG"] = debug
    ctx.obj["SwarmNode"] = swarm_node


@swarm_ctl.command("bootstrap", short_help="Bootstrap a Swarm Node")
@click.pass_context
def bootstrap(ctx):
    """Query the metastore for Docker Swarm Manager Nodes
    and attempt to join the cluster or initialize if first node"""

    swarm_node = ctx.obj["SwarmNode"]
    swarm_node.bootstrap()


@swarm_ctl.command("cleanup", short_help="Cleanup a Swarm Cluster")
@click.pass_context
def cleanup(ctx):
    """Prune dead nodes from the swarm."""

    swarm_node = ctx.obj["SwarmNode"]
    swarm_node.cleanup()


@swarm_ctl.command("relabel", short_help="Relabel nodes on a Swarm Cluster")
@click.pass_context
def relabel(ctx):
    """Query the metastore for node labels and add them to the docker engine"""

    swarm_node = ctx.obj["SwarmNode"]

    if swarm_node.role == "manager":
        swarm_node.swarm.update_labels()
    else:
        click.echo("Worker Node - skipped docker labeling.")
