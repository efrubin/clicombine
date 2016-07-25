"""
Additional commands using the same style as the drivecasa module.
"""
from drivecasa.utils import byteify


def feather(script, output_basename, highres, lowres, weighting):
    output_name = byteify('{}.feather'.format(output_basename))
    feather_args = {'imagename': output_name,
                    'highres': highres,
                    'lowres': lowres,
                    'sdfactor': weighting}

    script.append('feather(**{})'.format(repr(feather_args)))

    return output_name


def imstat(script, imagename, feature_name, feature_value):
    """
       Imstat displays statistical information from an image or image region.
    """

    imstat_args = {'imagename': imagename,
                   feature_name: feature_value}

    script.append('imstat(**{})'.format(repr(imstat_args)))

    return
