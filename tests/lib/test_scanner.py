import time

import pytest

from dockupdater.lib.config import OptionRegex
from dockupdater.update.container import Container
from dockupdater.update.service import Service


def prepare_containers(scanner):
    print("creating containers and services")

    if not scanner.client.swarm.attrs:
        scanner.client.swarm.init(force_new_cluster=True)

    try:
        scanner.client.services.create(
            "busybox:latest",
            name="TestService1",
            tty=True,
            labels={
                "dockupdater.wait": "1",
            },
            container_labels={
                "dockupdater.disable": "true",
            },
        )
        scanner.client.services.create(
            "busybox",
            tty=True,
            name="TestService2",
            container_labels={
                "dockupdater.disable": "true",
            },
        )

        scanner.client.containers.run(
            "busybox",
            tty=True,
            detach=True,
            name="Test1",
        )
        scanner.client.containers.run(
            "busybox",
            tty=True,
            detach=True,
            name="Test2",
            labels={
                "dockupdater.disable": "true",
                "dockupdater.stops": "Test1",
                "dockupdater.starts": "Test1",
            },
        )
        scanner.client.containers.run(
            "busybox",
            tty=True,
            detach=True,
            name="Test3",
            labels={
                "dockupdater.enable": "false",
            },
        )
        scanner.client.containers.run(
            "busybox",
            tty=True,
            detach=True,
            name="Test4",
            labels={
                "dockupdater.enable": "true",
            },
        )
    except:
        print("Tests containers already exist")
    print("Done")


@pytest.mark.docker
def test_scanner_get_containers(scanner):
    prepare_containers(scanner)

    containers = scanner.get_containers(OptionRegex("Test[1-2]"))
    assert len(containers) == 2
    containers = scanner.get_containers(OptionRegex("Nomatch"))
    assert len(containers) == 0


@pytest.mark.docker
def test_scanner_get_services(scanner):
    prepare_containers(scanner)

    services = scanner.get_services(OptionRegex("TestService[2-3]"))
    assert len(services) == 1
    services = scanner.get_services(OptionRegex("Nomatch"))
    assert len(services) == 0


@pytest.mark.docker
def test_scanner_starts_stops_before_update(docker_client, scanner):
    prepare_containers(scanner)
    container = Container(docker_client, scanner.get_containers(OptionRegex("Test2"))[0])

    container.load_new_config()

    assert container.name == "Test2"
    assert container.config.stops[0].regex == "Test1"
    assert container.config.starts[0].regex == "Test1"

    assert docker_client, scanner.get_containers(OptionRegex("Test1"))[0].status == "running"

    scanner.stops_before_update(container)
    assert docker_client, scanner.get_containers(OptionRegex("Test1"))[0].status != "running"

    scanner.starts_after_update(container)
    assert docker_client, scanner.get_containers(OptionRegex("Test1"))[0].status == "running"


@pytest.mark.docker
def test_scanner_scan_monitored(scanner):
    prepare_containers(scanner)

    monitored = scanner.scan_monitored()

    assert len([object.name for object in monitored if object.name in ["Test1", "Test3", "Test4"]]) == 3
    assert len([object.name for object in monitored if object.name in ["Test2"]]) == 0
    assert len([object.name for object in monitored if object.name in ["TestService1", "TestService2"]]) == 2

    scanner.config.label = True
    monitored = scanner.scan_monitored()
    assert len([object.name for object in monitored if object.name in ["Test4"]]) == 1
    assert len([object.name for object in monitored if object.name in ["Test1", "Test2", "Test3"]]) == 0
    assert len([object.name for object in monitored if object.name in ["TestService1", "TestService2"]]) == 0


@pytest.mark.docker
@pytest.mark.slow
def test_scanner_update(scanner, mocker, monkeypatch):
    prepare_containers(scanner)

    mocker.patch("dockupdater.update.container.Container.update")
    mocker.patch("dockupdater.update.service.Service.update")
    monkeypatch.setattr(time, 'sleep', lambda s: None)

    scanner.update()
    Service.update.assert_any_call()
    Container.update.assert_not_called()
