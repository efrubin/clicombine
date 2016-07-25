# cli.py
# author: Elias Rubin
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
Entrance to cli-combine application.  Set up the argument parser and dispatch
commands.
"""

import argparse
import commands


def entry():
    """
    Set up the parser.  Logically, there is only one parser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("input_fname",
                        help="The name of your configuration file.",
                        type=str,
                        nargs="?")

    parser.add_argument("-v", "--verbose",
                        help="Increase output verbosity.  Log to stderr.",
                        action="store_true")
    parser.add_argument("-o", "--overwrite",
                        help="Overwrite old combined images and create"
                        " new ones with the same filename.",
                        action="store_true")

    parser.add_argument("-r", "--raw",
                        help="Disable error checking of the configuration file which allows you"
                        " to pass arbitrary input to the clean task."
                        " Only use this option if you know what you're doing.",
                        action="store_true")

    group = parser.add_mutually_exclusive_group()
    group.set_defaults(mode="combine")
    group.add_argument("-e", "--example",
                       help="Create an example config file.",
                       action="store_const",
                       dest='mode',
                       const='example')

    group.add_argument("-n", "--new",
                       help="Create an empty config file.",
                       action="store_const",
                       dest='mode',
                       const='new')

    group.add_argument("-c", "--combine",
                       help="Combine images as specified in the config file."
                       " Default to true.",
                       action="store_const",
                       dest='mode',
                       const='combine')
    args = parser.parse_args()

# the parser should fail on combine and new without a filename
    if args.mode in ['combine', 'new'] and (not args.input_fname):
        parser.error("can't --{} without a filename argument".format(
            args.mode))

    _dispatch(args)


def _dispatch(args):
    """
    Dispatch arguments
    """
    if args.mode == 'combine':
        commands.combine(args)
    elif args.mode == 'new':
        commands.new(args)
    elif args.mode == 'example':
        commands.example(args)
if __name__ == "__main__":
    entry()
