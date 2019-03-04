import time

from click.testing import CliRunner

from docupdater.docupdater import cli
from docupdater.lib.scanner import Scanner


def test_cli_default_options(mocker, monkeypatch):
    monkeypatch.setattr(time, 'sleep', lambda s: None)
    monkeypatch.setattr("apscheduler.schedulers.base.BaseScheduler.get_jobs", lambda s: False)
    mocker.patch("docupdater.lib.scanner.Scanner.update")

    runner = CliRunner()
    result = runner.invoke(cli, [])

    assert result.exit_code == 0
    Scanner.update.assert_any_call()
