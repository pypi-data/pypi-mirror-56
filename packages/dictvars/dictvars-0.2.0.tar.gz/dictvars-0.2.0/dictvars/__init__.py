
import inspect

__version__ = '0.2.0'

__all__ = ('dictvars', 'varsnamed', 'compact')


def _flatten(l):
    return (item for sublist in l for item in sublist)


def dictvars(*variables, **kw_variables):
    """Creates a dict with the variables passed as arguments.

    The keys of the dict are the inferred names of the variables passed
    as arguments, plus all keys passed as keyword arguments.
    """

    caller = inspect.stack()[1][0]
    nested_items = [caller.f_locals.items(), caller.f_globals.items()]

    vars = {}
    for name, var in _flatten(nested_items):
        for v in variables:
            if var is v:
                vars[name] = var
                break

    for name, var in kw_variables.items():
        vars[name] = var

    return vars


def varsnamed(*names):
    """Creates a dict from variables names passed as arguments.

    The keys of the dict are the variable names.

    If a variable is not found with the name passed, a NameError exception
    is raised.
    """

    caller = inspect.stack()[1][0]
    vars = {}
    for n in names:
        if n in caller.f_locals:
            vars[n] = caller.f_locals[n]
        elif n in caller.f_globals:
            vars[n] = caller.f_globals[n]
        else:
            raise NameError("name '{0}' is not defined".format(n))
    return vars


compact = varsnamed
