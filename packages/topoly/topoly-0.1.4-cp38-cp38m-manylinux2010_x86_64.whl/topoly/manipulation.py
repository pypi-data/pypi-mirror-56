"""
The module containing the functions to manipulate the results.
Includes transforming the codes, printing, importing, simplification, and plotting functions.

Pawel Dabrowski-Tumanski
p.dabrowski at cent.uw.edu.pl
27.06.2019

Docs:
https://realpython.com/documenting-python-code/#docstring-types

The type used here: Google


Support in PyCharm:
https://www.jetbrains.com/help/pycharm/settings-tools-python-integrated-tools.html
- change default reStructuredText to Google

Docs will be published in: https://readthedocs.org/

"""

# TODO
# Dopisac w opisie potrzebne paczki (MatPlotLib) do rysowania?

import re
import ctypes
from topoly_preprocess import *
from topoly_homfly import *
from polynomial import polynomial
from polvalues import HOMFLYPT
from codes import PD



closures = {"closed": 0, "mass_center": 1, "two_points": 2, "one_point": 3, "rays": 4}

#### Importing
# importing the codes and structures
def import_coordinates(source):
    # returns the vector structure for the chain
    return

def import_PD(code):
    # import the PD code of a structure
    try:
        return PD[code]
    except KeyError:
        raise ValueError(code + " not in local library. Sorry.")

def parse_input(curve):
    return curve

def parse_input2(curve):
    if not curve:
        # TODO make an exception
        print('Empty curve')
        return
    if type(curve) is str:
        return chain_read_from_string(curve.encode('utf-8'))
    elif type(curve) is list:
        if type(curve[0]) is str:
            outdata = []
            for arc in curve:
                outdata.append(chain_read_from_string(arc.encode('utf-8')))
            return outdata
    else:
        # TODO make an exception
        print('The curve in unknown format.')
        return


#### Printing
# printing the results
def print_polynomial(name,polytype='Alexander'):
    # printing the value of the polynomial from library
    return

### Data manipulation
def prepare_data(curve):
    # we assume that each point is represented by its coordinates (list of three elements) exactly
    # TODO relax this condition
    file_list = []
    points = {}
    n = 0
    for k in range(len(curve)):
        arc = curve[k]
        for point in arc:
            if tuple(point) not in points.keys():
                n += 1
                points[tuple(point)] = n
        file_name = '_arc' + str(k)
        with open(file_name, 'w') as myfile:
            for point in arc:
                myfile.write(' '.join([str(points[tuple(point)])] + [str(x) for x in point]) + '\n')
        file_list.append(file_name)
    return file_list

#### Translating
# translating the codes
def coords2em(structure, yamada=False, closure='direct', direction=0, reduce='kmt', tries=200):
    # translating the coordinates to the (generalized) EM code
    closure_int = closures[closure]
    if yamada:
        code = find_link_yamada_code(structure)
    else:
        code = find_link_homfly_code(structure, closure=closure_int, uTRY=tries)
    code = code.decode('utf-8').strip()
    return code

def coords2chain(curve, beg=-1, end=-1):
    res = ''
    indices = []
    for atom in curve:
        res += ' '.join([str(x) for x in atom]) + '\n'
        indices.append(int(atom[0]))
    chain, unable = chain_read_from_string(res.encode('utf-8'))
    if beg not in indices:
        beg = min(indices)
    if end not in indices:
        end = max(indices)
    chain, res = cut_chain(chain, beg, end)
    return chain

def em2pd(code):
    # translates the extended EM code to PD code
    result = ''
    letters = 'abcd'
    intervals = []
    for cross in code.splitlines():
        if not cross:
            continue
        number, rest = re.sub('[-+V]', ' ', cross, count=1).split()
        typ = cross.strip(number)[0]
        code_tmp = []
        tmp = re.split(r'(\d+)', rest)[1:]
        for k in range(0, len(tmp), 2):
            end = tmp[k] + tmp[k + 1]
            if typ == 'V':
                start = number + 'V'
            else:
                start = number + letters[int(k / 2)]
            interval = sorted([start, end])
            if interval not in intervals:
                intervals.append(interval)
            code_tmp.append(str(intervals.index(interval)))
        if typ == '-':
            code_tmp = list(reversed(code_tmp))
        if typ == '+':
            code_tmp = [code_tmp[1], code_tmp[0], code_tmp[3], code_tmp[2]]
        result += re.sub('[-+]', 'X', typ) + '[' + ','.join(code_tmp) + '];'
    result = result[:-1]
    return result

