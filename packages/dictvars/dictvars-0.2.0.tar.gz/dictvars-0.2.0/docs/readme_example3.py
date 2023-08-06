
from dictvars import dictvars, varsnamed


myapp = 'MyApp'  # global var


def somefunc_dictvars(current_user):
    form = dict(some='very', complex_='expression')
    comments = ['bla', 'bla']

    return dictvars(form, comments, app=myapp, user=current_user)


if __name__ == '__main__':
    from pprint import pprint
    pprint(somefunc_dictvars('John Do'))
