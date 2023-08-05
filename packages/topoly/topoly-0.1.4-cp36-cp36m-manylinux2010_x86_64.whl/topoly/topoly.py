#!/usr/bin/python3
"""
The main module collecting the functions designed for the users.

Pawel Dabrowski-Tumanski
p.dabrowski at cent.uw.edu.pl
04.09.2019

Docs:
https://realpython.com/documenting-python-code/#docstring-types

The type used here: Google


Support in PyCharm:
https://www.jetbrains.com/help/pycharm/settings-tools-python-integrated-tools.html
- change default reStructuredText to Google

Docs will be published in: https://readthedocs.org/

"""
closures = {"closed": 0, "mass_center": 1, "two_points": 2, "one_point": 3, "rays": 4}


import os
import sys
# the part needed if package not installed yet (to find libraries)                                  #|
build_dir_name = 'build'  # set as needed                                                           #|
if 'LD_LIBRARY_PATH' not in os.environ or build_dir_name not in os.environ['LD_LIBRARY_PATH']:      #|
    build_dir_name = 'build'    # set as needed                                                     #|
    dir_path = os.path.dirname(os.path.realpath(__file__))                                          #|
    par_dir = os.path.abspath(os.path.join(dir_path, os.pardir))                                    #|
    build_dir = os.path.abspath(os.path.join(par_dir, build_dir_name))                              #|
    if 'LD_LIBRARY_PATH' not in os.environ:                                                         #|
        os.environ['LD_LIBRARY_PATH'] = ''                                                          #|
    if 'PYTHONPATH' not in os.environ:                                                              #|
        os.environ['PYTHONPATH'] = ''                                                               #|
    os.environ['LD_LIBRARY_PATH'] = os.environ['LD_LIBRARY_PATH'] + ':' + build_dir                 #|
    os.environ['PYTHONPATH'] = os.environ['PYTHONPATH'] + ':' + build_dir                           #|
    os.execv(sys.executable, [sys.executable] + sys.argv)                                           #|
# until here                                                                                        #|
from manipulation import *
from invariants import *
from topoly_knot import *
from codes import *
from plotting import KnotMap, Reader




### invariants
def alexander(input_data,
           closure='two_points', tries=200, direction=0, reduce_method='kmt',
           poly_reduce=True, translate=False, beg=-1, end=-1, max_cross=15,
           matrix=False, density=1, level=0, matrix_plot=False, plot_ofile="KnotFingerPrintMap", plot_format="png",
           output_file='', cuda=True, debug=False):
    return calculate_invariant(input_data, 'alexander',
            closure=closure, tries=tries, direction=direction, reduce_method=reduce_method,
            poly_reduce=poly_reduce, translate=translate, beg=beg, end=end, max_cross=max_cross,
            matrix=matrix, density=density, level=level, matrix_plot=matrix_plot, plot_ofile=plot_ofile,
            plot_format=plot_format, output_file=output_file, cuda=cuda, debug=debug)

def conway(input_data,
           closure='two_points', tries=200, direction=0, reduce_method='kmt',
           poly_reduce=True, translate=False, beg=-1, end=-1, max_cross=15,
           matrix=False, density=1, level=0, matrix_plot=False, plot_ofile="KnotFingerPrintMap", plot_format="png",
           output_file='', cuda=True, debug=False):
    return calculate_invariant(input_data, 'conway',
            closure=closure, tries=tries, direction=direction, reduce_method=reduce_method,
            poly_reduce=poly_reduce, translate=translate, beg=beg, end=end, max_cross=max_cross, chirality=chirality,
            matrix=matrix, density=density, level=level, matrix_plot=matrix_plot, plot_ofile=plot_ofile,
            plot_format=plot_format, output_file=output_file, cuda=cuda, debug=debug)

def jones(input_data,
           closure='two_points', tries=200, direction=0, reduce_method='kmt',
           poly_reduce=True, translate=False, beg=-1, end=-1, max_cross=15, chirality=False,
           matrix=False, density=1, level=0, matrix_plot=False, plot_ofile="KnotFingerPrintMap", plot_format="png",
           output_file='', cuda=True, debug=False):
    return calculate_invariant(input_data, 'jones',
            closure=closure, tries=tries, direction=direction, reduce_method=reduce_method,
            poly_reduce=poly_reduce, translate=translate, beg=beg, end=end, max_cross=max_cross, chirality=chirality,
            matrix=matrix, density=density, level=level, matrix_plot=matrix_plot, plot_ofile=plot_ofile,
            plot_format=plot_format, output_file=output_file, cuda=cuda, debug=debug)

