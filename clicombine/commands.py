# commands.py
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

import os
import sys
import pprint
import json
import combineparser
import combinedriver
from collections import OrderedDict
import utils


def example(clargs):
    # use OrderedDict for in-order printing  Kind of an ugly hack compared to
    # just writing a dict literal in Python but I would rather do this than try
    # and print RFC compliant JSON to a file.
    EXAMPLE_LITERAL = OrderedDict((
        ('twelve_meter_filename', 'SgrAstar_12m.contsub'),
        ('seven_meter_filename', 'SgrAstar_7m.contsub'),
        ('output_basename', 'auto'),
        ('weightings', (1.0, 1.0)),
        ('mode', 'channel'),
        ('imagermode', 'mosaic'),
        ('seven_meter_spw', '0,4,8'),
        ('twelve_meter_spw', '12'),
        ('field', '0~188'),
        ('outframe', 'lsrk'),
        ('seven_meter_imsize', 256),
        ('twelve_meter_imsize', 750),
        ('seven_meter_cell', '0.5arcsec'),
        ('twelve_meter_cell', '0.145arcsec'),
        ('phasecenter', 'J2000 17h45m40.3 -29d00m28'),
        ('robust', 0.5),
        ('restfreq', '354.505473Ghz'),
        ('start', '-200km/s'),
        ('width', '5.0km/s'),
        ('nchan', 80),
        ('thresh', '0.0145jy'),
        ('produce_feather', True),
        ('produce_uv', True),
        ('moments', '')
    ))

    config_fname = "example.json"

    if not clargs.overwrite:
        i = 1
        while os.path.exists(config_fname):
            config_fname = "example." + str(i) + ".json"
            i += 1

    if clargs.verbose:
        utils.eprint(
            "Writing an example config file to {}".format(config_fname))

    with open(config_fname, mode='w') as f:
        json.dump(EXAMPLE_LITERAL, f, indent=1)


def combine(clargs):
    config_fname = utils.config_name_from_input_name(clargs.input_fname)

    param_dict = combineparser.parse(config_fname, clargs)

    if clargs.verbose:
        pprint.pprint(param_dict, sys.stderr)

    combinedriver.drive(param_dict, clargs)


def new(clargs):
    NEW_LITERAL = OrderedDict((
        ('twelve_meter_filename', ''),
        ('seven_meter_filename', ''),
        ('output_basename', ''),
        ('weightings', (1.0, 1.0)),
        ('mode', ''),
        ('imagermode', ''),
        ('spw', ''),
        ('field', ''),
        ('outframe', ''),
        ('seven_meter_imsize', ''),
        ('twelve_meter_imsize', ''),
        ('seven_meter_cell', ''),
        ('twelve_meter_cell', ''),
        ('phasecenter', ''),
        ('robust', ''),
        ('restfreq', ''),
        ('start', ''),
        ('width', ''),
        ('nchan', ''),
        ('thresh', ''),
        ('produce_feather', True),
        ('produce_uv', True),
        ('moments', '')
    ))

    config_fname = utils.config_name_from_input_name(clargs.input_fname)
    i = 1

    if not clargs.overwrite:
        while os.path.exists(config_fname):
            config_fname = "{}.{}.json".format(
                clargs.input_fname.strip('.json'), i)
            i += 1

    with open(config_fname, mode='w+') as f:
        json.dump(NEW_LITERAL, f, indent=1)
