import pytest
from docker.client import DockerClient

# Global variables for caching fixture
HELLO_WORLD_IMAGE = None
HELLO_WORLD_CONTAINER = None


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
                "env3": "test3"
            }
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
                "env3": "test3"
            },
            ports=[(4567, "tcp"), (9876, "tcp")]
        )
        HELLO_WORLD_CONTAINER_WITH_PORT = client.containers.get(container.get("Id"))
    return HELLO_WORLD_CONTAINER_WITH_PORT
