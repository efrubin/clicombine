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

import glob
import os
import drivecasa
import utils
import additional_casa_commands


def drive(param_dict, clargs):
    """
    Drive the combination process.  This entails generating code for
    use in the casa interpreter and then running it.
    """
    output_basename = _gen_basename(param_dict, clargs)

    if not clargs.overwrite:
        i = 1
        while glob.glob('*{}*'.format(output_basename)):
            output_basename = '{}.{}'.format(
                _gen_basename(param_dict, clargs), i)
            i += 1

    casa_instance = drivecasa.Casapy()

    if param_dict['produce_uv']:
        _drive_uv(param_dict, clargs, output_basename, casa_instance)

    if param_dict['produce_feather']:
        _drive_feather(param_dict, clargs, output_basename, casa_instance)


def _drive_uv(param_dict, clargs, output_basename, casa_instance):
    """Drive the UV plane combination.  Functionally, this means
        * Performing concatenation
        * Cleaning the concatenated MS in the UV plane
        * Imaging the concatenated MS
    """

    script = []

    if glob.glob('{}.concat.ms'.format(output_basename)) and clargs.overwrite:
        os.system('rm -rf {}.concat.ms'.format(output_basename))

    # casa_instance.run_script(script)
    # todo
    # write an extension of the drivecasa command for imstat, which will let
    # us do the imstat work to do the inference for clean params.

    # perform concatenation

    if not glob.glob('{}.concat.ms'):
        concat_vis = drivecasa.commands.reduction.concat(script,
                                                         [
                                                             param_dict[
                                                                 'twelve_meter_filename'],
                                                             param_dict[
                                                                 'seven_meter_filename']
                                                         ],
                                                         out_path='./{}.concat.ms'.
                                                         format(output_basename))

    # clean + image
    thresh, clean_args = utils.param_dict_to_clean_input(
        param_dict, seven_meter=False)

    clean_args.update(
        {'spw': str(param_dict['seven_meter_spw'] + ',' + param_dict['twelve_meter_spw'])})
    clean_image = drivecasa.commands.clean(
        script,
        concat_vis,
        niter=10000,
        threshold_in_jy=thresh,
        other_clean_args=clean_args)

    if param_dict['moments']:
        for moment in param_dict['moments']:
            _ = additional_casa_commands.immoments(
                script, clean_image.image, clean_image.image, moment)
    if clargs.verbose:
        utils.eprint(script)
    _ = casa_instance.run_script(script, timeout=None)

    if clargs.verbose:
        utils.eprint("Data products present in {}".format(clean_image))


def _drive_feather(param_dict, clargs, output_basename, casa_instance):
    """Drive the feather combination.  Functionally, this means
        * Cleaning the individual ms separately.
        * Imaging the individual ms.
        * Feathering the two together.
    """

    # todo later -> the imstat stuff

    script = []

    thresh, seven_meter_clean_args = utils.param_dict_to_clean_input(
        param_dict, seven_meter=True)

    _, twelve_meter_clean_args = utils.param_dict_to_clean_input(
        param_dict, seven_meter=False)

    if clargs.verbose:
        utils.eprint('Seven meter clean args {}'.format(
            seven_meter_clean_args))
        utils.eprint('Twelve meter clean args {}'.format(
            twelve_meter_clean_args))
        utils.eprint('Running individual cleaning...')

    seven_meter_cleaned = drivecasa.commands.reduction.clean(
        script,
        niter=10000,
        vis_paths=param_dict['seven_meter_filename'],
        threshold_in_jy=thresh,
        other_clean_args=seven_meter_clean_args,
        out_path=os.path.abspath(output_basename))

    twelve_meter_cleaned = drivecasa.commands.reduction.clean(
        script,
        niter=10000,
        vis_paths=param_dict['twelve_meter_filename'],
        threshold_in_jy=thresh,
        other_clean_args=twelve_meter_clean_args,
        out_path=os.path.abspath(output_basename))

    _ = casa_instance.run_script(script, timeout=None)

    if clargs.verbose:
        utils.eprint('Individual cleanings complete.  Now feathering.')

    script = []

    feathered_image = additional_casa_commands.feather(script,
                                                       output_basename=output_basename,
                                                       highres=twelve_meter_cleaned.image,
                                                       lowres=seven_meter_cleaned.image,
                                                       weighting=_calc_feather_weighting(param_dict))
    if clargs.verbose:
        utils.eprint("Feather script")
        utils.eprint(script)

    _ = casa_instance.run_script(script, timeout=None)

    script = []
    if param_dict['moments']:
        for moment in param_dict['moments']:
            _ = additional_casa_commands.immoments(
                script, feathered_image, feathered_image, moment)

    if clargs.verbose:
        utils.eprint("Moments")
        utils.eprint(script)
    _ = casa_instance.run_script(script, timeout=None)


def _calc_feather_weighting(param_dict):
    weightings = param_dict['weightings']

    if not isinstance(weightings, (list, tuple)):
        return 1.0

    return float(weightings[1]) / float(weightings[0])


def _gen_basename(param_dict, clargs):
    if param_dict['output_basename'] in ['', 'auto']:
        return clargs.input_fname.lower().split('.json')[0]

    else:
        return param_dict['output_basename']
