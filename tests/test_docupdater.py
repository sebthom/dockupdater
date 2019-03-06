import pytest
from click.testing import CliRunner

from docupdater.docupdater import cli
from docupdater.lib.scanner import Scanner


@pytest.mark.cli
def test_cli_default_options(mocker):
    mocker.patch("docupdater.lib.scanner.Scanner.update")
    mocker.patch("docupdater.docupdater.apscheduler_wait")

    runner = CliRunner()
    result = runner.invoke(cli, [])

    assert result.exit_code == 0
    Scanner.update.assert_any_call()


@pytest.mark.cli
def test_cli_test_cron_option(mocker):
    mocker.patch("docupdater.docupdater.apscheduler_wait")
    mocker.patch("docupdater.lib.scanner.Scanner.update")

    runner = CliRunner()
    result = runner.invoke(cli, ["--cron", "0 12 * * *"])

    assert result.exit_code == 0
