# combineparser.py
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

import glob
import utils
import sys
import os
import json

ALLOWED_KEYS = {
    'twelve_meter_filename',
    'seven_meter_filename',
    'output_basename',
    'weightings',
    'mode',
    'imagermode',
    'spw',
    'field',
    'outframe',
    'seven_meter_imsize',
    'twelve_meter_imsize',
    'seven_meter_cell',
    'twelve_meter_cell',
    'phasecenter',
    'robust',
    'restfreq',
    'start',
    'width',
    'nchan',
    'thresh',
    'produce_feather',
    'produce_uv',
    'moments'
}


def parse(config_fname, clargs):
    error_occured = False
    if not os.path.exists(config_fname):
        utils.eprint("{} no such file '{}'".format(
            utils.color_string("Error:", 'red', bold=True),
            utils.color_string(config_fname, 'red', bold=True)))
        sys.exit(0)

    with open(config_fname, mode='r') as f:
        param_dict = json.load(f)

    if not clargs.raw:
        for k, v in param_dict.iteritems():

            if k not in ALLOWED_KEYS:
                parse_error(utils.color_string("{} : {}".format(k, v), 'p'), k,
                            config_fname, expected=closest_legal(k, ALLOWED_KEYS))
                error_occured = True
                continue

            if not legal_value_for_key(k, v, param_dict):
                error_occured = True
                continue

            # TODO
            # units = parse_units(k, v)

            # if units not in ALLOWED_UNITS[k]:
            #     parse_error("{} : {}".format(k, v), units, config_fname,
            #                 expected=closest_legal(units, ALLOWED_UNITS[k]))
            #     error_occured = True

    if error_occured:
        sys.exit(0)

    return param_dict


def legal_value_for_key(key, value, param_dict):
    """Determine if the value is a legal value for the key, given the conditions
    of param_dict."""

    if param_dict['mode'] == 'channel':
        if key == 'start' and not utils.castable(value, int):
            utils.eprint("{} Mode channel requires integer value for 'start'".format(
                utils.color_string("Error:", 'red', bold=True)))
            return False

        if key == 'width' and not utils.castable(value, int):
            utils.eprint("{} Mode channel requires integer value for 'width'".format(
                utils.color_string("Error:", 'red', bold=True)))
            return False

    if key == 'nchan' and not utils.castable(value, int):
        return False

    if 'imsize' in key and not utils.castable(value, list):
        if not utils.castable(value, int):
            return False

    if key == 'thresh' and not utils.castable(value, float) and 'jy' not in value.lower():
        utils.eprint("{} key 'thresh' must be numeric or in [m]jy.".format(
            utils.color_string("Error:", 'red', bold=True)))
        return False

    if key == 'robust' and not utils.castable(value, float):
        utils.eprint("{} key 'robust' must be of type float".format(
            utils.color_string("Error:", 'red', bold=True)))
        return False

    if key == 'moments' and not utils.castable(value, list):
        utils.eprint('{} key "moments" must be of type list<int>'.format(
            utils.color_string("Error:", 'red', bold=True)))
        return False

    if key == 'seven_meter_filename' and not glob.glob(value):
        utils.eprint('{} no file of name {} present'.format(
            utils.color_string("Error:", 'red', bold=True), value))
        return False

    if key == 'twelve_meter_filename' and not glob.glob(value):
        utils.eprint('{} no file of name {} present'.format(
            utils.color_string("Error:", 'red', bold=True), value))
        return False

    return True


def closest_legal(illegal_string, legal_collection, metric=utils.levenshtein):
    """ Find the closest string (as determined by metric) to
        illegal_string in legal_collection """

    return sorted([(metric(illegal_string, legal_string), legal_string)
                   for legal_string in legal_collection],
                  key=lambda x: x[0])[0][1]


def parse_error(line, problem, fname, linenum=None, expected=None):

    if linenum and expected:
        error_string = """{} you wrote '{}' at {}:{}.
        We had trouble parsing '{}'.  Did you mean '{}'?""".format(
            utils.color_string("Error:", 'red', bold=True),
            line, fname, linenum,
            utils.color_string(problem, 'red'),
            utils.color_string(expected, 'blue'))

    elif linenum:
        error_string = """{} you wrote '{}' at {}:{}.
            We had trouble parsing '{}'.""".format(
            utils.color_string("Error:", 'red', bold=True),
            line, fname, linenum,
            utils.color_string(problem, 'red'))

    elif expected:
        error_string = """{} you wrote '{}' in {}.  We had trouble parsing
        '{}'.  Did you mean '{}'?""".format(
            utils.color_string("Error:", 'red', bold=True),
            line, fname,
            utils.color_string(problem, 'red'),
            utils.color_string(expected, 'blue'))
    else:
        error_string = """{} you wrote '{}' in {}.  We had trouble parsing
        '{}'.""".format(
            utils.color_string("Error:", 'red', bold=True),
            line, fname, utils.color_string(problem, 'red'))

    utils.eprint(error_string)
