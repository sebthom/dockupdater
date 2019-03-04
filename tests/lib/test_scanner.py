import time

import pytest

from docupdater.lib.update import Service, Container


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

    mocker.patch("docupdater.lib.update.Container.update")
    mocker.patch("docupdater.lib.update.Service.update")
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
