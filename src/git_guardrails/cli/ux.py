from colorama import init as initColorama, Style, Fore

initColorama()


def generate_welcome_banner():
    return ''.join(
        [
            Style.DIM, "|===|===|===|==", Style.RESET_ALL,
            Fore.LIGHTCYAN_EX, " Git Guardrails ", Fore.RESET,
            Style.DIM, "==|===|===|===|", Style.RESET_ALL
        ]
    )


class CLIUX:
    def __init__(self):
        return
