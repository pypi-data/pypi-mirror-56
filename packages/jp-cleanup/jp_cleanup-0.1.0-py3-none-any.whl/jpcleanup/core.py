from copy import deepcopy

from . import itercells, is_code_cell


# noinspection PyDefaultArgument
def clear_field(content, field='outputs', clear_value=[]):
    """
    Clear the output fields of the given jupyter notebook content file.

    Args:
        content (dict):     The jupyter notebook content.
        field (str):        The name of the field to clear (default is 'outputs').
        clear_value (any):  The value to set the field to (default is an empty list)

    Returns:
        list[dict]: The jupyter notebook content with cleared output fields.
    """

    # make a copy of the given content to replace the output fields
    c = deepcopy(content)

    for idx, cell_content in itercells(content):
        if is_code_cell(cell_content):
            # clear the content of the outputs field to the specified value
            c['cells'][idx][field] = clear_value

    return c


def reset_counters(content, value=0):
    """
    Reset the execution counter for each code cell.

    Args:
        content (dict):   The jupyter notebook content.
        value (int):      The execution counter to set (default is 0).

    Returns:
        dict:   The content with all execution counters set to the given number

    """
    # make a copy of the given content to replace the output fields
    c = deepcopy(content)

    for idx, cell_content in itercells(content):
        if is_code_cell(cell_content):
            c['cells'][idx]['execution_count'] = value

    return c
