'''onemillion CLI'''

# local import
from .onemillion import OneMillion


def main():
    '''onemillion CLI main command.'''
    import argparse

    parser = argparse.ArgumentParser(
        prog='onemillion',
        description='Determine if host in one million domain list')

    # TODO: enable version
    # parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('domain', nargs=1, help='host')

    # parser.add_argument('-u', '--update', default=False, action='store_true',
    #                     help='force fetch the latest TLD definitions')
    # parser.add_argument('-c', '--cache_file',
    #                     help='use an alternate TLD definition file')
    # parser.add_argument('-p', '--private_domains', default=False, action='store_true',
    #                     help='Include private domains')

    args = parser.parse_args()
    one_million = OneMillion()

    # if args.cache_file:
    #     tld_extract.cache_file = args.cache_file

    # if args.update:
    #     tld_extract.update(True)
    # elif len(args.input) is 0:
    #     parser.print_usage()
    #     exit(1)

    for i in args.input:
        print(' '.join(tld_extract(i)))  # pylint: disable=superfluous-parens
