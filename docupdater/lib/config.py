from logging import getLogger
from os import environ
from pathlib import Path

from .logger import BlacklistFilter


class DefaultConfig(object):
    hostname = environ.get('HOSTNAME')
    interval = 300
    cron = None
    docker_socket = 'unix://var/run/docker.sock'
    docker_tls = False
    docker_tls_verify = True
    log_level = 'info'
    cleanup = False
    run_once = False
    label = False

    repo_user = None
    repo_pass = None

    notifiers = []
    skip_start_notif = False
    template_file = None


class Config(object):
    def __init__(self, **kwargs):
        self.options = kwargs

        self.compute_args()

        self.filtered_strings = None
        self.config_blacklist()

        self.logger = getLogger()

    def __getattr__(self, attr):
        if attr in self.options:
            return self.options.get(attr)
        raise AttributeError("%r object has no attribute %r" %
                             (self.__class__.__name__, attr))

    def __setattr__(self, attr, value):
        if attr in self.options:
            self.config[attr] = value
        else:
            super().__setattr__(attr, value)

    def config_blacklist(self):
        filtered_strings = [getattr(self, key.lower()) for key in Config.options
                            if key.lower() in BlacklistFilter.blacklisted_keys]
        # Clear None values
        self.filtered_strings = list(filter(None, filtered_strings))
        # take lists inside of list and append to list
        for index, value in enumerate(self.filtered_strings, 0):
            if isinstance(value, list):
                self.filtered_strings.extend(self.filtered_strings.pop(index))
                self.filtered_strings.insert(index, self.filtered_strings[-1:][0])
        # Added matching for ports
        ports = [string.split(':')[0] for string in self.filtered_strings if ':' in string]
        self.filtered_strings.extend(ports)
        # Added matching for tcp sockets. ConnectionPool ignores the tcp://
        tcp_sockets = [string.split('//')[1] for string in self.filtered_strings if '//' in string]
        self.filtered_strings.extend(tcp_sockets)
        # Get JUST hostname from tcp//unix
        for socket in getattr(self, 'docker_sockets'):
            self.filtered_strings.append(socket.split('//')[1].split(':')[0])

        for handler in self.logger.handlers:
            handler.addFilter(BlacklistFilter(set(self.filtered_strings)))

    def compute_args(self):
        if self.repo_user and self.repo_pass:
            self.config["auth_json"] = {'Username': self.repo_user, 'Password': self.repo_pass}

        if self.interval < 30:
            self.logger.warning('Minimum value for interval was 30 seconds.')
            self.interval = 30

        # Config sanity checks
        if self.cron:
            cron_times = self.cron.strip().split(' ')
            if len(cron_times) != 5:
                self.logger.critical("Cron must be in cron syntax. e.g. * * * * * (5 places).")
                raise AttributeError("Invalid cron")
            else:
                self.logger.info("Cron configuration is valid. Using Cron schedule %s", cron_times)
                self.cron = cron_times
                self.interval = None

        # Load default template file
        if not self.template_file:
            dir_path = Path().absolute()
            if self.swarm:
                self.template_file = dir_path.joinpath("pypyupdater/templates/services.j2")
            else:
                self.template_file = dir_path.joinpath("pypyupdater/templates/containers.j2")

        if Path(self.template_file).exists():
            with open(self.template_file) as f:
                self.option["template"] = f.read()
        else:
            self.logger.critical("Template file %s not found", self.template_file)
            raise AttributeError(f"Template file {self.template_file} not found")
