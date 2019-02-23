from copy import deepcopy
from logging import getLogger
from os import environ
from pathlib import Path

from .logger import BlacklistFilter

ENABLE_LABEL = "docupdater.enable"
DISABLE_LABEL = "docupdater.disable"

LABELS_MAPPING = {
    "docupdater.notifiers": "notifiers",
    "docupdater.stop_signal": "stop_signal",
    "docupdater.cleanup": "cleanup",
    "docupdater.template_file": "template_file"
}


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
    stop_signal = None
    disable_containers_check = False
    disable_services_check = False

    repo_user = None
    repo_pass = None

    notifiers = []
    skip_start_notif = False
    template_file = None


class Config(object):
    def __init__(self, **kwargs):
        self.options = kwargs
        self.logger = getLogger()
        self.compute_args()
        self.filtered_strings = None
        self.config_blacklist()

    @property
    def hostname(self):
        return self.options.get("hostname")

    @hostname.setter
    def hostname(self, value):
        self.options["hostname"] = value

    @property
    def interval(self):
        return self.options.get("interval")

    @interval.setter
    def interval(self, value):
        self.options["interval"] = value

    @property
    def cron(self):
        return self.options.get("cron")

    @cron.setter
    def cron(self, value):
        self.options["cron"] = value

    @property
    def docker_socket(self):
        return self.options.get("docker_socket")

    @docker_socket.setter
    def docker_socket(self, value):
        self.options["docker_socket"] = value

    @property
    def docker_tls(self):
        return self.options.get("docker_tls")

    @docker_tls.setter
    def docker_tls(self, value):
        self.options["docker_tls"] = value

    @property
    def docker_tls_verify(self):
        return self.options.get("docker_tls_verify")

    @docker_tls_verify.setter
    def docker_tls_verify(self, value):
        self.options["docker_tls_verify"] = value

    @property
    def log_level(self):
        return self.options.get("log_level")

    @log_level.setter
    def log_level(self, value):
        self.options["log_level"] = value

    @property
    def cleanup(self):
        return self.options.get("cleanup")

    @cleanup.setter
    def cleanup(self, value):
        self.options["cleanup"] = value

    @property
    def run_once(self):
        return self.options.get("run_once")

    @run_once.setter
    def run_once(self, value):
        self.options["run_once"] = value

    @property
    def label(self):
        return self.options.get("label")

    @label.setter
    def label(self, value):
        self.options["label"] = value

    @property
    def stop_signal(self):
        return self.options.get("stop_signal")

    @stop_signal.setter
    def stop_signal(self, value):
        self.options["stop_signal"] = value

    @property
    def disable_containers_check(self):
        return self.options.get("disable_containers_check")

    @disable_containers_check.setter
    def disable_containers_check(self, value):
        self.options["disable_containers_check"] = value

    @property
    def disable_services_check(self):
        return self.options.get("disable_services_check")

    @disable_services_check.setter
    def disable_services_check(self, value):
        self.options["disable_services_check"] = value

    @property
    def repo_user(self):
        return self.options.get("repo_user")

    @repo_user.setter
    def repo_user(self, value):
        self.options["repo_user"] = value

    @property
    def repo_pass(self):
        return self.options.get("repo_pass")

    @repo_pass.setter
    def repo_pass(self, value):
        self.options["repo_pass"] = value

    @property
    def notifiers(self):
        return self.options.get("notifiers")

    @notifiers.setter
    def notifiers(self, value):
        self.options["notifiers"] = value

    @property
    def skip_start_notif(self):
        return self.options.get("skip_start_notif")

    @skip_start_notif.setter
    def skip_start_notif(self, value):
        self.options["skip_start_notif"] = value

    @property
    def template_file(self):
        return self.options.get("template_file")

    @template_file.setter
    def template_file(self, value):
        self.options["template_file"] = value

    @property
    def template(self):
        return self.options.get("template")

    @template.setter
    def template(self, value):
        self.options["template"] = value

    @property
    def auth_json(self):
        return self.options.get("auth_json")

    @auth_json.setter
    def auth_json(self, value):
        self.options["auth_json"] = value

    @classmethod
    def from_labels(cls, config, labels):
        options = deepcopy(config.options)

        if labels:
            for label, value in labels.items():
                if label in LABELS_MAPPING:
                    options[LABELS_MAPPING[label]] = value
                    if label == "docupdater.template_file":
                        # Reload template
                        options["template"] = Config.load_template(options.get('template_file'))

        return cls(**options)

    def config_blacklist(self):
        filtered_strings = [getattr(self, key.lower()) for key, value in self.options.items()
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

        for handler in self.logger.handlers:
            handler.addFilter(BlacklistFilter(set(self.filtered_strings)))

    def compute_args(self):
        if self.repo_user and self.repo_pass:
            self.auth_json = {'Username': self.repo_user, 'Password': self.repo_pass}

        if self.disable_containers_check and self.disable_services_check:
            raise AttributeError("Error you can't disable all monitoring.")

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

        self.template = Config.load_template(self.template_file)

    @staticmethod
    def load_template(template_file):
        # Load default template file
        if not template_file:
            dir_path = Path().absolute()
            template_file = dir_path.joinpath("docupdater/templates/notification.j2")

        if Path(template_file).exists():
            with open(template_file) as f:
                return f.read()
        else:
            raise AttributeError(f"Template file {template_file} not found")
