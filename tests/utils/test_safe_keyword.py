from inori.utils.safe_keyword import safe_keyword


def test_safe_keyword():
    result = safe_keyword('import')
    assert '_import' == result


def test_safe_keyword_no_match():
    result = safe_keyword('word')
    assert 'word' == result


def test_safe_keyword_multiple_words():
    result = safe_keyword('This is not a word.')
    assert 'This is not a word.' == result