def braid2pd(code):
    # translates the braid one dimensional representation to PD code
    # returns the PD code of the braid, number of strings and the indices of the outgoing arcs
    crossings = [float(x) for x in code.split()]
    strings = max([abs(int(n)) for n in crossings] + [int(str(x)[2:]) for x in crossings if abs(x) < 1]) + 1
    current = range(strings)
    code = ''
    for cross in crossings:
        new = max(current) + 1
        if cross <= -1:
            ind = int(cross)
            code += 'X[' + ','.join([str(current[abs(ind)]), str(new + 1), str(new), str(current[abs(ind)-1])]) + '];'
        elif cross >= 1:
            ind = int(cross)
            code += 'X[' + ','.join([str(current[abs(ind)-1]), str(current[abs(ind)]), str(new + 1), str(new)]) + '];'
        else:
            ind = int(str(abs(cross))[2:])
            code += 'V[' + ','.join([str(current[abs(ind) - 1]), str(current[abs(ind)])]) + '];'
            code += 'V[' + ','.join([str(new), str(new + 1)]) + '];'
        current[abs(ind)] = new + 1
        current[abs(ind) - 1] = new
        code = code[:-1]
    return code, strings, current


def pd2em(code):
    # translates the extended PD code to EM code
    return


def empoly(poly):
    p = polynomial()
    parts = poly.split('|')
    n = 0
    for k in range(len(parts)):
        part = parts[k]
        print(part)
    return p

def data2Wanda(data, beg, end):
    res = '# ' + str(beg) + ' ' + str(end) +' >90 >87 >84 >81 >78 >75 >72 >69 >66 >63 >60 >57 >54 >51 >48 >45 >42 >39 ' \
                                '>36 >33 >30 >27 >24 >21 >18 >15 >12 >9 >6 >3 >0 IN ' + str(beg) + ' ' + str(end) + '\n'
    for key in sorted(data.keys()):
        res_line = list(key) + [0 for _ in range(32)] + list(key)
        for knot in data[key]:
            ind = 32-int(min(100*knot[1], 90)/3)
            if res_line[ind] == 0:
                res_line[ind] = knot[0].replace('_', '')
            else:
                res_line[ind] += ';' + knot[0].replace('_', '')
        res += ' '.join([str(_) for _ in res_line]) + '\n'
    return res


### Graph manipulation

def substitute_edge(graph, substitue='Virtual', debug=True):
    # substituting second edge type with another structure
    return

### Closing the chains or braids
def braid_close(code, strings, current, close_type='N'):
    # returns the PD code of the closed braid
    start = range(strings)
    if close_type == 'N':
        code += 'V[' + ','.join(str(x) for x in list(reversed(start))) + '];'
        code += 'V[' + ','.join(str(x) for x in current) + ']'
    elif close_type == 'D':
        for s in range(strings):
            code += 'V[' + ','.join([str(start[s]), str(current[s])]) + '];'
        code = code[:-1]
    elif close_type == 'V':
        code += 'V[' + ','.join(str(x) for x in current + list(reversed(start))) + ']'
    else:
        new = max(current) + 1
        code += 'V[' + ','.join(str(x) for x in list(reversed(start))) + ',' + str(new) + '];'
        code += 'V[' + ','.join(str(x) for x in current) + ',' + str(new) + ']'
    return code

def chain_close(chain_in, method, direction=0):
    if method == 'mass_center':
        res, chain = close_chain_out(chain_in)
    elif method == 'one_point':
        res, chain = close_chain_1point(chain_in)
    elif method == 'two_points':
        res, chain = close_chain_2points(chain_in)
    elif method == 'rays':
        res, chain = close_chain_1direction(chain_in)
    elif method == 'direction':
        res, chain = close_chain_1direction_no_random(chain_in, direction)
    elif method == 'closed':
        res, chain = 0, chain_in
    else:
        print("Unknown closing method") # TODO make it as exception
        return
    return chain

#### Simplification
# simplification of the curves
def chain_reduce(curve, method, closed=True):
    if method == 'sono':
        return chain_sono(curve)
    elif method == 'knot_pull':
        return chain_knot_pull(curve)
    elif method == 'kmt':
        return chain_kmt(curve, closed)
    elif method == 'reidemeister':
        return chain_reidemeister(curve)
    else:
        print('Unknown reduction method ' + method)     # TODO make it as exception
        return

def chain_kmt(curve, closed=True):
    return kmt_reduction(curve, closed)

def chain_knot_pull(curve):
    return

def chain_sono(curve):
    return

def chain_reidemeister(code):
    return


#### Plotting
# plotting the results, e.g. the matrices
def plot_matrix(data,palette='default',debug=False):
    return


#### Generating
def generate_coordinates(code):
    # builds the spatial graph from PD code
    return

def generate_polyhedra(n):
    # generating the Martin's polyhedra with n vertices
    return


### Structure validation

### Others
def understand_homfly(p):
    if p in HOMFLYPT.keys():
        return HOMFLYPT[p]
    return 'Unknown'

