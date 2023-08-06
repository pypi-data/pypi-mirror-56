#!/usr/bin/env python3

import os
import shutil
import glob
import sys
import subprocess

################################

LOCAL_BASH = '~/.bashrc'
BACKUP_BASH = '~/.bashrc.bak'

FULL_PATH_BASH = os.path.expanduser(LOCAL_BASH)
FULL_PATH_BASH_BAK = os.path.expanduser(BACKUP_BASH)

PKG_DIR = os.path.abspath(os.path.dirname(__file__))
PYPATH_DIR = os.path.dirname(PKG_DIR)


PYGFUNC_F90_FILE = "lib/pygfunc.f90"
PYGFUNC_PYF_FILE = "lib/pygfunc.pyf"
WRITE_DATA_PHANTOM_F90_FILE = "lib/write_data_phantom.f90"


subprocess.run("pip3 install -r requirements.txt --user", shell=True)

# install fortran locally
subprocess.run('./install_phantom.sh', shell=True)

python_path = os.environ.get('PYTHONPATH') or ''
python_paths = [os.path.abspath(path) for path in python_path.split(':')]

pypath = None
if PYPATH_DIR not in python_paths:
    print("{} not in PYTHONPATH, needed for local development of MESA2HYDRO"
          .format(PYPATH_DIR))
    print("Appending {} to PYTHONPATH in {}".format(PYPATH_DIR, FULL_PATH_BASH))
    pypath = 'export PYTHONPATH=$PYTHONPATH:{}\n'.format(PYPATH_DIR)

root_path = os.environ.get('MESA2HYDRO_ROOT')
root_export = None
if not root_path:
    print("Setting MESA2HYDRO_ROOT path to {}. To update change in {}"
          .format(PKG_DIR, FULL_PATH_BASH))
    root_export = 'export MESA2HYDRO_ROOT={}\n'.format(PKG_DIR)

if pypath or root_export:
    shutil.copyfile(FULL_PATH_BASH, FULL_PATH_BASH_BAK)
    with open(FULL_PATH_BASH, 'a') as f:
        f.write('# ADDED BY MESA2HYDRO FOR LOCAL DEVELOPMENT\n')
        if pypath:
            f.write(pypath)
        if root_export:
            f.write("# MODIFY TO CHANGE DEFAULT DATA PATH IN MESA2HYDRO\n")
            f.write(root_export)

    print("Restart your terminal to complete local installation")

so_files = glob.glob(os.path.join(PKG_DIR, 'lib/*pygfunc.cpython-*.so'))
if len(so_files) == 1:
    file_name = os.path.basename(so_files[0])
    shutil.copyfile(so_files[0], os.path.join(PKG_DIR, 'work', file_name))


