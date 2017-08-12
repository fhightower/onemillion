# -*- coding: utf-8 -*-

"""One Million.

Usage:
    onemillion <host> [--no-cache | --no-update | (-l <cache> | --cache_location=<cache>)]
    onemillion (-h | --help)
    onemillion --version

Options:
    -h --help     Show this screen.
    --version     Show version.
    --no-cache    Don't cache the top million domain lists
    --no-update   Don't update any cached domain lists
    -l <cache>, --cache_location=<cache>  Specify a cache location
"""

from docopt import docopt

from .__init__ import __version__ as VERSION
from .onemillion import OneMillion


def main(args=None):
    """Console script for onemillion"""
    arguments = docopt(__doc__, version=VERSION)

    # if there is a cache location, pass it into onemillion
    if arguments['--cache_location'] is not None:
        one_million = OneMillion(cache=(not arguments['--no-cache']), update=(not arguments['--no-update']), cache_location=arguments['--cache_location'])
    else:
        # if there is no cache location, use the default one and pass in the other values
        one_million = OneMillion(cache=(not arguments['--no-cache']), update=(not arguments['--no-update']))

    print(one_million.domain_in_million(arguments['<host>']))


if __name__ == "__main__":
    main()
