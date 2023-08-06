# text2code
Parses arbitrary strings and returns a dictionary.

## Usage

```
from text2code import text2code as t2c

d = t2c("""
def f(x, y):
    return x + y

def a(b, c):
    return b + c
""")
```

The result of this code would be a dictionary with 2 keys: `f`, and `a`, both of which would be the functions defined above.
