from time import sleep

from docker.errors import APIError

from .config import DISABLE_LABEL, ENABLE_LABEL
from .notifiers import TemplateMessage
from .update import Container, Service


class Scanner(object):
    def __init__(self, docker_client):
        self.docker = docker_client
        self.logger = self.docker.logger
        self.config = self.docker.config
        self.client = self.docker.client
        self.socket = self.docker.socket
        self.notification_manager = self.docker.notification_manager

    def _scan_containers(self):
        """Return filtered container objects list"""
        monitored_containers = []

        for container in self.client.containers.list(filters={'status': 'running'}):
            enable_label = container.labels.get(ENABLE_LABEL, False)
            disable_label = container.labels.get(DISABLE_LABEL, False)
            swarm = container.labels.get('com.docker.stack.namespace', False)
            if (not self.config.label or enable_label) and not disable_label and not swarm:
                monitored_containers.append(Container(self.docker, container))
            else:
                self.logger.debug("skip monitoring for %s", container.name)

        self.logger.info("total containers monitored: %s", len(monitored_containers))

        return monitored_containers

    def _scan_services(self):
        """Return filtered service objects list"""
        monitored_services = []

        for service in self.client.services.list():
            enable_label = service.attrs['Spec']['Labels'].get(ENABLE_LABEL, False)
            disable_label = service.attrs['Spec']['Labels'].get(DISABLE_LABEL, False)
            if (not self.config.label or enable_label) and not disable_label:
                monitored_services.append(Service(self.docker, service))

        self.logger.info("total services monitored: %s", len(monitored_services))

        return monitored_services

    def scan_monitored(self):
        """Return all object update if there are a new version"""
        monitored = []

        if not self.config.disable_containers_check:
            monitored.extend(self._scan_containers())

        try:
            if not self.config.disable_services_check:
                monitored.extend(self._scan_services())
        except APIError as e:
            if "This node is not a swarm manager" in str(e):
                self.logger.debug("Your are not running in swarm mode, skip services")
            raise e

        return monitored

    def update(self):
        monitoreds = self.scan_monitored()

        if not monitoreds:
            self.logger.info('No containers/services are running or monitored on %s', self.socket)
            return

        for container_or_service in monitoreds:
            self.logger.debug("checking object %s", container_or_service.name)

            if container_or_service.has_new_version():
                self.logger.info('%s will be updated', container_or_service.name)
                container_or_service.update()
                self.logger.debug('%s is updated', container_or_service.name)
                self.notification_manager.send(
                    TemplateMessage(container_or_service), container_or_service.config.notifiers)
                if container_or_service.config.wait:
                    sleep(container_or_service.config.wait)
            else:
                self.logger.debug("no new version for %s", container_or_service.name)
