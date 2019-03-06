from pathlib import Path

import pytest

from docupdater.lib.config import DefaultConfig, Config, DEFAULT_REGEX_WEIGHT, MINIMUM_INTERVAL, OptionRegex


def _update_config(options, new_options):
    options.update(new_options)
    return Config(**options)


def test_config(config):
    def check(key, value):
        print(key)
        return value == getattr(config, key)

    assert config.hostname == DefaultConfig.hostname
    assert all([check(key, value) for key, value in DefaultConfig.__dict__.items() if "__" not in key])
    assert config.template is not None
    assert config.auth_json is None


def test_config_with_option():
    option_dict = {key: value for key, value in DefaultConfig.__dict__.items() if "__" not in key}

    option_dict["run_once"] = True
    option_dict["latest"] = True
    option_dict["recreate_first"] = True
    option_dict["cleanup"] = True
    option_dict["starts"] = ["myRegex"]
    option_dict["stops"] = ["weight:999,myRegex", "container2"]

    config = Config(**option_dict)

    assert config.run_once is True
    assert config.latest is True
    assert config.recreate_first is True
    assert config.cleanup is True
    assert len(config.starts) == 1
    assert config.starts[0].weight == DEFAULT_REGEX_WEIGHT
    assert len(config.stops) == 2
    assert config.stops[0].weight == 999
    assert config.stops[1].weight == DEFAULT_REGEX_WEIGHT


def test_config_load_labels(config):
    new_config = _update_config(config.options, {
        "recreate_first": True
    })

    assert new_config.latest is False
    assert len(new_config.notifiers) == 0
    assert new_config.cleanup is False
    assert new_config.wait == DefaultConfig.wait
    assert new_config.recreate_first is True

    dir_path = Path().absolute()
    template_file = dir_path.joinpath("docupdater/templates/notification.j2")

    config2 = Config.from_labels(new_config, {
        "docupdater.latest": True,
        "docupdater.notifiers": "slack://token slack://token2",
        "docupdater.cleanup": True,
        "docupdater.wait": 60,
        "docupdater.recreate_first": False,
        "docupdater.template_file": template_file,
        "docupdater.starts": "Container1",
        "docupdater.stops": "weight:1,Container1 Container2"
    })

    assert config2.hostname == config.hostname
    assert config2.latest is True
    assert len(config2.notifiers) == 2
    assert config2.cleanup is True
    assert config2.wait == 60
    assert config2.recreate_first is False
    assert config2.starts
    assert config2.starts[0].weight == DEFAULT_REGEX_WEIGHT, config2.starts
    assert config2.stops
    assert config2.stops[0].weight == 1, config2.stops
    assert config2.stops[1].weight == DEFAULT_REGEX_WEIGHT, config2.stops
    assert config2.template is not None


def test_config_invalid(config):
    # Test to GET an invalid attribute
    with pytest.raises(AttributeError):
        config.invalid_option


def test_config_set_attribute(config):
    # Set a attribute
    config.hostname = "MyTestHostname"
    assert config.hostname == "MyTestHostname"


def test_config_with_auth(config):
    new_config = _update_config(config.options, {
        "repo_user": "Username",
        "repo_pass": "Password"
    })
    assert new_config.auth_json is not None


def test_config_invalid_check(config):
    with pytest.raises(AttributeError):
        new_config = _update_config(config.options, {
            "disable_containers_check": True,
            "disable_services_check": True
        })


def test_config_minimum_interval(config):
    new_config = _update_config(config.options, {
        "interval": 1
    })
    assert new_config.interval == MINIMUM_INTERVAL


def test_config_test_cron(config):
    new_config = _update_config(config.options, {
        "cron": "* * * * *"
    })
    assert new_config.cron is not None


def test_config_test_invalid_cron(config):
    with pytest.raises(AttributeError):
        new_config = _update_config(config.options, {
            "cron": "* * *"
        })


def test_config_invalid_template(config):
    with pytest.raises(AttributeError):
        new_config = _update_config(config.options, {
            "template_file": "/invalid.j2"
        })


def test_config_option_regex_object():
    assert OptionRegex("hello-.*").regex.pattern == "hello-.*"
    assert OptionRegex("hello-.*").weight == DEFAULT_REGEX_WEIGHT
    assert OptionRegex("weight:1,myregex").weight == 1
    assert OptionRegex("weight:999,myregex").weight == 999
    with pytest.raises(AttributeError):
        OptionRegex("InvalidRegex[")
