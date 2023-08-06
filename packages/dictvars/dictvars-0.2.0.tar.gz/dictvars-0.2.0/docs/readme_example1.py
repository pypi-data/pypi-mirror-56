
from dictvars import dictvars, varsnamed


myapp = 'MyApp'  # global var


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


def main():
    from pprint import pprint
    pprint(somefunc_regular_python())
    pprint(somefunc_dictvars())
    pprint(somefunc_varsnamed())


if __name__ == '__main__':
    main()
