RE = "\033[1;31m"
GR = "\033[1;32m"
CY = "\033[1;36m"


def plus_simbol_text(text: str) -> str:
    return GR + '[+] ' + text


def emphasis_format(text: str) -> str:
    return GR + '[' + RE + text + GR + ']' + CY + ' '
