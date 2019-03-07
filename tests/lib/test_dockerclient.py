import pytest


@pytest.mark.docker
@pytest.mark.slow
def test_scanner_check_swarm_mode(docker_client):
    assert docker_client.config.disable_services_check is False

    if not docker_client.client.swarm.attrs:
        docker_client.client.swarm.init(force_new_cluster=True)

    docker_client.check_swarm_mode()
    assert docker_client.config.disable_services_check is False

    docker_client.client.swarm.leave(force=True)

    docker_client.check_swarm_mode()
    assert docker_client.config.disable_services_check is True

    docker_client.config.disable_containers_check = True

    with pytest.raises(AttributeError):
        docker_client.check_swarm_mode()
