import argparse

from .cell import *
from .core import *
from .io import *


def entry_main():
    """
    Entry point for image renaming
    """
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--file', help="Path to jupyter notebook", required=True)
    arg_parser.add_argument('--destination', help="Path to new jupyter notebook", required=False, default=None)
    arg_parser.add_argument('--clear-field', help="Clear the cell fields of the notebook (by default 'outputs')",
                            required=False, default="outputs")
    arg_parser.add_argument('--clear-value', help="The value to set the output fields to (by default [])",
                            required=False, default=[])

    args = arg_parser.parse_args()

    # load the file content
    path, content = load(args.file)

    new_content = None

    # clear output if specified
    if args.clear_output:
        new_content = clear_field(content, field=args.clear_field, clear_value=args.clear_value)

    if new_content:
        destination = path
        if args.destination is not None:
            destination = args.destination
        else:
            logging.info('Will overwrite the content of the jupyter notebook')
        save(new_content, destination)
