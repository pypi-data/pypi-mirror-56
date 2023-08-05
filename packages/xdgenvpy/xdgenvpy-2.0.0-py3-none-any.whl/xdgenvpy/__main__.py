#!/usr/bin/env python3

from argparse import ArgumentParser
from logging import Formatter
from logging import StreamHandler
from logging import WARNING
from logging import getLogger
from sys import stderr

import pkg_resources

from xdgenvpy import XDG
from xdgenvpy import XDGPackage

LOG = None


def setup_logger(level=None):
    """
    Sets up a basic logger, mainly used for warning and error messages.  These
    messages will be sent to the process' stderr.  Actual XDG output will be
    written to stdout.

    :param int level: The minimum log level.
    """
    if not level:
        level = WARNING
    formatter = Formatter('%(levelname)s %(message)s')
    handler = StreamHandler(stderr)
    handler.setFormatter(formatter)
    logger = getLogger()
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


def get_version_str():
    return '%(prog)s ' + pkg_resources.require('xdgenvpy')[0].version


def parse_args():
    """
    Parses the process' command line arguments and returns a simple plain-old
    data object.

    :rtype: object
    :return: Plain old data object representing the CLI arguments.
    """
    parser = ArgumentParser(prog='xdg',
                            description='Print XDG Base Directories.')
    parser.add_argument('-V',
                        '--version',
                        action='version',
                        version=get_version_str())
    parser.add_argument('variables',
                        metavar='XDG_VAR',
                        type=str,
                        nargs='*',
                        help='The XDG Base Directory variable to print.')
    parser.add_argument('-p',
                        '--package',
                        dest='package',
                        help='Optional package name.')
    return parser.parse_args()


def get_xdg(package):
    """
    Gets an :class:`XDG` instance based on whether or not a package name was
    specified.  If a package name is specified then it will be incorporated into
    the directory values returned from the :class:`XDG` object.

    :param str package: Optional package name.

    :rtype: XDG|XDGPackage
    :return: Returns an XDG object.
    """
    if package:
        xdg = XDGPackage(package)
    else:
        xdg = XDG()
    return xdg


def print_vars(xdg, variables):
    """
    Prints each of the specified XDG variables.  Note that each variable
    specified must be a valid XDG variable, also enumerated in the dictionary
    :code:`XDG_TO_METHOD_MAPPING`.

    For each XDG variable, the associated value will be printed onto separate
    lines on stdout.  Note that logs will be written to stderr, so you may need
    shell-foo to redirect stdout or stderr to different destinations.

    :param XDG xdg: The XDG object to calculate base directories from.
    :param list variables: A sequence of XDG variables to print.
    """
    for var in variables:
        if not (str(var).startswith('XDG_') and hasattr(xdg, var)):
            LOG.error('Invalid XDG variable: %s', var)
        else:
            value = getattr(xdg, var)
            if isinstance(value, str):
                print(value)
            elif isinstance(value, tuple):
                print(':'.join(value))
            else:
                LOG.error('Unexpected type for XDG variable: %s = %s',
                          var,
                          value)


def main():
    """The main entry point for this 'application'."""
    global LOG
    LOG = setup_logger()
    args = parse_args()
    xdg = get_xdg(args.package)
    print_vars(xdg, args.variables)


if __name__ == '__main__':
    main()
