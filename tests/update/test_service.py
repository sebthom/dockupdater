import pytest


@pytest.mark.docker
def test_service(service):
    service.load_new_config()
    assert service.get_image_name() == "busybox"
    assert service.get_tag() == "latest"
    assert service.labels.get("test") == "1234"
    assert service.stack_name is None
    assert service.is_replicated()
    service.stop()
    assert service.labels.get("docupdater._replicas") == "1"
    assert service.is_replicated().get("Replicas") == 0
    service.start()
    assert service.is_replicated().get("Replicas") == 1


@pytest.mark.docker
def test_service_has_new_version(monkeypatch, service, hello_world_image):
    monkeypatch.setattr("docker.models.images.ImageCollection.pull", lambda *args, **kwargs: hello_world_image)

    assert service.has_new_version() is True
    assert service.name == "TestServiceUpdate1"
    assert service.get_image_name() == "busybox"
    assert service.get_tag() == "latest"
    assert service.get_current_id() != service.get_latest_id()


@pytest.mark.docker
def test_service_update(monkeypatch, service, hello_world_image, mocker):
    monkeypatch.setattr("docker.models.images.ImageCollection.pull", lambda *args, **kwargs: hello_world_image)
    mocker.patch("docker.models.services.Service.update")

    service.update()
