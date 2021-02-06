from inori.utils.string_template import StringTemplate


def test_string_template_no_template():
    dummy = StringTemplate('Mighty Pirate')

    assert 'Mighty Pirate' == dummy


def test_string_template_partial():
    s = StringTemplate('${hello} ${world}')
    s.format(hello='Hello')

    assert 'Hello ${world}' == s


def test_string_template_full():
    s = StringTemplate('${hello} ${world}')
    s.format(hello='Hello', world='World')

    assert 'Hello World' == s


def test_string_template_str():
    s = StringTemplate('${hello} ${world}')

    assert '${hello} ${world}' == str(s)


def test_string_template_formatted_then_str():
    s = StringTemplate('${hello} ${world}')
    s.format(hello='Hello')

    assert 'Hello ${world}' == str(s)
