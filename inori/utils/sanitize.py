import keyword


def safe_keyword(word: str) -> str:
    """If word is a python keyword, add an underscore prefix.

    Arguments:
        word: A string with a single word in it.

    Returns:
        str: The word, in a safe form.
    """
    if keyword.iskeyword(word):
        return f'_{word}'
    return word


def safe_illegal_character(word: str) -> str:
    """If word has an illegal character in it, replace with an underscore.

    Arguments:
        word: A string with a single word in it.

    Returns:
        str: The word, in a safe form.
    """
    if '-' in word:
        return word.replace('-', '_')
    return word
