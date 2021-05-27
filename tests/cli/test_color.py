from colorama import Fore
from git_guardrails.cli.color import supports_color, strip_ansi


def test_strip_ansi():
    s1 = strip_ansi('abc')
    assert s1 is not None
    assert s1 == 'abc'

    s2 = strip_ansi(Fore.CYAN + 'pear ' + Fore.GREEN + 'grape')
    assert s2 is not None
    assert s2 == 'pear grape'


def test_supports_color():
    color_is_supported = supports_color()
    assert color_is_supported in [True, False]
