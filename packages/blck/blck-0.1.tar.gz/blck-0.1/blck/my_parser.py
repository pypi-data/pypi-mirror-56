import argparse
import sys


class CustomFormatter(argparse.RawDescriptionHelpFormatter,
                      argparse.ArgumentDefaultsHelpFormatter):
    pass


def parse_args(args=sys.argv[1:]):
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        description=sys.modules[__name__].__doc__,
        formatter_class=CustomFormatter)

    g = parser.add_argument('-p', '--port', type=int, default=5000, help="Start a server to interact with the blockchain at the specified port ")
    #g.add_argument("--fizz", metavar="N",
    #               default=3,
    #               type=int,
    #               help="Modulo value for fizz")
    #g.add_argument("--buzz", metavar="N",
    #               default=5,
    #               type=int,
    #               help="Modulo value for buzz")
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--debug", "-d", action="store_true",
               default=False,
               help="enable debugging")
    g.add_argument("--silent", "-s", action="store_true",
               default=False,
               help="don't log to console")

    #parser.add_argument("start", type=int, help="Start value")
    #parser.add_argument("end", type=int, help="End value")

    return parser.parse_args(args)