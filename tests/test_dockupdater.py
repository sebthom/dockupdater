import time

import pytest
from click.testing import CliRunner

from dockupdater.dockupdater import cli
from dockupdater.lib.scanner import Scanner


@pytest.mark.cli
def test_cli_default_options(mocker, monkeypatch):
    monkeypatch.setattr(time, 'sleep', lambda s: None)
    monkeypatch.setattr("apscheduler.schedulers.base.BaseScheduler.get_jobs", lambda s: False)
    mocker.patch("dockupdater.lib.scanner.Scanner.update")

    runner = CliRunner()
    result = runner.invoke(cli, [])

    assert result.exit_code == 0
    Scanner.update.assert_any_call()
