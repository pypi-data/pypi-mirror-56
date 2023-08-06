__all__ = [
    'cell_type',
    'is_code_cell',

    'itercells'
]


def cell_type(cell):
    """
    Get the cell type:

    Args:
        cell (dict):    The cell as a dictionary

    Returns:
        str|None:    The name of the cell or None if the given cell is empty

    """
    if cell:
        return cell.get('cell_type', None)


def is_code_cell(cell):
    """
    Checks if the given cell is a code cell.

    Args:
        cell (dict):    The cell as a dictionary

    Returns:

    """
    return cell_type(cell) == 'code'


def itercells(content):
    """
    Iterator to the jupyter notebook cells

    Args:
        content (dict): The jupyter notebook content

    Yields:
        int, dict:  Index of the cell and the cell content
    """

    for idx, cell in enumerate(content['cells']):
        yield idx, cell