def homfly(input_data,
           closure='two_points', tries=200, direction=0, reduce_method='kmt',
           poly_reduce=True, translate=False, beg=-1, end=-1, max_cross=15, chirality=False,
           matrix=False, density=1, level=0, matrix_plot=False, plot_ofile="KnotFingerPrintMap", plot_format="png",
           output_file='', cuda=True, debug=False):
    return calculate_invariant(input_data, 'homfly',
            closure=closure, tries=tries, direction=direction, reduce_method=reduce_method,
            poly_reduce=poly_reduce, translate=translate, beg=beg, end=end, max_cross=max_cross, chirality=chirality,
            matrix=matrix, density=density, level=level, matrix_plot=matrix_plot, plot_ofile=plot_ofile,
            plot_format=plot_format, output_file=output_file, cuda=cuda, debug=debug)

def yamada(input_data,
           closure='two_points', tries=200, direction=0, reduce_method='kmt',
           poly_reduce=True, translate=False, beg=-1, end=-1, max_cross=15, chirality=False,
           matrix=False, density=1, level=0, matrix_plot=False, plot_ofile="KnotFingerPrintMap", plot_format="png",
           output_file='', cuda=True, debug=False):
    return calculate_invariant(input_data, 'yamada',
            closure=closure, tries=tries, direction=direction, reduce_method=reduce_method,
            poly_reduce=poly_reduce, translate=translate, beg=beg, end=end, max_cross=max_cross, chirality=chirality,
            matrix=matrix, density=density, level=level, matrix_plot=matrix_plot, plot_ofile=plot_ofile,
            plot_format=plot_format, output_file=output_file, cuda=cuda, debug=debug)

def kauffman_bracket(input_data,
           closure='two_points', tries=200, direction=0, reduce_method='kmt',
           poly_reduce=True, translate=False, beg=-1, end=-1, max_cross=15, chirality=False,
           matrix=False, density=1, level=0, matrix_plot=False, plot_ofile="KnotFingerPrintMap", plot_format="png",
           output_file='', cuda=True, debug=False):
    return calculate_invariant(input_data, 'kauffman_bracket',
            closure=closure, tries=tries, direction=direction, reduce_method=reduce_method,
            poly_reduce=poly_reduce, translate=translate, beg=beg, end=end, max_cross=max_cross, chirality=chirality,
            matrix=matrix, density=density, level=level, matrix_plot=matrix_plot, plot_ofile=plot_ofile,
            plot_format=plot_format, output_file=output_file, cuda=cuda, debug=debug)

def kauffman_polynomial(input_data,
           closure='two_points', tries=200, direction=0, reduce_method='kmt',
           poly_reduce=True, translate=False, beg=-1, end=-1, max_cross=15, chirality=False,
           matrix=False, density=1, level=0, matrix_plot=False, plot_ofile="KnotFingerPrintMap", plot_format="png",
           output_file='', cuda=True, debug=False):
    return calculate_invariant(input_data, 'kauffman_polynomial',
            closure=closure, tries=tries, direction=direction, reduce_method=reduce_method,
            poly_reduce=poly_reduce, translate=translate, beg=beg, end=end, max_cross=max_cross, chirality=chirality,
            matrix=matrix, density=density, level=level, matrix_plot=matrix_plot, plot_ofile=plot_ofile,
            plot_format=plot_format, output_file=output_file, cuda=cuda, debug=debug)

def blmho(input_data,
           closure='two_points', tries=200, direction=0, reduce_method='kmt',
           poly_reduce=True, translate=False, beg=-1, end=-1, max_cross=15, chirality=False,
           matrix=False, density=1, level=0, matrix_plot=False, plot_ofile="KnotFingerPrintMap", plot_format="png",
           output_file='', cuda=True, debug=False):
    return calculate_invariant(input_data, 'blmho',
            closure=closure, tries=tries, direction=direction, reduce_method=reduce_method,
            poly_reduce=poly_reduce, translate=translate, beg=beg, end=end, max_cross=max_cross, chirality=chirality,
            matrix=matrix, density=density, level=level, matrix_plot=matrix_plot, plot_ofile=plot_ofile,
            plot_format=plot_format, output_file=output_file, cuda=cuda, debug=debug)

