#!/usr/bin/python3

import os
import sys
try:
    from topoly import import_coords, yamada, homfly, alexander, conway, \
        jones, yamada, blmho, kauffman_bracket, kauffman_polynomial, plot_matrix
    from graph import Graph

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


# with open('/Users/pawel/Downloads/2efv.pdb', 'r') as myfile:
# with open('/Users/pawel/Downloads/1aoc.pdb', 'r') as myfile:
# with open('/Users/pawel/PycharmProjects/topoly/structures/31.xyz', 'r') as myfile:
# with open('/Users/pawel/Downloads/1j85.pdb', 'r') as myfile:
# with open('/Users/pawel/Downloads/mathematica.xyz', 'r') as myfile:
with open('/Users/pawel/Desktop/73.txt', 'r') as myfile:
    data = myfile.read()
curve = import_coords(data)
print(curve)
print(alexander(curve, closure='closed', translate=True))



#     data = myfile.read()
#     curve = import_coords(data)
    # for arc in curve:
    #     print(arc)

# g = Graph(code)
# for key in g.abstract_graph:
#     print(key,g.abstract_graph[key])
# print(g.find_loops())
#     print('Alexander ', alexander(curve, closure_method='two_points', translate=True, matrix=True, tries=20))
    # print('Alexander ', alexander(curve, closure_method='two_points', translate=True, beg=6, end=15, tries=20))
    # print('Conway ' + str(k), conway(curve, closure_method='closed', translate=True))
    # print('Jones ' + str(k), jones(curve, closure_method='closed', translate=True))
    # print('HOMFLY ' + str(k), homfly(curve, closure_method='closed', translate=True))
    # print('Yamada ' + str(k), yamada(curve, closure_method='closed', translate=True))
    # print('BLM/Ho ' + str(k), blmho(curve, closure_method='closed', translate=True))
    # print('Kauffman bracket ' + str(k), kauffman_bracket(curve, closure_method='closed', translate=True))
    # print('Kauffman polynomial ' + str(k), kauffman_polynomial(curve, closure_method='closed', translate=True))
    # k += 1

