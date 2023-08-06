from argparse import ArgumentParser
from sys import argv, stdout

from ipwg import Generator


def get_opts():
    args = ArgumentParser(description="Generate random passwords")
    args.add_argument(
        "-n",
        help="Do not add a new-line character at the end of the output",
        action="store_true")
    args.add_argument(
        "-a",
        "--alpha",
        help="Include at least 1 alpha character",
        action="store_true")
    args.add_argument(
        "-u",
        "--upper",
        help="Include at least 1 upper case alpha character",
        action="store_true")
    args.add_argument(
        "-d",
        "--digit",
        help="Include at least 1 digit",
        action="store_true")
    args.add_argument(
        "-s",
        "--special",
        help="Include at least 1 special",
        action="store_true")
    args.add_argument(
        "length",
        help="The length of the password",
        type=int,
        default=10)
    opts = args.parse_args(argv[1:])
    if not any([opts.alpha, opts.digit, opts.special, opts.upper]):
        opts.alpha = True
        opts.upper = True
        opts.digit = True
    return opts


def main():
    opts = get_opts()
    g = Generator()
    g.lowers_enabled = 1 if opts.alpha else 0
    g.uppers_enabled = 1 if opts.upper else 0
    g.digits_enabled = 1 if opts.digit else 0
    g.specials_enabled = 1 if opts.special else 0
    pwd = g.create_password(opts.length)
    stdout.write(pwd)
    if not opts.n:
        stdout.write('\n')

