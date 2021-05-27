from git_guardrails.cli.ux import CLIUX, generate_welcome_banner


def test_generate_welcome_banner():
    s = generate_welcome_banner()
    assert s is not None


def test_cliux_creation():
    cli = CLIUX()
    assert cli is not None
