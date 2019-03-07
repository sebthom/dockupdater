import pytest
from docker.errors import APIError


@pytest.mark.docker
@pytest.mark.slow
def test_container(container):
    container.load_new_config()
    assert container.name == "ContainerUpdateTest1"
    assert container.get_image_name() == "busybox"
    assert container.get_tag() == "latest"
    assert container.labels.get("test") == "9876"
    assert container.stack_name is None
    container.stop()
    container.start()
    with pytest.raises(APIError):
        container.remove()
    container.stop()
    container.remove()


@pytest.mark.docker
def test_container_has_new_version(monkeypatch, container, hello_world_image):
    monkeypatch.setattr("docker.models.images.ImageCollection.pull", lambda *args, **kwargs: hello_world_image)

    assert container.has_new_version() is True
    assert container.name == "ContainerUpdateTest1"
    assert container.get_image_name() == "busybox"
    assert container.get_tag() == "latest"
    assert container.get_current_id() != container.get_latest_id()


@pytest.mark.docker
@pytest.mark.slow
def test_container_update(monkeypatch, mocker, container, hello_world_image):
    monkeypatch.setattr("docker.models.images.ImageCollection.pull", lambda *args, **kwargs: hello_world_image)
    mocker.patch("docupdater.update.container.Container.recreate")
    container.update()
