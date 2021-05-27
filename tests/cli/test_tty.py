from git_guardrails.cli.tty import is_tty_supported


def test_is_tty_supported():
    result = is_tty_supported()
    assert result is not None
