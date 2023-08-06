"""
Implementation of the reader for XYZ files using OpenBabel
"""

import os
import seamm
import seamm_util
from read_structure_step.errors import MopError
from read_structure_step.formats.registries import register_reader
from ..which import which
from .mopac import run_mopac

obabel_error_identifiers = ['0 molecules converted']


@register_reader('.mop')
def load_mop(file_name):

    try:

        obabel_exe = which('obabel')
        local = seamm.ExecLocal()

        result = local.run(
            cmd=[
                obabel_exe, '-f 1', '-l 1', '-imop', file_name, '-omol', '-x3'
            ]
        )
        for each_error in obabel_error_identifiers:
            if each_error in result['stderr']:
                raise MopError(
                    'OpenBabel: Could not read input file. %s' % result
                )

        mol = result['stdout']

        structure = seamm_util.molfile.to_seamm(mol)

        return structure

    except MopError:

        run_mopac(file_name)

        output_file = os.path.splitext(file_name)[0] + '.out'

        obabel_exe = which('obabel')
        local = seamm.ExecLocal()

        result = local.run(
            cmd=[
                obabel_exe, '-f 1', '-l 1', '-imoo', output_file, '-omol',
                '-x3'
            ]
        )

        for each_error in obabel_error_identifiers:
            if each_error in result['stderr']:
                raise MopError(
                    'OpenBabel: Could not read input file. %s' % result
                )

        mol = result['stdout']

        structure = seamm_util.molfile.to_seamm(mol)

        return structure
