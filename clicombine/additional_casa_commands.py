"""
Additional commands using the same style as the drivecasa module.
"""
import os
from drivecasa.utils import byteify


def feather(script, output_basename, highres, lowres, weighting):
    output_name = byteify('{}.feather'.format(output_basename))
    feather_args = {'imagename': os.path.abspath(output_name),
                    'highres': highres,
                    'lowres': lowres,
                    'sdfactor': weighting}

    script.append('feather(**{})'.format(repr(feather_args)))

    return output_name


def imstat(script, imagename, feature_name, feature_value):
    """
       Imstat displays statistical information from an image or image region.
    """

    imstat_args = {'imagename': os.path.abspath(imagename),
                   feature_name: feature_value}

    script.append('imstat(**{})'.format(repr(imstat_args)))

    return


def immoments(script, imagename, output_basename, moment, axis='spectral'):

    output_name = byteify('{}.moment{}'.format(output_basename, moment))
    immoments_args = {'imagename': imagename,
                      'moments': [moment],
                      'axis': axis,
                      'outfile': os.path.abspath(output_name)}

    script.append('immoments(**{})'.format(repr(immoments_args)))

    return output_name
