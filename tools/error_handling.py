def attribute_err(stat_name):
    raise Exception(f'No such attribute named "{stat_name}"')

def check_index_err(x, y, name):
    if x < 0 or y < 0: # negative index case
        raise Exception(f'Index of ({x}, {y}) is negative\nObject: {name}')
    else: # beyond UI boundaries case
        raise Exception(f'Index of ({x}, {y}) is beyond the UI limit\nObject: {name}')