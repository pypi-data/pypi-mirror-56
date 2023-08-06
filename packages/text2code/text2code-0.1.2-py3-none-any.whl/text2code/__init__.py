"""Provides the text2code function."""


def text2code(string, filename, **globs):
    """Parses the given string as code, which is evaluated with the current
    globals, as well as any additional globals passed with globs. A dictionary
    is returned with name: variable pairs."""
    g = globals().copy()
    g.update(**globs)
    old_names = set(g.keys())
    code = compile(string, filename, 'exec')
    eval(code, g)
    new_names = set(g.keys()).difference(old_names)
    return {name: g[name] for name in new_names}
