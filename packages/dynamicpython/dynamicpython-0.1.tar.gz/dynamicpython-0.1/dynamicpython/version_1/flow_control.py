def for_each(iterable_input: iter) -> any:
    for index, current_item in enumerate(iterable_input):
        yield index, current_item
