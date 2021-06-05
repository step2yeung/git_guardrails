from logging import DEBUG
from git_guardrails.cli.color import strip_ansi
from git_guardrails.cli.ux import CLIUX, generate_welcome_banner
from git_guardrails_test_helpers.cliux_test_utils import fake_cliux


def test_generate_welcome_banner():
    s = generate_welcome_banner()
    assert s is not None


def test_cliux_creation():
    cli = CLIUX(supports_color=False, log_level=DEBUG, supports_tty=False)
    assert cli is not None


def test_cliux_logging():
    with fake_cliux(log_level=DEBUG) as (cli, get_lines):
        cli.info('grapes')
        cli.debug('apple')
        cli.warning('pear')
        cli.error('orange')
        lines = "".join(get_lines())
        assert strip_ansi(lines) == """[INFO]: grapes
[DEBUG]: apple
[WARNING]: pear
[ERROR]: orange
"""
