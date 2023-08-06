from .Expression import Expression

def Filter(**kwargs):
    if 'all' in kwargs:
        # and
        all = []
        for expression in kwargs.get('all'): all.append(Expression(**expression))
        return {
            'and': all
        }
    elif 'one' in kwargs:
        # or
        one = []
        for expression in kwargs.get('one'): one.append(Expression(**expression))
        return {
            'or': one
        }
    else:
        # expression
        return {
            'expression': Expression(**kwargs)
        }
