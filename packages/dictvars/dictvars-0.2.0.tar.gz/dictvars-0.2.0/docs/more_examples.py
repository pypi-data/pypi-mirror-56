from dictvars import dictvars, varsnamed, compact


myapp = 'MyApp'  # global var
leaked_var_global = None


def filter_keys(mapping, *keys):
    return {k: mapping[k] for k in mapping if k in keys}


def somefunc_regular_python1():
    # pretend this is a controller code that makes sense
    user = dict(some='very', complex_='expression')
    permission = user.get('permission', False)
    user_has_permission = bool(permission)
    form = dict(another='object', perm=user_has_permission)
    comments = []
    for values in [d.values() for d in [user, form]]:
        comments.extend([v for v in values if isinstance(v, str)])

    return dict(form=form, comments=comments)


def somefunc_regular_python2():
    # pretend this is a controller code that makes sense
    user = dict(some='very', complex_='expression')
    permission = user.get('permission', False)
    user_has_permission = bool(permission)
    form = dict(another='object', perm=user_has_permission)
    comments = []
    for values in [d.values() for d in [user, form]]:
        comments.extend([v for v in values if isinstance(v, str)])

    return {'form': form, 'comments': comments}


def somefunc_regular_python_generic_awkward():
    # pretend this is a controller code that makes sense
    user = dict(some='very', complex_='expression')
    permission = user.get('permission', False)
    user_has_permission = bool(permission)
    form = dict(another='object', perm=user_has_permission)
    comments = []
    for values in [d.values() for d in [user, form]]:
        comments.extend([v for v in values if isinstance(v, str)])

    # very cumbersome
    return {k: v for k, v in locals().items() if k in ['form', 'comments']}


def somefunc_filter_keys():
    # pretend this is a controller code that makes sense
    user = dict(some='very', complex_='expression')
    permission = user.get('permission', False)
    user_has_permission = bool(permission)
    form = dict(another='object', perm=user_has_permission)
    comments = []
    for values in [d.values() for d in [user, form]]:
        comments.extend([v for v in values if isinstance(v, str)])

    # explict version with pure python and no external dependecies
    return filter_keys(locals(), 'form', 'comments')


def somefunc_varsnamed():
    # pretend this is a controller code that makes sense
    user = dict(some='very', complex_='expression')
    permission = user.get('permission', False)
    user_has_permission = bool(permission)
    form = dict(another='object', perm=user_has_permission)
    comments = []
    for values in [d.values() for d in [user, form]]:
        comments.extend([v for v in values if isinstance(v, str)])

    # similar to previous version, with the "magic" that locals() is
    # implict now, less boilerplate
    return varsnamed('form', 'comments')


def somefunc_varsnamed_global():
    # pretend this is a controller code that makes sense
    user = dict(some='very', complex_='expression')
    permission = user.get('permission', False)
    user_has_permission = bool(permission)
    form = dict(another='object', perm=user_has_permission)
    comments = []
    for values in [d.values() for d in [user, form]]:
        comments.extend([v for v in values if isinstance(v, str)])

    # adding a global variable now,
    # this wouldn't work with filter_keys version
    return varsnamed('form', 'comments', 'myapp')


def somefunc_compact_local():
    # pretend this is a controller code that makes sense
    user = dict(some='very', complex_='expression')
    permission = user.get('permission', False)
    user_has_permission = bool(permission)
    form = dict(another='object', perm=user_has_permission)
    comments = []
    for values in [d.values() for d in [user, form]]:
        comments.extend([v for v in values if isinstance(v, str)])

    # `compact` is just an alias to varsnamed,
    # more like an easteregg for PHP people moving to Python ;)
    return compact('form', 'comments')


def somefunc_compact_global():
    # pretend this is a controller code that makes sense
    user = dict(some='very', complex_='expression')
    permission = user.get('permission', False)
    user_has_permission = bool(permission)
    form = dict(another='object', perm=user_has_permission)
    comments = []
    for values in [d.values() for d in [user, form]]:
        comments.extend([v for v in values if isinstance(v, str)])

    # compact with a global var
    return compact('form', 'comments', 'myapp')


