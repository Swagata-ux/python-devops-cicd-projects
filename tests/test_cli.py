from click.testing import CliRunner
from pytest_mock import MockerFixture

from simple_http_checker.cli import main


def test_no_urls():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "Usage: check-urls" in result.output


def test_single_url_success(mocker: MockerFixture):
    mock_check_urls = mocker.patch(
        "simple_http_checker.cli.check_urls"
    )
    mock_check_urls.return_value = {
        "https://example.com": "200 OK"
    }
    
    runner = CliRunner()
    result = runner.invoke(main, ["https://example.com"])
    assert result.exit_code == 0
    assert "200 OK" in result.output
    mock_check_urls.assert_called_once_with(
        ("https://example.com",), 5
    )


def test_multiple_urls(mocker: MockerFixture):
    mock_check_urls = mocker.patch(
        "simple_http_checker.cli.check_urls"
    )
    mock_check_urls.return_value = {
        "https://example.com": "200 OK",
        "https://notfound.com": "404 Not Found",
    }
    
    runner = CliRunner()
    result = runner.invoke(
        main, ["https://example.com", "https://notfound.com"]
    )
    assert result.exit_code == 0
    assert "200 OK" in result.output
    assert "404 Not Found" in result.output


def test_custom_timeout(mocker: MockerFixture):
    mock_check_urls = mocker.patch(
        "simple_http_checker.cli.check_urls"
    )
    mock_check_urls.return_value = {
        "https://example.com": "200 OK"
    }
    
    runner = CliRunner()
    result = runner.invoke(
        main, ["--timeout", "10", "https://example.com"]
    )
    assert result.exit_code == 0
    mock_check_urls.assert_called_once_with(
        ("https://example.com",), 10
    )


def test_verbose_flag(mocker: MockerFixture):
    mock_check_urls = mocker.patch(
        "simple_http_checker.cli.check_urls"
    )
    mock_check_urls.return_value = {
        "https://example.com": "200 OK"
    }
    
    runner = CliRunner()
    result = runner.invoke(
        main, ["-v", "https://example.com"]
    )
    assert result.exit_code == 0
    # Verbose logging goes to stderr/logs, not stdout
    assert "200 OK" in result.output