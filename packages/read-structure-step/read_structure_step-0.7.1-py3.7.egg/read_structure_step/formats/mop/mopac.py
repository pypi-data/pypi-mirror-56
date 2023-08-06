import seamm
import os

mopac_error_identifiers = []


def run_mopac(file_name):

    if os.path.isdir('/opt/mopac/'):
        mopac_path = '/opt/mopac/'
    else:
        try:
            mopac_path = os.path.split(os.environ['mopac'])[0]
        except KeyError:
            mopac_path = os.environ['MOPAC_LICENSE']
        except KeyError:
            raise FileNotFoundError('The MOPAC executable could not be found')

        mopac_exe = mopac_path + 'MOPAC2016.exe'

        local = seamm.ExecLocal()

        local.run(cmd=[mopac_exe, file_name])
