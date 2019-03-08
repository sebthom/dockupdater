import pytest
from docker.client import DockerClient

from dockupdater.helpers.helpers import set_properties, remove_sha_prefix, convert_to_boolean, get_id_from_image


@pytest.mark.docker
def test_set_properties(hello_world_container, hello_world_image):
    new = set_properties(hello_world_container, hello_world_image)
    assert new.get("labels", dict()).get("test") == "12345"
    assert len(new.get("labels", dict()).keys()) == 1
    assert new.get("name") == hello_world_container.name
    assert new.get("name") == hello_world_container.name
    assert new.get("hostname") == "hello-world-test"
    assert all([env for env in new.get("environment") if env == "env1=test1"])


@pytest.mark.docker
def test_set_properties_with_self_update(hello_world_image):
    client = DockerClient.from_env()

    container_dict = dict(
        labels={"test": "12345"},
        hostname="hello-world-test",
        environment={
            "env1": "test1",
            "env2": "test2",
            "env3": "test3"
        },
        ports=[(4567, "tcp"), (9876, "tcp")]
    )
    container = client.api.create_container("hello-world:latest", **container_dict)

    new = set_properties(client.containers.get(container.get("Id")), hello_world_image, self_update=True)
    assert new.get("labels", dict()).get("test") == "12345"
    assert new.get("labels", dict()).get("dockupdater.updater_port") == "4567,tcp:9876,tcp"
    assert not new.get("ports")

    container_dict["labels"] = new.get("labels")
    del container_dict["ports"]
    container2 = client.api.create_container("hello-world:latest", **container_dict)
    new2 = set_properties(client.containers.get(container2.get("Id")), hello_world_image, self_update=True)
    assert new2.get("labels").get("test") == "12345"
    assert new2.get("labels").get("dockupdater.updater_port") is None
    assert all([(a, b) for a, b in new2.get("ports") if a in [4567, 9876]])


def test_remove_sha():
    assert remove_sha_prefix("sha256:test123") == "test123", "Remove sha with value sha256:test123 failed"
    assert remove_sha_prefix("test123") == "test123", "Remove sha with value test123 failed"
    assert remove_sha_prefix("test123:sah256") == "test123:sah256", "Remove sha with test123:sah256 failed"


def test_convert_to_boolean():
    assert convert_to_boolean("Y"), "Convert to bool with value Y failed"
    assert convert_to_boolean("Yes"), "Convert to bool with value Yes failed"
    assert not convert_to_boolean("no"), "Convert to bool with value no failed"
    assert not convert_to_boolean("blabla"), "Convert to bool with value balbla failed"


def test_get_id_from_image(hello_world_image):
    assert get_id_from_image(hello_world_image)
