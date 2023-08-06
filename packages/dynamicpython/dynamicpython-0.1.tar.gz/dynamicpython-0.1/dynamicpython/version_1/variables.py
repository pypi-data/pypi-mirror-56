def variable_set(variable_value: str, type: str, **kwargs) -> any:
    if type == 'Array':
        variable_value = variable_value.split(kwargs['delimiter'])
    return variable_value