def aps(input_data,
           closure='two_points', tries=200, direction=0, reduce_method='kmt',
           poly_reduce=True, translate=False, beg=-1, end=-1, max_cross=15, chirality=False,
           matrix=False, density=1, level=0, matrix_plot=False, plot_ofile="KnotFingerPrintMap", plot_format="png",
           output_file='', cuda=True, debug=False):
    return calculate_invariant(input_data, 'aps',
            closure=closure, tries=tries, direction=direction, reduce_method=reduce_method,
            poly_reduce=poly_reduce, translate=translate, beg=beg, end=end,  max_cross=max_cross, chirality=chirality,
            matrix=matrix, density=density, level=level, matrix_plot=matrix_plot, plot_ofile=plot_ofile,
            plot_format=plot_format, output_file=output_file, cuda=cuda, debug=debug)

def gln(input_data,
           closure='two_points', tries=200, direction=0, reduce_method='kmt',
           poly_reduce=True, translate=False, beg=-1, end=-1,
           matrix=False, density=1, level=0, matrix_plot=False, plot_ofile="KnotFingerPrintMap", plot_format="png",
           output_file='', cuda=True, debug=False):
    return calculate_invariant(input_data, 'gln',
            closure=closure, tries=tries, direction=direction, reduce_method=reduce_method,
            poly_reduce=poly_reduce, translate=translate, beg=beg, end=end,
            matrix=matrix, density=density, level=level, matrix_plot=matrix_plot, plot_ofile=plot_ofile,
            plot_format=plot_format, output_file=output_file, cuda=cuda, debug=debug)

def writhe(input_data,
           closure='two_points', tries=200, direction=0, reduce_method='kmt',
           poly_reduce=True, translate=False, beg=-1, end=-1,
           matrix=False, density=1, level=0, matrix_plot=False, plot_ofile="KnotFingerPrintMap", plot_format="png",
           output_file='', cuda=True, debug=False):
    return calculate_invariant(input_data, 'writhe',
            closure=closure, tries=tries, direction=direction, reduce_method=reduce_method,
            poly_reduce=poly_reduce, translate=translate, beg=beg, end=end,
            matrix=matrix, density=density, level=level, matrix_plot=matrix_plot, plot_ofile=plot_ofile,
            plot_format=plot_format, output_file=output_file, cuda=cuda, debug=debug)


### sampling
def generate_curve(n):
    return

def generate_loop(n, equilateral=False):
    return

def generate_lasso(loop,tail):
    return

def find_loops(curve):
    return

def find_thetas(curve):
    return

def find_handcuffs(curve):
    return

### surfaces
def make_surface(coordinates):
    return

def lasso_type(coordinates, bindex, eindex):
    # TODO add calculation of whole fingerprint
    return

def lasso_classify(coordinates, loop_indices):
    return

### translating/understanding
def translate(code, intype, outtype):
    return

def find_matching(data):
    return find_matching_structure(data)

### plotting
def plot_matrix(matrix, plot_ofile="KnotFingerPrintMap", plot_format="png", matrix_type="knot", circular=False,
                yamada=False, cutoff=0.48, debug=False):
    knotmap_data = Reader(matrix, cutoff=cutoff)
    unique_knots = knotmap_data.getUniqueKnots()
    knots_size = len(unique_knots)
    knotmap = KnotMap(patches=knots_size, protstart=knotmap_data.chainStart(), protlen=knotmap_data.chainEnd(),
                      rasterized=True, matrix_type=matrix_type)

    for e in unique_knots:
        d = knotmap_data.getKnot(e)
        knotmap.add_patch_new(d)
    knotmap.saveFilePng(plot_ofile + "." + plot_format)
    knotmap.close()
    return

def generate_coordinates(pdcode):
    return

def plot_graph(pdcode):
    return

### importing code/coordinates
def import_coords(input_data, format=None, pipe=False):
    available_formats = ['xyz', 'nxyz', 'list', 'pdb', 'mathematica']
    if format and format not in available_formats:
        raise AttributeError('The chosen format not supported (yet?). The available formats: ' + str(available_formats))
    if type(input_data) is str and (len(input_data.splitlines()) > 1 or '"' in input_data):
        pipe = True
    if pipe:
        data = input_data
    else:
        with open(input_data, 'r') as myfile:
            data = myfile.read()
    if not format:
        format = guess_format(data)
    structure = parse_data(data, format)
    return structure

def import_structure(name):
    return

