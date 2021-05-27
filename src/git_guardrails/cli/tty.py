import sys


def is_tty_supported() -> bool:
    """
    Taken with appreciation from Django codebase
    https://github.com/django/django/blob/0d67481a6664a1e66d875eef59b96ed489060601/django/core/management/color.py
    Permissable use under the Django BSD License
    """
    # isatty is not always implemented, https://code.djangoproject.com/ticket/6223.
    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
