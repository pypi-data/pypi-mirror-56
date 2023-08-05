#!/usr/bin/python3

import os
import sys
try:
    from topoly import import_coords, yamada
except ImportError:
    # fragment needed if topoly is still not istalled
        build_dir_name = 'build'    # set as needed                                     #|
        dir_path = os.path.dirname(os.path.realpath(__file__))                          #|
        par_dir = os.path.abspath(os.path.join(dir_path, os.pardir))                    #|
        build_dir = os.path.abspath(os.path.join(par_dir, build_dir_name))              #|
        python_dir = os.path.abspath(os.path.join(par_dir, 'python'))                   #|
        os.environ['LD_LIBRARY_PATH'] = build_dir                                       #|
        os.environ['PYTHONPATH'] = ':'.join([build_dir, python_dir])                    #|
        os.execv(sys.executable, [sys.executable] + sys.argv)                           #|
    # until here



with open('sample_structures.csv', 'r') as myfile:
    k = 1
    for line in myfile.readlines():
        curve = import_coords(line)
        print('Structure ' + str(k), yamada(curve, closure_method='closed', translate=True))
        k += 1
