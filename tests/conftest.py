import pytest
from docker.client import DockerClient

from dockupdater.lib.config import Config
from dockupdater.lib.config import DefaultConfig
from dockupdater.lib.dockerclient import Docker
from dockupdater.lib.notifiers import NotificationManager
from dockupdater.lib.scanner import Scanner
from dockupdater.update.container import Container
from dockupdater.update.service import Service

# Global variables for caching fixture
HELLO_WORLD_IMAGE = None
HELLO_WORLD_CONTAINER = None


@pytest.fixture()
def config():
    return Config(**{key: value for key, value in DefaultConfig.__dict__.items() if "__" not in key})


@pytest.fixture()
def notification(config):
    return NotificationManager(config)


@pytest.fixture()
def docker_client(config, notification):
    return Docker("unix://var/run/docker.sock", config, notification)


@pytest.fixture()
def scanner(docker_client):
    return Scanner(docker_client)


@pytest.fixture()
def service(docker_client):
    if not docker_client.client.swarm.attrs:
        docker_client.client.swarm.init(force_new_cluster=True)
    while True:
        try:
            service = docker_client.client.services.create(
                "busybox:latest",
                tty=True,
                name="TestServiceUpdate1",
                labels={
                    "test": "1234",
                },
                container_labels={
                    "dockupdater.disable": "true",
                },
            )
            break
        except:
            service = docker_client.client.services.get("TestServiceUpdate1")
            service.remove()
    return Service(docker_client, service)


@pytest.fixture()
def container(docker_client):
    try:
        container = docker_client.client.containers.run(
            "busybox:latest",
            tty=True,
            detach=True,
            name="ContainerUpdateTest1",
            labels={
                "test": "9876",
            },
        )
    except:
        container = docker_client.client.containers.get("ContainerUpdateTest1")
    return Container(docker_client, container)


@pytest.fixture()
def hello_world_image():
    global HELLO_WORLD_IMAGE
    if not HELLO_WORLD_IMAGE:
        client = DockerClient.from_env()
        HELLO_WORLD_IMAGE = client.images.pull("hello-world:latest")
    return HELLO_WORLD_IMAGE


@pytest.fixture()
def hello_world_container(hello_world_image):
    global HELLO_WORLD_CONTAINER
    if not HELLO_WORLD_CONTAINER:
        client = DockerClient.from_env()
        HELLO_WORLD_CONTAINER = client.containers.create(
            hello_world_image,
            labels={"test": "12345"},
            hostname="hello-world-test",
            environment={
                "env1": "test1",
                "env2": "test2",
                "env3": "test3",
            },
        )
    return HELLO_WORLD_CONTAINER


@pytest.fixture()
def hello_world_container_with_port():
    global HELLO_WORLD_CONTAINER_WITH_PORT
    if not HELLO_WORLD_CONTAINER_WITH_PORT:
        client = DockerClient.from_env()
        container = client.api.create_container(
            "hello-world:latest",
            labels={"test": "12345"},
            hostname="hello-world-test",
            environment={
                "env1": "test1",
                "env2": "test2",
                "env3": "test3",
            },
            ports=[(4567, "tcp"), (9876, "tcp")],
        )
        HELLO_WORLD_CONTAINER_WITH_PORT = client.containers.get(container.get("Id"))
    return HELLO_WORLD_CONTAINER_WITH_PORT