def somefunc_dictvars():
    # pretend this is a controller code that makes sense
    user = dict(some='very', complex_='expression')
    permission = user.get('permission', False)
    user_has_permission = bool(permission)
    form = dict(another='object', perm=user_has_permission)
    comments = []
    for values in [d.values() for d in [user, form]]:
        comments.extend([v for v in values if isinstance(v, str)])

    # finally `dictvars` version, the lesser boilerplate of all
    return dictvars(form, comments)


def somefunc_dictvars_global():
    # pretend this is a controller code that makes sense
    user = dict(some='very', complex_='expression')
    permission = user.get('permission', False)
    user_has_permission = bool(permission)
    form = dict(another='object', perm=user_has_permission)
    comments = []
    for values in [d.values() for d in [user, form]]:
        comments.extend([v for v in values if isinstance(v, str)])

    # `dictvars` version with a global var
    return dictvars(form, comments, myapp)


def somefunc_dictvars_kwargs():
    # pretend this is a controller code that makes sense
    current_user = dict(some='very', complex_='expression')
    permission = current_user.get('permission', False)
    user_has_permission = bool(permission)
    form = dict(another='object', perm=user_has_permission)
    comments = []
    for values in [d.values() for d in [current_user, form]]:
        comments.extend([v for v in values if isinstance(v, str)])

    # explicitly renaming a variable using keywords syntax 
    # just like a regular dict
    return dictvars(form, comments, user=current_user)


def somefunc_dictvars_local_leak():
    # pretend this is a controller code that makes sense
    user = dict(some='very', complex_='expression')
    permission = user.get('permission', False)
    user_has_permission = bool(permission)
    form = dict(another='object', perm=user_has_permission)
    comments = []
    leaked_var_local = form
    for values in [d.values() for d in [user, form]]:
        comments.extend([v for v in values if isinstance(v, str)])

    # the variable `leaked_var_local` will also be returned
    # because it is actually the same variable as `form`, just with
    # another name (e.g. id(form) == id(leaked_var_local))
    return dictvars(form, comments, myapp)


def somefunc_dictvars_global_leak():
    # pretend this is a controller code that makes sense
    user = dict(some='very', complex_='expression')
    permission = user.get('permission', False)
    user_has_permission = bool(permission)
    form = dict(another='object', perm=user_has_permission)
    comments = []
    global leaked_var_global
    leaked_var_global = myapp
    for values in [d.values() for d in [user, form]]:
        comments.extend([v for v in values if isinstance(v, str)])

    # global vars can also leak when the same object is referenced
    # by more than one name
    return dictvars(form, comments, myapp)


def somefunc_dictvars_kwargs_nonleak():
    # pretend this is a controller code that makes sense
    user = dict(some='very', complex_='expression')
    permission = user.get('permission', False)
    user_has_permission = bool(permission)
    form = dict(another='object', perm=user_has_permission)
    comments = []
    global leaked_var_global
    leaked_var_local = form
    leaked_var_global = myapp
    for values in [d.values() for d in [user, form]]:
        comments.extend([v for v in values if isinstance(v, str)])

    # if the vars are explicitly named (using kwargs syntax)
    # any leaks can be supressed
    return dictvars(comments, form=form, myapp=myapp)


def somefunc_dictvars_local_python_optimization():
    some_num = 42
    some_str = 'hi'
    another_num = 3333
    another_str = 'byebye'
    yet_another_num = 42
    yet_another_str = 'hi'

    # sometimes python can cached small immutable values and reuse them,
    # when this happens, the variables will reference the same object in
    # memory, which can also trigger a leak
    # this code may or may not return yet_another_num and yet_another_str
    # depending on the python interpreter implementation
    # (it does on cpython)
    return dictvars(some_num, some_str)


def main():
    from pprint import pformat
    from textwrap import indent
    for name in globals():
        if name.startswith('somefunc_'):
            print("\n{}():".format(name))
            print(indent(pformat(globals()[name]()), ' '*4))


if __name__ == '__main__':
    main()
