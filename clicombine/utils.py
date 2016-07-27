from __future__ import print_function
import os
import sys


def output_to_file(script, output_basename):
    """ 
    @param script a list of strings
    @param output_basename a base for a filename
    returns void
    IO
    """
    with open(os.path.abspath('{}.genscript.py'.format(output_basename)), 'a') as f:
        for command in script:
            print(command, file=f)


def param_dict_to_clean_input(param_dict, seven_meter):
    """Convert a param dict into input appropriately formatted for casa's
       'clean' task."""

    thresh = to_jansky(param_dict['thresh'])

    clean_input = {}

    # using str() because casa breaks when given unicode string literals
    # in the generated code, i.e. an input like **{'cell': u'0.0145arcsec'}
    # does not work, but **{'cell' : '0.0145arcsec'} does.
    clean_input.update({
        'mode': str(param_dict['mode']),
        'imagermode': str(param_dict['imagermode']),
        'spw': str(param_dict['seven_meter_spw']) if
        seven_meter else str(param_dict['twelve_meter_spw']),
        'field': str(param_dict['field']),
        'outframe': str(param_dict['outframe']),
        'imsize': param_dict['seven_meter_imsize'] if
        seven_meter else param_dict['twelve_meter_imsize'],
        'cell': str(param_dict['seven_meter_cell']) if
        seven_meter else str(param_dict['twelve_meter_cell']),
        'phasecenter': str(param_dict['phasecenter']),
        'robust': numberify(param_dict['robust']),
        'restfreq': str(param_dict['restfreq']),
        'start': str(param_dict['start']),
        'width': str(param_dict['width']),
        'nchan': (param_dict['nchan'])
    })

    return thresh, clean_input


def castable(value, typename):
    """Can value be cast as type typename without throwing an exception?"""
    try:
        typename(value)
        return True
    except Exception:
        return False


def numberify(non_numeric_string):
    if non_numeric_string == '':
        return ''
    if isinstance(non_numeric_string, (int, float)):
        return non_numeric_string
    if isinstance(non_numeric_string, str):
        return float(''.join((c for c in non_numeric_string if c in '0123456789.')))


def to_jansky(thresh):
    if (isinstance(thresh, float)):
        return thresh

    if (isinstance(thresh, int)):
        return thresh

    if 'mjy' in thresh.lower():
        return float(thresh.lower().strip('mjy')) / 1000.

    if 'jy' in thresh.lower():
        return float(thresh.lower().strip('jy'))

    else:
        return 1.0


def config_name_from_input_name(input_fname):
    if '.json' in input_fname:
        return input_fname
    return input_fname + '.json'


def levenshtein(s1, s2):
    """
    source:
    https: // en.wikibooks.org / wiki / Algorithm_Implementation
    / Strings / Levenshtein_distance
    """
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # j+1 instead of j since previous_row and current_row are one
            # character longer
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def color_string(string, color_arg, bold=False, underline=False):
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    c = color_arg[0].lower()
    if c == 'p':
        color = PURPLE
    elif c == 'b':
        color = BLUE
    elif c == 'y':
        color = YELLOW
    elif c == 'g':
        color = GREEN
    elif c == 'r':
        color = RED
    else:
        color = ''

    b = BOLD if bold else ''
    u = UNDERLINE if underline else ''

    return b + u + color + string + ENDC


def eprint(*args, **kwargs):
    """Print to stderr. """
    print(*args, file=sys.stderr, **kwargs)
