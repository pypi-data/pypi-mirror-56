#


""" Command line interface
"""


import argparse
import logging

from . import _meta
from . import _core


def main():
    """ CLI main function
    """
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    #
    parser = argparse.ArgumentParser(
        allow_abbrev=False,
    )
    parser.add_argument('--version', action='version', version=_meta.VERSION)
    parser.add_argument('directory', default='.venv', nargs='?')
    #
    args = parser.parse_args()
    logger.info("Arguments %s", args)
    #
    _core.main(args.directory)


# EOF
