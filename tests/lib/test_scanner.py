import time

import pytest

from docupdater.update.container import Container
from docupdater.update.service import Service


def prepare_containers(scanner):
    if not scanner.client.swarm.attrs:
        scanner.client.swarm.init(force_new_cluster=True)

    try:
        scanner.client.services.create(
            "busybox:latest",
            name="TestService1",
            labels={
                "docupdater.wait": "1"
            }
        )
        scanner.client.services.create("busybox", name="TestService2")

        scanner.client.containers.run("busybox", tty=True, detach=True, name="Test1")
        scanner.client.containers.run(
            "busybox",
            tty=True,
            detach=True,
            name="Test2",
            labels={"docupdater.disable": "true"}
        )
        scanner.client.containers.run(
            "busybox",
            tty=True,
            detach=True,
            name="Test3",
            labels={"docupdater.enable": "false"}
        )
    except:
        print("Tests containers already exist")


@pytest.mark.docker
@pytest.mark.slow
def test_scanner_get_containers(scanner):
    prepare_containers(scanner)

    containers = scanner.get_containers("Test[1-2]")
    assert len(containers) == 2
    containers = scanner.get_containers("Nomatch")
    assert len(containers) == 0


@pytest.mark.docker
@pytest.mark.slow
def test_scanner_get_services(scanner):
    prepare_containers(scanner)

    services = scanner.get_services("TestService[2-3]")
    assert len(services) == 1
    services = scanner.get_services("Nomatch")
    assert len(services) == 0


@pytest.mark.docker
def test_scanner_scan_monitored(scanner):
    prepare_containers(scanner)

    monitored = scanner.scan_monitored()

    assert len([object.name for object in monitored if object.name in ["Test1", "Test3"]]) == 2
    assert len([object.name for object in monitored if object.name in ["Test2"]]) == 0
    assert len([object.name for object in monitored if object.name in ["TestService1", "TestService2"]]) == 2

    scanner.config.label = True
    monitored = scanner.scan_monitored()
    assert len([object.name for object in monitored if object.name in ["Test3"]]) == 1
    assert len([object.name for object in monitored if object.name in ["Test1", "Test2"]]) == 0
    assert len([object.name for object in monitored if object.name in ["TestService1", "TestService2"]]) == 0


@pytest.mark.docker
@pytest.mark.slow
def test_scanner_update(scanner, mocker, monkeypatch):
    prepare_containers(scanner)

    mocker.patch("docupdater.update.container.Container.update")
    mocker.patch("docupdater.update.service.Service.update")
    monkeypatch.setattr(time, 'sleep', lambda s: None)

    scanner.update()
    Service.update.assert_any_call()
    Container.update.assert_not_called()


@pytest.mark.docker
@pytest.mark.slow
def test_scanner_check_swarm_mode(scanner):
    assert scanner.config.disable_services_check is False

    if not scanner.client.swarm.attrs:
        scanner.client.swarm.init(force_new_cluster=True)

    scanner.check_swarm_mode()
    assert scanner.config.disable_services_check is False

    scanner.client.swarm.leave(force=True)

    scanner.check_swarm_mode()
    assert scanner.config.disable_services_check is True

    scanner.config.disable_containers_check = True

    with pytest.raises(AttributeError):
        scanner.check_swarm_mode()
