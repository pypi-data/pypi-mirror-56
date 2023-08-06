
from dictvars import dictvars, varsnamed


def somefunc():
    a = '1'
    b = '2'
    c = '3'
    leak = b
    return dictvars(a, b)


print(somefunc())


def somefunc2():
    a = '1'
    b = '2'
    c = '3'
    no_leaks_now = b
    return dictvars(a, b=b)


print(somefunc2())


def somefunc3():
    a = '1'
    b = '2'
    c = '3'
    no_leaks_now = b
    return varsnamed('a', 'b')


print(somefunc3())
