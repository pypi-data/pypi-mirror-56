import sys

from .__about__ import __copyright__, __version__


def show(argv=None):
    # Parse command line arguments.
    parser = _get_parser()
    args = parser.parse_args(argv)

    print(args.number)
    return


def _get_parser():
    import argparse

    parser = argparse.ArgumentParser(
        description=("Dummy pyfoobar executable."),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("number", type=int, help="number to show")

    version_text = "\n".join(
        [
            "pyfoobar {} [Python {}.{}.{}]".format(
                __version__,
                sys.version_info.major,
                sys.version_info.minor,
                sys.version_info.micro,
            ),
            __copyright__,
        ]
    )
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=version_text,
        help="display version information",
    )

    return parser
