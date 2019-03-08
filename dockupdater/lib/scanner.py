from time import sleep

from .config import DISABLE_LABEL, ENABLE_LABEL
from .notifiers import TemplateMessage
from ..update.container import Container
from ..update.service import Service


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

        for container in self.client.containers.list(filters={'status': 'running'}, ignore_removed=True):
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

        if not self.config.disable_services_check:
            monitored.extend(self._scan_services())

        return monitored

    def check_swarm_mode(self):
        try:
            if not self.client.swarm or not self.client.swarm.attrs:
                self.logger.info("Your aren't running in swarm mode, skip services check.")
                self.config.disable_services_check = True
        except Exception as e:
            error_str = str(e).lower()
            if "this node is not a swarm manager" in error_str:
                if "worker nodes" in error_str:
                    raise EnvironmentError(
                        "Your running on a swarm worker, it isn't working. You must add placement constraints. "
                        "See docs at https://github.com/dockupdater/dockupdater for help."
                    )
                else:
                    self.logger.info("Your aren't running in swarm mode, skip services check.")
                    self.config.disable_services_check = True
            else:
                raise e

        if self.config.disable_containers_check and self.config.disable_services_check:
            raise AttributeError("Error you can't disable all monitoring (containers/services).")

    def update(self):
        monitored = self.scan_monitored()

        if not monitored:
            self.logger.info('No containers/services are running or monitored on %s', self.socket)
            return

        for container_or_service in monitored:
            self.logger.debug("checking object %s", container_or_service.name)

            if container_or_service.has_new_version():
                self.logger.info('%s will be updated', container_or_service.name)
                container_or_service.update()
                self.logger.debug('%s is updated', container_or_service.name)
                self.notification_manager.send(
                    TemplateMessage(container_or_service),
                    container_or_service.config.notifiers
                )
                if container_or_service.config.wait:
                    self.logger.info('Waiting %s before next update', container_or_service.config.wait)
                    sleep(container_or_service.config.wait)
            else:
                self.logger.debug("no new version for %s", container_or_service.name)

    def self_update(self):
        if not self.config.disable_containers_check:
            # Removing old dockupdater
            self.logger.debug('Looking for old dockupdater on %s', self.socket)
            for container in self.client.containers.list(all=True, ignore_removed=True):
                if container.name.endswith("_old_dockupdater"):
                    self.logger.debug('Stopping and deleting %s', container.name)
                    container.stop()
                    container.remove()
            # Fix dockupdater if they need exposed port
            for container in self.client.containers.list(all=True, ignore_removed=True):
                if container.labels.get("dockupdater.updater_port"):
                    self.logger.info('Recreate dockupdater container with exposed ports')
                    Container(self.docker, container)
                    container.update()
