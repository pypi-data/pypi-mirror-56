import json

__all__ = [
    'load',
    'save'
]


def load(jupyter_file):
    """
    Open and load the specified jupyter notebook

    Args:
        jupyter_file (str): The path to the file

    Returns:
        str|str:    The path of the file and json-decoded content
    """

    if not jupyter_file.endswith('.ipynb'):
        jupyter_file += '.ipynb'

    with open(jupyter_file, 'r') as file:
        content = json.load(file)

    return jupyter_file, content


def save(content, file):
    """
    Save the jupyter notebook content to the given file

    Args:
        content (dict): The jupyter notebook content
        file (str):     Path of the file
    """
    if not file.endswith('.ipynb'):
        file += '.ipynb'

    with open(file, 'w') as f:
        json.dump(content, f)
