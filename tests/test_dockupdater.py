import pytest
from click.testing import CliRunner

from dockupdater.dockupdater import cli
from dockupdater.lib.scanner import Scanner


@pytest.mark.cli
def test_cli_default_options(mocker):
    mocker.patch("dockupdater.lib.scanner.Scanner.update")
    mocker.patch("dockupdater.dockupdater.apscheduler_wait")

    runner = CliRunner()
    result = runner.invoke(cli, [])

    assert result.exit_code == 0
    Scanner.update.assert_any_call()


@pytest.mark.cli
def test_cli_test_cron_option(mocker):
    mocker.patch("dockupdater.dockupdater.apscheduler_wait")
    mocker.patch("dockupdater.lib.scanner.Scanner.update")

    runner = CliRunner()
    result = runner.invoke(cli, ["--cron", "0 12 * * *"])

    assert result.exit_code == 0
