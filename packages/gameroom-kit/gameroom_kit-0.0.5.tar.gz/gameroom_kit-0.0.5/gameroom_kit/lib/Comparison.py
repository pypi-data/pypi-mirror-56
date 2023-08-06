def Comparison(s):
    if (s == '=' or s == '==' or s == 'equal to' or s == 'equal_to'): return 'equal_to'
    if (s == '!=' or s == 'not equal to' or s == 'not_equal_to'): return 'not_equal_to'
    if (s == '>' or s == 'greater than' or s == 'greater_than'): return 'greater_than'
    if (s == '>=' or s == 'greater than or equal to' or s == 'greater_than_or_equal_to'): return 'greater_than_or_equal_to'
    if (s == '<' or s == 'less than' or s == 'less_than'): return 'less_than'
    if (s == '<=' or s == 'less than or equal to' or s == 'less_than_or_equal_to'): return 'less_than_or_equal_to'
    if (s == 'contains'): return 'contains'
    if (s == '~' or s == 'like'): return 'like'
    if (s == 'inside' or s == 'in'): return 'in'
    if (s == 'search'): return 'search'
    # default
    raise Exception(f'comparison not found for {s}')