def import_knot(name):
    return import_structure(name)

### structure manipulation
def reduce(curve, method, closed=True):
    return chain_reduce(curve, method, closed=closed)

def kmt(curve, closed=True):
    return chain_kmt(curve, closed)

def reidemeister(curve):
    return chain_reidemeister(curve)

def close_curve(curve):
    return

#### OLD VERSIONS ####
def alexander_old(curve, closure='two_points', tries=200, direction=0, reduce='kmt', beg=-1, end=-1, translate=False,
              poly_reduce=True, matrix=False, cuda=True, density=1, level=0, plot=False, plot_ofile="KnotFingerPrintMap",
              plot_format="png", output_file='', circular=False, debug=False):

    """Returns either the dictionary of Alexander polynomials/knot types with their probability for the chain delimited
    by beg/end (matrix=False), or the whole matrix of knot types for each subchain (matrix=True), or the status 0,
    if the output is directed to the output_file.

    Args:
        curve: the list of lists storing the coordinates of the chain, e.g curve = [[0,1.0,2.0,1.0],[1,1.0,2.7,3.0],[2,2.0,4,3.0],[3,0,-2.0,1.0]].
        closure: (string) the method of chain closure. Possible methods: 'two points' (default), 'one point', 'rays', 'mass_center, 'direction', and 'closed'.
        tries: (int) the number of closures for the probabilistic methods ('two points', 'one point', and 'rays').
        reduce: (string) the method of chain reduction. Possible methods: 'kmt', 'knot_pull', 'sono'.
        beg: (int) the starting bead of the subchain to be analyzed.
        end: (int) the last bead of the subchain to be analyzed.
        translate: (bool) if true, returns the knot type, if present in the library. If not, the polynomial is returned.
        poly_reduce: (bool) if true, the reduced version of the polynomial is printed. If false, the variables are written explicitly.
        matrix: (bool) if the analysis of each subchain has to be performed. The results are returned in the form of a matrix.
        cuda: (bool) use CUDA speedup if possible.
        density: (int)
        level: (int)
        plot: (bool) if true, the matrix of analysis of the subchains is plotted.
        plot_ofile: (string) the name of the file to store the plotted matrix.
        plot_format: (string) the format of the output file for the plot. Possible choices: png, svg.
        output_file: (string) the name of the output file. If empty, the result is directed to STDout.
        circular: (bool) if True, the circular matrix will be plotted.
        debug: (bool) the debugging mode.

        For the matrix calculation, the chain is always reduced with KMT and the knot types are printed (not
        polynomials). The knot types up to 8 crossings are stored. More complicated knots are "UNKNOWN".

    >>> curve = [[[0,1.0,2.0,1.0],[1,1.0,2.7,3.0],[2,2.0,4,3.0],[3,0,-2.0,1.0]]]
    >>> alexander(curve)
    '1'
    >>> alexander(curve, translate=True)
    '0_1'
    >>> alexander(curve, matrix=True)
    """
    if plot:
        matrix = True
    if len(curve) > 1:
        print("The Alexander polynomial is rather poor invariant for structures with more than one arc. "
              "Calculating the HOMFLY-PT polynomial instead.")
        return homfly(curve,closure=closure, tries=tries, direction=direction, reduce=reduce, translate=translate,
        poly_reduce=poly_reduce, matrix=matrix, density=density, level=level, plot=plot, plot_ofile=plot_ofile,
        plot_format=plot_format, output_file=output_file, debug=debug)

    c_in = curve[0]
    chain = coords2chain(c_in, beg, end)
    closure_int = closures[closure]

    if matrix:
        if cuda and check_cuda():
            if debug:
                print("CUDA detected and allowed, calculating whole fingerprint matrix.")
            res = find_alexander_fingerprint_cuda(chain, density, level, closure_int, tries)
        else:
            if debug:
                print("CUDA not detected or disallowed, calculating whole fingerprint matrix without CUDA.")
            res = find_alexander_fingerprint_simple(chain, density=density, level=level, closure=closure, reduce=reduce,
                                                    tries=tries, direction=direction, debug=debug)
    else:
        res = find_alexander_whole_chain(chain, closure=closure, reduce=reduce, tries=tries, translate=translate,
                                         poly_reduce=poly_reduce, direction=direction, debug=debug)

    if plot:
        plot_matrix(res, plot_ofile=plot_ofile, plot_format=plot_format, circular=circular)

    if output_file:
        with open(output_file, 'w') as myfile:
            myfile.write(res)
        res = 0

    return res