def check_cuda():
    """
    It's a port of https://gist.github.com/f0k/0d6431e3faa60bffc788f8b4daa029b1
    Author: Jan Schlüter
    """

    libnames = ('libcuda.so', 'libcuda.dylib', 'cuda.dll')
    CUDA_SUCCESS = 0
    for libname in libnames:
        try:
            cuda = ctypes.CDLL(libname)
        except OSError:
            return False
        else:
            break
    else:
        return False

    nGpus = ctypes.c_int()
    result = cuda.cuInit(0)
    if result != CUDA_SUCCESS:
        return False
    result = cuda.cuDeviceGetCount(ctypes.byref(nGpus))
    if result != CUDA_SUCCESS:
        return False
    return True

def guess_format(data):
    first_line = data.split('\n')[0]
    if isinstance(data, list):
        return 'list'
    elif not isinstance(data, str):
        raise TypeError('Unknown type of input data. Expected string or list.')
    elif '{' in data:
        return 'mathematica'
    elif 'ATOM' in data:
        return 'pdb'
    elif len(first_line.split()) == 4 and isinstance(first_line.split()[0], int):
        return 'nxyz'
    else:
        return 'xyz'

def parse_data(data,format):
    if format == 'list':
        return read_list(data)
    elif format == 'nxyz':
        return read_nxyz(data)
    elif format == 'mathematica':
        return read_mathematica(data)
    elif format == 'pdb':
        return read_pdb(data)
    else:
        return read_xyz(data)

def read_list(data):
    return data

def read_mathematica(data):
    structure = []
    indices = {}
    arcs = data.strip('"{}\n').split('}}","{{')
    for arc in arcs:
        arc_list = []
        atoms = arc.strip().split('}, {')
        for atom in atoms:
            coords = atom.replace(',', '')
            if coords in indices.keys():
                ind = indices[coords]
            else:
                ind = len(indices) + 1
                indices[coords] = ind
            arc_list.append([ind] + [float(_.replace('*^','E')) for _ in coords.split()])
        if arc_list[-1] == arc_list[0]:
            structure.append(arc_list[:-1])
            structure.append(arc_list[-2:])
        else:
            structure.append(arc_list)
    return structure

def read_pdb(data):
    structure = []
    coords = {}
    bridges = []
    for line in data.splitlines():
        if line[0:4] == 'ATOM' and line[12:16].strip() == 'CA':
            coords[int(line[22:26].strip())] = [float(line[30:38].strip()), float(line[38:46].strip()), float(line[46:54].strip())]
        elif line[0:4] == 'LINK':
            continue
        elif line[0:6] == 'SSBOND':
            bridges.append([int(line[17:21].strip()), int(line[31:35].strip())])
        else:
            continue
    beg, end = min(list(coords.keys())), max(list(coords.keys()))
    breaks = sorted(list(set([item for sublist in bridges for item in sublist] + [beg,end])))
    for k in range(len(breaks)-1):
        arc = []
        for l in range(breaks[k], breaks[k+1]+1):
            arc.append([l] + coords[l])
        structure.append(arc)
    for bridge in bridges:
        structure.append([[atom] + coords[atom] for atom in bridge])
    return structure

def read_xyz(data):
    structure = []
    arc = []
    indices = {}
    for line in data.splitlines():
        first_float = False
        try:
            float(line.split()[0])
            first_float = True
        except ValueError:
            first_float = False
        if not first_float:
            if arc and arc[-1] == arc[0]:
                structure.append(arc[:-1])
                structure.append(arc[-2:])
            elif arc:
                structure.append(arc)
            arc = []
        else:
            if line.strip() in indices.keys():
                ind = indices[line.strip()]
            else:
                ind = len(indices) + 1
                indices[line.strip()] = ind
            arc.append([ind] + [float(_) for _ in line.strip().split()])
    if arc and arc not in structure and arc[:-1] not in structure:
        if arc[-1] == arc[0]:
            structure.append(arc[:-1])
            structure.append(arc[-2:])
        else:
            structure.append(arc)
    return structure

def read_nxyz(data):
    structure = []
    arc = []
    for line in data.splitlines():
        first_int = False
        try:
            int(line.split()[0])
            first_int = True
        except ValueError:
            first_int = False
        if not first_int:
            if arc[-1] == arc[0]:
                structure.append(arc[:-1])
                structure.append(arc[-2:])
            else:
                structure.append(arc)
            arc = []
        else:
            atom = [float(_) for _ in line.strip().split()]
            atom[0] = int(atom[0])
            arc.append(atom)
    if arc and arc not in structure and arc[:-1] not in structure:
        if arc[-1] == arc[0]:
            structure.append(arc[:-1])
            structure.append(arc[-2:])
        else:
            structure.append(arc)
    return structure