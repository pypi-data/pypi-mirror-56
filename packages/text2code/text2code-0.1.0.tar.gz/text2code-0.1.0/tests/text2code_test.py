from text2code import text2code as t2c


def test_nothing():
    assert t2c('', 'test') == {}


def test_single_function():
    code = 'def f(a, b):\n return a + b\n'
    d = t2c(code, 'test')
    assert len(d) == 1
    f = d['f']
    assert f(5, 6) == 11


def test_multiple_functions():
    code = 'def a(x, y):\n return x + y\ndef b(x, y):\n return x * y\n'
    d = t2c(code, 'test')
    assert len(d) == 2
    a = d['a']
    b = d['b']
    assert a(3, 5) == 8
    assert b(3, 5) == 15
