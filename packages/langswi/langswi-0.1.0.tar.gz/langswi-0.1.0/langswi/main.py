import sys
import subprocess

from langswi.mapping import cyrillic_latin_mapping, cyrillic_symbols


def get_mapping(input: str) -> dict:
    input = ''.join(
        symbol for symbol in input.strip().replace(' ', '') if symbol.isalpha()
    )

    if set(input.lower()) <= cyrillic_symbols:
        mapping = {v: k for k, v in cyrillic_latin_mapping.items()}
    else:
        mapping = cyrillic_latin_mapping

    return mapping


def translate(input: str) -> str:
    mapping = get_mapping(input)

    result = ''
    for symbol in input:
        if ord(symbol) in mapping.keys():
            result += chr(mapping[ord(symbol)])
        else:
            result += symbol

    return result


def get_stdout() -> str:
    args = ('pbpaste', 'r',)
    process = subprocess.Popen(args, stdout=subprocess.PIPE, close_fds=True)
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8')


def main() -> None:
    input = get_stdout()
    result = translate(input)
    sys.stdout.write(result + '\n')