def jones_old(structure, closure='two_points', tries=200, direction=0, reduce='kmt', translate=False,
        poly_reduce=True, matrix=False, density=1, level=0, plot=False, plot_ofile="KnotFingerPrintMap",
        plot_format="png", output_file='', circular=False, debug=False):
    # calculating the Jones polynomial
    """Returns either the dictionary of the Jones polynomials/knot types with their probability for the chain delimited
        by beg/end (matrix=False), or the whole matrix of knot types for each subchain (matrix=True), or the status 0,
        if the output is directed to the output_file.

        Args:
    """
    if plot:
        matrix = True
    if len(structure) > 1 and matrix:
        print("The matrix mode can be invoked only for one-chain structure. Setting matrix mode and plot to False.")
        matrix = False
        plot = False

    chains = [coords2chain(chain) for chain in structure]


    if matrix:
        if debug:
            print("Calculating whole fingerprint matrix.")
        res = find_jones_fingerprint(chains[0], density=density, level=level, closure=closure, reduce=reduce,
                                                tries=tries, direction=direction, debug=debug)
    else:
        res = find_jones_whole_chain(chains, closure=closure, reduce=reduce, tries=tries, translate=translate,
                                         poly_reduce=poly_reduce, direction=direction, debug=debug)

    if plot:
        plot_matrix(res, plot_ofile=plot_ofile, plot_format=plot_format, circular=circular)

    if output_file:
        with open(output_file, 'w') as myfile:
            myfile.write(res)
        res = 0
    return res

def homfly_old(structure, closure='two_points', tries=200, direction=0, reduce='kmt', translate=False,
        poly_reduce=True, matrix=False, density=1, level=0, plot=False, plot_ofile="KnotFingerPrintMap",
        plot_format="png", output_file='', circular=False, debug=False):

    """Returns either the dictionary of the HOMFLY-PT polynomials/knot types with their probability for the chain delimited
        by beg/end (matrix=False), or the whole matrix of knot types for each subchain (matrix=True), or the status 0,
        if the output is directed to the output_file.

        Args:
    """
    if plot:
        matrix = True
    if len(structure) > 1 and matrix:
        print("The matrix mode can be invoked only for one-chain structure. Setting matrix mode and plot to False.")
        matrix = False
        plot = False

    chains = [coords2chain(chain) for chain in structure]


    if matrix:
        if debug:
            print("Calculating whole fingerprint matrix.")
        res = find_homfly_fingerprint(chains[0], density=density, level=level, closure=closure, reduce=reduce,
                                                tries=tries, direction=direction, debug=debug)
    else:
        res = find_homfly_whole_chain(chains, closure=closure, reduce=reduce, tries=tries, translate=translate,
                                         poly_reduce=poly_reduce, direction=direction, debug=debug)

    if plot:
        plot_matrix(res, plot_ofile=plot_ofile, plot_format=plot_format, circular=circular)

    if output_file:
        with open(output_file, 'w') as myfile:
            myfile.write(res)
        res = 0
    return res


def yamada_old(structure, closure='two_points', tries=200, direction=0, reduce='kmt', translate=False,
    poly_reduce=True, matrix=False, density=1, level=0, plot=False, plot_ofile="KnotFingerPrintMap",
    plot_format="png", output_file='', debug=False):

    """Returns either the dictionary of the HOMFLY-PT polynomials/knot types with their probability for the chain delimited
        by beg/end (matrix=False), or the whole matrix of knot types for each subchain (matrix=True), or the status 0,
        if the output is directed to the output_file.

        Args:
    """
    if plot:
        matrix = True

    chains = [coords2chain(chain) for chain in structure]

    if matrix:
        if debug:
            print("Calculating whole fingerprint matrix.")
        res = find_yamada_fingerprint(chains, density=density, level=level, closure=closure, reduce=reduce,
                                      tries=tries, direction=direction, debug=debug)
    else:
        res = find_yamada_whole_chain(chains, closure=closure, reduce=reduce, tries=tries, translate=translate,
                                      poly_reduce=poly_reduce, direction=direction, debug=debug)

    if plot:
        plot_matrix(res, plot_ofile=plot_ofile, plot_format=plot_format, yamada=True)

    if output_file:
        with open(output_file, 'w') as myfile:
            myfile.write(res)
        res = 0
    return res