# Second Python's rule: Explicit is better than implicit.

alpha_mapping = {
    ord('q'): ord('й'),
    ord('w'): ord('ц'),
    ord('e'): ord('у'),
    ord('r'): ord('к'),
    ord('t'): ord('е'),
    ord('y'): ord('н'),
    ord('u'): ord('г'),
    ord('i'): ord('ш'),
    ord('o'): ord('щ'),
    ord('p'): ord('з'),
    ord('a'): ord('ф'),
    ord('s'): ord('ы'),
    ord('d'): ord('в'),
    ord('f'): ord('а'),
    ord('g'): ord('п'),
    ord('h'): ord('р'),
    ord('j'): ord('о'),
    ord('k'): ord('л'),
    ord('l'): ord('д'),
    ord('z'): ord('я'),
    ord('x'): ord('ч'),
    ord('c'): ord('с'),
    ord('v'): ord('м'),
    ord('b'): ord('и'),
    ord('n'): ord('т'),
    ord('m'): ord('ь'),
}

non_alpha_mapping = {
    ord(';'): ord('ж'),
    ord("'"): ord('э'),
    ord('['): ord('х'),
    ord(']'): ord('ъ'),
    ord(','): ord('б'),
    ord('.'): ord('ю'),
    ord('§'): ord('ё'),
    ord('?'): ord(','),
    ord('&'): ord('?'),
    ord('<'): ord('Б'),
    ord('>'): ord('Ю'),
}

uppers_mapping = {ord(chr(k).upper()): ord(chr(v).upper()) for k, v in alpha_mapping.items()}

cyrillic_latin_mapping = {
    **alpha_mapping,
    **non_alpha_mapping,
    **uppers_mapping
}

cyrillic_symbols = {
    chr(symbol) for symbol in cyrillic_latin_mapping.values() if chr(symbol).isalpha()
}
