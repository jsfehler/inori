from inori.utils.sanitize import safe_keyword, safe_illegal_character


def test_safe_keyword():
    result = safe_keyword('import')
    assert '_import' == result


def test_safe_keyword_no_match():
    result = safe_keyword('word')
    assert 'word' == result


def test_safe_keyword_multiple_words():
    result = safe_keyword('This is not a word.')
    assert 'This is not a word.' == result


def test_safe_illegal_character():
    result = safe_illegal_character('foo-bar')
    assert 'foo_bar' == result
