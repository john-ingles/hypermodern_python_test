from unittest.mock import Mock

import click.testing
import pytest
import requests
from pytest_mock import MockerFixture

from hypermodern_python_test import console


@pytest.fixture
def runner() -> click.testing.CliRunner:
    return click.testing.CliRunner()


@pytest.fixture
def mock_wikipedia_random_page(mocker: MockerFixture) -> Mock:
    return mocker.patch("hypermodern_python_test.wikipedia.random_page")


def test_main_succeeds(
    runner: click.testing.CliRunner, mock_requests_get: Mock
) -> None:
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(
    runner: click.testing.CliRunner, mock_requests_get: Mock
) -> None:
    result = runner.invoke(console.main)
    assert "Lorem Ipsum" in result.output


def test_main_invokes_requests_get(
    runner: click.testing.CliRunner, mock_requests_get: Mock
) -> None:
    runner.invoke(console.main)
    assert mock_requests_get.called


def test_main_uses_en_wikipedia_org(
    runner: click.testing.CliRunner, mock_requests_get: Mock
) -> None:
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]


def test_main_fails_on_request_error(
    runner: click.testing.CliRunner, mock_requests_get: Mock
) -> None:
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(console.main)
    assert result.exit_code == 1


def test_main_prints_message_on_request_error(
    runner: click.testing.CliRunner, mock_requests_get: Mock
) -> None:
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output


def test_main_uses_specified_language(
    runner: click.testing.CliRunner, mock_wikipedia_random_page: Mock
) -> None:
    runner.invoke(console.main, ["--language=pl"])
    mock_wikipedia_random_page.assert_called_with(language="pl")


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner: click.testing.CliRunner) -> None:
    result = runner.invoke(console.main)
    assert result.exit_code == 0
