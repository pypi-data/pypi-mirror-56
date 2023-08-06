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

from .manipulation import *
from .invariants import *
from .topoly_knot import *
from .codes import *
from .plotting import KnotMap, Reader




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