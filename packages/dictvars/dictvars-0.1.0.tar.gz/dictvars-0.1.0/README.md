[![Build Status](https://travis-ci.com/fabianoengler/dictvars.svg?branch=master)](https://travis-ci.com/fabianoengler/dictvars)
[![Coverage Status](https://coveralls.io/repos/github/fabianoengler/dictvars/badge.svg)](https://coveralls.io/github/fabianoengler/dictvars)

# dictvars

Create dicts from variables in scope.


## Why?

In python it is very common to create a dict from variables already
defined, for example when returning a context dict from a view function
that will be passed to a serializer or a template render.

Code like this:

```python
    return dict(user=user, form=form, comments=comments)
```

With `varsdict` you can get rid of the redundancy of having all
variables named twice in the code.

The above code can be replaced for this:

```python
    return dictvars(user, form, comments)
```

Alternatively, variable names can be passed as strings with `varsnamed`:

```python
    return varsnamed('form', 'comments', 'myapp')
```

## Install

```
pip install dictvars
```

## Example

Global variables can be passed to `varsdict` as well.

The following example is a complete code to illustrate how
a "real" code looks like when using and not using `varsdict`
 and `varsnamed`.

```python
from dictvars import dictvars, varsnamed


myapp = 'MyApp'  # a global var


def somefunc_regular_python():
    # pretend this is a controller code that makes sense
    user = dict(some='very', complex_='expression')
    permission = user.get('permission', False)
    user_has_permission = bool(permission)
    form = dict(another='object', perm=user_has_permission)
    comments = []
    for values in [d.values() for d in [user, form]]:
        comments.extend([v for v in values if isinstance(v, str)])

    return dict(form=form, comments=comments, myapp=myapp)


def somefunc_dictvars():
    # pretend this is a controller code that makes sense
    user = dict(some='very', complex_='expression')
    permission = user.get('permission', False)
    user_has_permission = bool(permission)
    form = dict(another='object', perm=user_has_permission)
    comments = []
    for values in [d.values() for d in [user, form]]:
        comments.extend([v for v in values if isinstance(v, str)])

    return dictvars(form, comments, myapp)


def somefunc_varsnamed():
    # pretend this is a controller code that makes sense
    user = dict(some='very', complex_='expression')
    permission = user.get('permission', False)
    user_has_permission = bool(permission)
    form = dict(another='object', perm=user_has_permission)
    comments = []
    for values in [d.values() for d in [user, form]]:
        comments.extend([v for v in values if isinstance(v, str)])

    return varsnamed('form', 'comments', 'myapp')


if __name__ == '__main__':
    from pprint import pprint
    pprint(somefunc_regular_python())
    pprint(somefunc_dictvars())
    pprint(somefunc_varsnamed())

```


Output is the same in all versions:

```
{'comments': ['very', 'expression', 'object'],
 'form': {'another': 'object', 'perm': False},
 'myapp': 'MyApp'}
{'comments': ['very', 'expression', 'object'],
 'form': {'another': 'object', 'perm': False},
 'myapp': 'MyApp'}
{'comments': ['very', 'expression', 'object'],
 'form': {'another': 'object', 'perm': False},
 'myapp': 'MyApp'}
```

## Limitations

To create a dict from the passed variables, some "magic" is done to
obtain the original variables names: the variables list from the scope
is traversed looking for variables that are the same (same reference,
same id).

This implementation detail can lead to unintended leak of variables
when an object is referenced more then one time.

An example:

```python
def somefunc():
    a = '1'
    b = '2'
    c = '3'
    leak = b
    return dictvars(a, b)

print(somefunc())
```

Returns:
```
{'a': '1',
 'b': '2',
 'leak': '2'}
```

Please note that no new value or object is leaked, only the name of
an object that was already in the dict.

I find that this is rare enough to not be a problem most of the time,
additional variables returned usually can just be ignored.

I'm not sure how to fix this yet. Open to suggestions.

If this is a problem on a specific context, one can just swap
`dictvars` for `varsnamed` and pass the variable names as strings
instead:

```python
def somefunc():
    a = '1'
    b = '2'
    c = '3'
    no_leaks_now = b
    return varsnamed('a', 'b')

print(somefunc())
```

Returns:
```
{'a': '1',
 'b': '2'}
```
