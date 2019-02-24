from datetime import datetime, timezone, timedelta
from time import sleep

import click
from apscheduler.schedulers.background import BackgroundScheduler
from requests.exceptions import ConnectionError

from . import VERSION, BRANCH
from .lib.config import DefaultConfig, Config
from .lib.dockerclient import Docker
from .lib.logger import DocupdaterLogger
from .lib.notifiers import NotificationManager, StartupMessage
from .lib.scanner import Scanner


@click.command()
@click.version_option(version=VERSION)
@click.option("-d", "--docker-sockets", "docker_sockets",
              default=DefaultConfig.docker_sockets, show_default=True, multiple=True,
              help='Socket for docker management. EXAMPLE: -d unix://var/run/docker.sock')
@click.option("-t", "--docker-tls", "docker_tls",
              is_flag=True, default=DefaultConfig.docker_tls, show_default=True,
              help='Enable docker TLS. REQUIRES: docker cert mount')
@click.option("-T", "--docker-tls-verify", "docker_tls_verify",
              is_flag=True, default=DefaultConfig.docker_tls_verify, show_default=True,
              help='Verify the CA Certificate mounted for TLS')
@click.option("-i", "--interval", "interval",
              type=int, default=DefaultConfig.interval, show_default=True,
              help='Interval in seconds between checking for updates')
@click.option("-C", "--cron", "cron",
              default=DefaultConfig.cron,
              help='Cron formatted string for scheduling. EXAMPLE: "*/5 * * * *"')
@click.option("-l", "--log-level", "log_level",
              type=click.Choice(['debug', 'info', 'warn', 'error', 'critical']), default=DefaultConfig.log_level,
              show_default=True, help='Set logging level')
@click.option("-L", "--latest", "latest",
              default=DefaultConfig.latest, show_default=True, is_flag=True,
              help='Pull the :latest tags and update all containers to it.')
@click.option("-o", "--run-once", "run_once",
              is_flag=True, default=DefaultConfig.run_once, show_default=True,
              help='Single run')
@click.option("-N", "--notifiers", "notifiers",
              default=DefaultConfig.notifiers, multiple=True,
              help='Apprise formatted notifiers\n'
                   'EXAMPLE: -N discord://1234123412341234/jasdfasdfasdfasddfasdf '
                   'mailto://user:pass@gmail.com')
@click.option("--skip-start-notif", "skip_start_notif",
              default=DefaultConfig.skip_start_notif, is_flag=True, show_default=True,
              help='Skip notification of docupdater has started')
@click.option("--template-file", "template_file",
              default=DefaultConfig.template_file, type=click.Path(),
              help='Use a custom template for notification')
@click.option("-k", "--label", "label",
              default=DefaultConfig.label, is_flag=True, show_default=True,
              help='Enable label monitoring for docupdater instead of monitoring all containers/services')
@click.option("-c", "--cleanup", "cleanup",
              default=DefaultConfig.cleanup, is_flag=True, show_default=True,
              help='Remove old images after updating')
@click.option("-r", "--repo-user", "repo_user",
              default=DefaultConfig.repo_user,
              help='Private docker registry username\n'
                   'EXAMPLE: foo@bar.baz')
@click.option("-R", "--repo-pass", "repo_pass",
              default=DefaultConfig.repo_pass,
              help='Private docker registry password')
@click.option("--stop-signal", "stop_signal",
              type=int, default=DefaultConfig.stop_signal,
              help='Override the stop signal send to container')
@click.option("--disable-services-check", "disable_services_check",
              default=DefaultConfig.disable_services_check, is_flag=True, show_default=True,
              help='Disable services (swarm) check')
@click.option("--disable-containers-check", "disable_containers_check",
              default=DefaultConfig.disable_containers_check, is_flag=True, show_default=True,
              help='Disable standalone containers check')
@click.option("--hostname", "hostname",
              default=DefaultConfig.hostname, envvar="HOSTNAME",
              help='Set hostname (for debugging only)')
@click.option("-w", "--wait", "wait",
              default=DefaultConfig.wait, type=click.INT,
              help='Define a time in seconds to wait after an update before updating any others containers/services.')
def cli(docker_sockets, docker_tls, docker_tls_verify, interval, cron, log_level, run_once, notifiers,
        skip_start_notif, label, cleanup, repo_user, repo_pass, stop_signal, disable_services_check,
        disable_containers_check, template_file, hostname, latest, wait):
    """Declare command line options"""

    # Create App logger
    log = DocupdaterLogger(level=log_level)
    log.logger.info('Version: %s-%s', VERSION, BRANCH)

    config = Config(docker_sockets=docker_sockets,
                    docker_tls=docker_tls,
                    docker_tls_verify=docker_tls_verify,
                    interval=interval,
                    cron=cron,
                    log_level=log_level,
                    run_once=run_once,
                    notifiers=notifiers,
                    skip_start_notif=skip_start_notif,
                    label=label,
                    cleanup=cleanup,
                    repo_user=repo_user,
                    repo_pass=repo_pass,
                    stop_signal=stop_signal,
                    disable_services_check=disable_services_check,
                    disable_containers_check=disable_containers_check,
                    template_file=template_file,
                    hostname=hostname,
                    latest=latest,
                    wait=wait)

    log.logger.debug("pyupdater configuration: %s", config.options)

    notification_manager = NotificationManager(config)
    scheduler = BackgroundScheduler()
    scheduler.start()

    for socket in config.docker_sockets:
        try:
            docker = Docker(socket, config, notification_manager)
            scanner = Scanner(docker)

            if config.cron:
                scheduler.add_job(
                    scanner.update,
                    name=f'Cron container update for {socket}',
                    trigger='cron',
                    minute=config.cron[0],
                    hour=config.cron[1],
                    day=config.cron[2],
                    month=config.cron[3],
                    day_of_week=config.cron[4],
                    misfire_grace_time=20
                )
            else:
                if config.run_once:
                    scheduler.add_job(scanner.update, name=f'Run Once container update for {socket}')
                else:
                    scheduler.add_job(
                        scanner.update,
                        name=f'Initial run interval container update for {socket}'
                    )
                    scheduler.add_job(
                        scanner.update,
                        name=f'Interval container update for {socket}',
                        trigger='interval', seconds=config.interval,
                        misfire_grace_time=20
                    )
        except ConnectionError:
            log.logger.error("Could not connect to socket %s. Check your config", config.socket)

    if config.run_once:
        next_run = None
    elif config.cron:
        next_run = scheduler.get_jobs()[0].next_run_time
    else:
        now = datetime.now(timezone.utc).astimezone()
        next_run = (now + timedelta(0, config.interval)).strftime("%Y-%m-%d %H:%M:%S")

    if not config.skip_start_notif:
        notification_manager.send(StartupMessage(config.hostname, next_run=next_run), config.notifiers)

    while scheduler.get_jobs():
        sleep(10)

    scheduler.shutdown()


def main():
    cli(auto_envvar_prefix="DOCUPDATER")


if __name__ == "__main__":
    main()
