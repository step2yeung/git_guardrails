import os
import sys
import re

from git_guardrails.cli.tty import is_tty_supported

try:
    import colorama
    colorama.init()
except (ImportError, OSError):
    HAS_COLORAMA = False
else:
    HAS_COLORAMA = True


def supports_color() -> bool:
    """
    Return True if the running system's terminal supports color,
    and False otherwise.

    Taken with appreciation from Django codebase
    https://github.com/django/django/blob/0d67481a6664a1e66d875eef59b96ed489060601/django/core/management/color.py
    Permissable use under the Django BSD License
    """
    def vt_codes_enabled_in_windows_registry():
        """
        Check the Windows Registry to see if VT code handling has been enabled
        by default, see https://superuser.com/a/1300251/447564.
        """
        try:
            # winreg is only available on Windows.
            import winreg
        except ImportError:
            return False
        else:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Console')
            try:
                reg_key_value, _ = winreg.QueryValueEx(reg_key, 'VirtualTerminalLevel')
            except FileNotFoundError:
                return False
            else:
                return reg_key_value == 1

    return is_tty_supported() and (
        sys.platform != 'win32' or
        HAS_COLORAMA or
        'ANSICON' in os.environ or
        # Windows Terminal supports VT codes.
        'WT_SESSION' in os.environ or
        # Microsoft Visual Studio Code's built-in terminal supports colors.
        os.environ.get('TERM_PROGRAM') == 'vscode' or
        os.environ.get('TERM_PROGRAM') == 'vscode' or
        vt_codes_enabled_in_windows_registry()
    )


def strip_ansi(text: str) -> str:
    # 7-bit C1 ANSI sequences
    ansi_escape = re.compile(r'''
      \x1B  # ESC
      (?:   # 7-bit C1 Fe (except CSI)
          [@-Z\\-_]
      |     # or [ for CSI, followed by a control sequence
          \[
          [0-?]*  # Parameter bytes
          [ -/]*  # Intermediate bytes
          [@-~]   # Final byte
      )
  ''', re.VERBOSE)
    result = ansi_escape.sub('', text)
    return result
