import pytest


@pytest.mark.docker
def test_update_service_has_new_version(monkeypatch, service, hello_world_image):
    monkeypatch.setattr("docker.models.images.ImageCollection.pull", lambda *args, **kwargs: hello_world_image)

    assert service.has_new_version() is True
    assert service.name == "TestServiceUpdate1"
    assert service.get_image_name() == "busybox"
    assert service.get_tag() == "latest"
    assert service.get_current_id() != service.get_latest_id()


@pytest.mark.docker
def test_update_service_update(monkeypatch, service, hello_world_image, mocker):
    monkeypatch.setattr("docker.models.images.ImageCollection.pull", lambda *args, **kwargs: hello_world_image)
    mocker.patch("docker.models.services.Service.update")

    service.update()


@pytest.mark.docker
def test_update_container_has_new_version(monkeypatch, container, hello_world_image):
    monkeypatch.setattr("docker.models.images.ImageCollection.pull", lambda *args, **kwargs: hello_world_image)

    assert container.has_new_version() is True
    assert container.name == "ContainerUpdateTest1"
    assert container.get_image_name() == "busybox"
    assert container.get_tag() == "latest"
    assert container.get_current_id() != container.get_latest_id()


@pytest.mark.docker
@pytest.mark.slow
def test_update_container_update(monkeypatch, mocker, container, hello_world_image):
    monkeypatch.setattr("docker.models.images.ImageCollection.pull", lambda *args, **kwargs: hello_world_image)
    mocker.patch("docupdater.lib.update.Container.recreate")
    container.update()
