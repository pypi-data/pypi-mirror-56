"""
The module containing the functions for calculating the isotopy invariants starting from graphs. In particular,
it contains functions to calculate knot invariants (Jones, Alexander, HOMFLY-PT) and spatial graph invariants.

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

import subprocess
import os
from polynomial import polynomial as Poly, decode_poly, understand_poly
from topoly_homfly import *
from topoly_preprocess import *
from manipulation import chain_close, chain_reduce, data2Wanda, coords2em, em2pd
from topoly_knot import *
from topoly_lmpoly import *
import array
from graph import Graph
from polvalues import polvalues

closures = {"closed": 0, "mass_center": 1, "two_points": 2, "one_point": 3, "rays": 4}
knot_amount = 40

# general function
def calculate_invariant(input_data, invariant,
            closure='two_points', tries=200, direction=0, reduce_method='kmt',
            poly_reduce=True, translate=False,
            matrix=False, density=1, level=0, beg=-1, end=-1, max_cross=15, chirality=False,
            matrix_plot=False, plot_ofile="KnotFingerPrintMap", plot_format="png", disk=False,
            output_file='', cuda=True, debug=False):

    if disk:
        matrix_plot = True
    if matrix_plot:
        matrix = True
    if isinstance(input_data, Graph):
       pass
    else:
        g = Graph(input_data)
    result = g.invariant(invariant, closure=closure, tries=tries, direction=direction, cuda=cuda,
                         reduce_method=reduce_method, matrix=matrix, density=density, beg=beg, end=end,
                         max_cross=max_cross, chirality=chirality, level=level, debug=debug)

    if translate:
        result = find_matching_structure(result)
    elif not poly_reduce:
        result = make_poly_explicit(result)    # TODO place it somewhere
    if matrix_plot:
        plot_matrix(result, plot_ofile, plot_format, disk)
    if output_file:
        with open(output_file, 'w') as myfile:
            myfile.write(result)
            return 0
    return result



# Alexander polynomial
def find_alexander_fingerprint_simple(curve_in, density=1, level=0, closure='closed', tries=200, direction=0, debug=False):
    # TODO add the density and the level
    beg, end = int(curve_in[0]['id']), int(curve_in[-1]['id'])
    data = {}
    for k in range(beg, end+1):
        for l in range(beg, k-5):
            c, res = cut_chain(curve_in, l, k)
            res = find_alexander_whole_chain_c(c, closure=closure, tries=tries, direction=direction)
            res_filtered = []
            for r in res:
                if r[0]!= '0_1':
                    res_filtered.append(r)
            if res_filtered:
                data[(l, k)] = res_filtered
    res = data2Wanda(data, beg, end)
    return res

def find_alexander_whole_chain_c(chain, closure='closed', tries=200, direction=0):
    # TODO include the direction
    knots = array.array('i', [0] * knot_amount)
    closure_int = closures[closure]
    out, k = find_major_knot(chain, knots, closure=closure_int, uTRY_AMOUNT=tries)
    res_tmp = give_the_name_of_knot(k).split()
    res = []
    for knot in res_tmp:
        knot_type, p = knot.split('(')
        knot_type = knot_type[0] + '_' + knot_type[1:]
        p = float(p.strip('%)'))/100
        res.append([knot_type, p])
    return res

def find_alexander_whole_chain(chain, closure='closed', reduce='kmt', tries=200, translate=False, poly_reduce=True, direction=0, debug=False):
    res = {}
    if closure in ['closed', 'mass_center']:
        if debug:
            print("Deterministic closure method chosen. Number of tries set to 1.")
        tries = 1

    for k in range(tries):
        # closing the chain
        if debug:
            print("Try: " + str(k+1) + "/" + str(tries) + ".\nClosing chain with method " + closure + ":")
        closed_chain = chain_close(chain, closure, direction)
        if debug:
            print(chain)

        # chain reducing
        if debug:
            print("Reducing the chain using method " + reduce + ":")
        chain_red = chain_reduce(closed_chain, reduce, closed=True)
        if debug:
            print(chain_red)

        # calculating the Alexander polynomial
        if debug:
            print("Calculating the Alexander polynomial.")
        p = calc_alexander_poly(chain_red)
        if debug:
            print("The polynomial in reduced form:")
            print(p)
        if not p:
            return "UNKNOWN"

        if not poly_reduce:
            p_unred = decode_poly(p, 'Alexander')
            if debug:
                print("The polynomial in excplicit form:")
                print(p_unred)

        if translate:
            if debug:
                print("The matching knot in the library:")
            p_undest = understand_poly(p, 'Alexander')
            if debug:
                print(p_undest)

        if not poly_reduce:
            p = decode_poly(p, 'Alexander')

        if translate:
            if debug:
                print(p)
                print("The matching knot in the library:")
            p_undest = understand_poly(p, 'Alexander')
            if debug:
                print(p)

        if int(p.split()[0]) < 0:
            p = ' '.join([str(_) for _ in [-int(x) for x in p.split()]])
        if p not in res.keys():
            res[p] = 0
        res[p] += 1
    if len(res.keys()) == 1:
        for key in res.keys():
            p = key
        res = p
    else:
        for key in res.keys():
            res[key] = float(res[key])/tries
    return res

# Kauffman bracket
def point_kauffman():
    return

def calculate_kauffman_bracket(graph, level=0, known={}, p='', return_known=False, debug=False):
    return

# Jones polynomial
def find_jones_fingerprint(curve_in, density=1, level=0, closure='two_points', reduce='kmt',
                                                tries=200, direction=0, debug=False):
    beg, end = int(curve_in[0]['id']), int(curve_in[-1]['id'])
    data = {}
    for k in range(beg, end+1):
        for l in range(beg, k-5):
            c, res = cut_chain(curve_in, l, k)
            res = find_jones_whole_chain(c, closure=closure, tries=tries, direction=direction)
            res_filtered = []
            for r in res:
                if r[0]!= '0_1':
                    res_filtered.append(r)
            if res_filtered:
                data[(l, k)] = res_filtered
    res = data2Wanda(data, beg, end)
    return res

def find_jones_whole_chain(curve, closure='two_points', reduce='kmt', tries=200, translate=False,
                                         poly_reduce=True, direction=0, debug=False):
    res = {}
    EMcode = coords2em(curve,yamada=False,closure=closure,direction=direction,reduce=reduce,tries=tries)
    codes = EMcode.split('\n\n')
    if debug:
        print("EMcodes: ",[code.strip().replace("\n", ";") for code in codes])
    for code in codes:
        # calculating the Jones polynomial
        if debug:
            print("Calculating the Jones polynomial.")
        p = lmpoly(code.encode('utf-8')).replace('\n','|')
        p_unred = Poly(decode_poly(p, 'HOMFLY'))
        p_unred = p_unred({"l": 'it**-1', "m": 'it**-0.5 - it**0.5'})
        p_unred = p_unred({"i**2": '-1'})
        p = p_unred.print_short()
        if debug:
            print("The polynomial in reduced form:")
            print(p)
        if not p:
            return "UNKNOWN"
        if not poly_reduce:
            if debug:
                print("The polynomial in excplicit form:")
                print(p_unred)

        if translate:
            if debug:
                print("The matching knot in the library:")
            p_undest = understand_poly(p, 'Jones')
            if debug:
                print(p_undest)

        if p not in res.keys():
            res[p] = 0
        res[p] += 1
    if len(res.keys()) == 1:
        for key in res.keys():
            p = key
        res = p
    else:
        for key in res.keys():
            res[key] = float(res[key]) / tries
    return res

# HOMFLY-PT polynomial
def find_homfly_fingerprint(curve_in, density=1, level=0, closure='two_points', reduce='kmt',
                                                tries=200, direction=0, debug=False):
    beg, end = int(curve_in[0]['id']), int(curve_in[-1]['id'])
    data = {}
    for k in range(beg, end+1):
        for l in range(beg, k-5):
            c, res = cut_chain(curve_in, l, k)
            res = find_homfly_whole_chain(c, closure=closure, tries=tries, direction=direction)
            res_filtered = []
            for r in res:
                if r[0]!= '0_1':
                    res_filtered.append(r)
            if res_filtered:
                data[(l, k)] = res_filtered
    res = data2Wanda(data, beg, end)
    return res

def find_homfly_whole_chain(curve, closure='two_points', reduce='kmt', tries=200, translate=False,
                                         poly_reduce=True, direction=0, debug=False):
    res = {}
    EMcode = coords2em(curve,yamada=False,closure=closure,direction=direction,reduce=reduce,tries=tries)
    codes = EMcode.split('\n\n')
    if debug:
        print("EMcodes: ",[code.strip().replace("\n", ";") for code in codes])
    for code in codes:
        # calculating the HOMFLY-PT polynomial
        if debug:
            print("Calculating the HOMFLY-PT polynomial.")
        p = lmpoly(code.encode('utf-8')).replace('\n','|')
        if debug:
            print("The polynomial in reduced form:")
            print(p)
        if not p:
            return "UNKNOWN"
        if not poly_reduce:
            p_unred = decode_poly(p, 'HOMFLY')
            if debug:
                print("The polynomial in excplicit form:")
                print(p_unred)

        if translate:
            if debug:
                print("The matching knot in the library:")
            p_undest = understand_poly(p, 'HOMFLY')
            if debug:
                print(p_undest)
            return p_undest

        if p not in res.keys():
            res[p] = 0
        res[p] += 1
    if len(res.keys()) == 1:
        for key in res.keys():
            p = key
        res = p
    else:
        for key in res.keys():
            res[key] = float(res[key]) / tries
    return res

# Yamada polynomial
def find_yamada_fingerprint(chains, density=1, level=0, closure='two_point', reduce='kmt',
                                      tries=200, direction=0, debug=False):
    return

def find_yamada_whole_chain(chains, closure='two_point', reduce='kmt', tries=200, translate=False,
                                         poly_reduce=True, direction=0, debug=False):
    # calculating the Yamada polynomial
    EMcode = coords2em(chains,yamada=True,closure=closure,direction=direction,reduce=reduce,tries=tries)
    if debug:
        print("EMcode: " + EMcode.strip().replace("\n", ";"))
    PDcode = em2pd(EMcode)
    if debug:
        print("PDcode: " + PDcode)
    g = Graph(PDcode)
    g.simplify()
    if len(g.get_crossings()) > 15:
        return "Too many crossings (" + str(len(g.get_crossings())) + ")."
    p_unred = calculate_yamada(g)
    p = p_unred.print_short()
    if translate:
        if debug:
            print("The matching knot in the library:")
        p_undest = understand_poly(p, 'Yamada')
        if debug:
            print(p_undest)
        p = p_undest
    return p

def calculate_yamada(graph, level=0, known={}, p='', return_known=False, debug=False):
    com1 = ''
    com2 = ''
    if debug:
        if level > 0:
            for k in range(level-1):
                com1 += '|  '
                com2 += '|  '
            com1 += '|->'
            com2 += '|  '
        com1 += p + graph.get_pdcode()
        print(com1)
    # calculating Yamada polynomial

    n = graph.simplify(debug=debug)  # returns power of x as a result of 1st and 5th Reidemeister move
    if debug:
        print(com2 + "After simplification: " + graph.get_pdcode() + '\tn=' + str(n))
    if len(graph.crossings) > 15:
        return 'Too many crossings.'

    # known cases, to speed up calculations:
    if graph.get_pdcode() in known.keys() and known[graph.get_pdcode()]:
        res = known[graph.get_pdcode()] * Poly(str((-1)**(n % 2))+'x^'+str(n))
        if debug:
            print(com2 + 'Known case.')
            print(com2 + "Result " + p + str(res))
        if return_known:
            return res, known
        return known[graph.get_pdcode()]
    if len(graph.vertices) == 1 and not graph.crossings:                    # bouquet of circles:
        # number of circles in bouquet = len(set(graph.vertices[0]))
        known[graph.get_pdcode()] = Poly(-1) * (Poly('-x-1-x^-1') ** len(set(graph.vertices[0])))
        res = known[graph.get_pdcode()] * Poly(str((-1)**(n % 2))+'x^' + str(n))
        if debug:
            print(com2 + "It's a bouquet of " + str(len(set(graph.vertices[0]))) + " circles.\n" + com2 + "Result " + p + str(res))
        if return_known:
            return res, known
        return res
    if len(graph.vertices) == 2 and not graph.crossings and len(graph.vertices[0]) == 3:
        if set(graph.vertices[0]) == set(graph.vertices[1]):                # trivial theta
            known[graph.get_pdcode()] = Poly('-x^2-x-2-x^-1-x^-2')
            res = known[graph.get_pdcode()] * Poly(str((-1)**(n % 2))+'x^'+str(n))
            if debug:
                print(com2 + "It's a trivial theta.\n" + com2 + "Result " + p + str(res))
            if return_known:
                return res, known
            return res
        elif len(set(graph.vertices[0]) & set(graph.vertices[1])) == 1:     # trivial handcuff
            known[graph.get_pdcode()] = Poly('0')
            res = known[graph.get_pdcode()]
            if debug:
                print(com2 + "It's a trivial handcuff graph.\n" + com2 + "Result " + str(res))
            if return_known:
                return res, known
            return res

    # other simplifying cases
    for v in range(len(graph.vertices)):
        vert = graph.vertices[v]
        if len(vert) > 3:
            for k in range(len(vert)):
                if vert[k] == vert[k-1]:
                    # bouquet with one loop
                    if debug:
                        print(com2 + "Removing loop.")
                    res_tmp, known = calculate_yamada(graph.remove_loop(v, k), level=level + 1, known=known, p=' * ', return_known=True, debug=debug)
                    known[graph.get_pdcode()] = Poly('-1') * Poly('x+1+x^-1') * res_tmp
                    res = known[graph.get_pdcode()] * Poly(str((-1) ** (n % 2)) + 'x^' + str(n))
                    if debug:
                        print(com2 + 'Result ' + str(res) + '\t(n=' + str(n) + ').')
                    if return_known:
                        return res, known
                    return res

    # split sum:
    subgraphs = graph.create_disjoined_components()
    if len(subgraphs) > 1:
        if debug:
            print(com2 + "It's a split graph.")
        known[graph.get_pdcode()] = Poly('1')
        for k in range(len(subgraphs)):
            subgraph = subgraphs[k]
            res_tmp, known = calculate_yamada(subgraph, level=level+1, known=known, p=' * ', return_known=True, debug=debug)
            known[graph.get_pdcode()] *= res_tmp
        res = known[graph.get_pdcode()] * Poly(str((-1)**(n % 2))+'x^'+str(n))
        if debug:
            print(com2 + 'Result ' + str(res) + '\t(n=' + str(n) + ').')
        if return_known:
            return res, known
        return res

    # crossing reduction:
    if len(graph.crossings) > 0:
        # two ways of removing the crossing.
        g = graph.invert_crossing(0)
        g.simplify()
        if len(g.crossings) < len(graph.crossings):
            # the skein-like relation
            if debug:
                print(com2 + "Reducing crossing " + str(graph.crossings[0]) + " by skein relation.")
            part1, known = calculate_yamada(graph.smooth_crossing(0, 1), level=level + 1, known=known, p=' (x-x^-1)* ',
                                            return_known=True, debug=debug)
            part2, known = calculate_yamada(graph.smooth_crossing(0, -1), level=level + 1, known=known,
                                            p=' -(x-x^-1)* ', return_known=True, debug=debug)
            part3, known = calculate_yamada(graph.invert_crossing(0), known=known, p=' + ', level=level + 1,
                                            return_known=True, debug=debug)
            known[graph.get_pdcode()] = Poly('x-x^-1') * (part1 - part2) + part3
            res = Poly(str((-1) ** (n % 2)) + 'x^' + str(n)) * known[graph.get_pdcode()]
            if debug:
                print(com2 + 'Result ' + str(res) + '\t(n=' + str(n) + ').')
            if return_known:
                return res, known
            return res
        else:
            # removing the crossing with introduction of new vertex
            if debug:
                print(com2 + "Reducing crossing " + str(graph.crossings[0]) + " by crossing removal.")
            part1, known = calculate_yamada(graph.smooth_crossing(0, 1), known=known, level=level + 1,
                                            return_known=True, p=' x* ', debug=debug)
            part2, known = calculate_yamada(graph.smooth_crossing(0, -1), known=known, level=level + 1,
                                            return_known=True, p=' +x^-1* ', debug=debug)
            part3, known = calculate_yamada(graph.smooth_crossing(0, 0), p=' + ', known=known, level=level + 1,
                                            return_known=True, debug=debug)
            known[graph.get_pdcode()] = Poly('x') * part1 + Poly('x^-1') * part2 + part3
            res = known[graph.get_pdcode()] * Poly(str((-1) ** (n % 2)) + 'x^' + str(n))
            if debug:
                print(com2 + 'Result ' + str(res) + '\t(n=' + str(n) + ').')
            if return_known:
                return res, known
            return res

    # edge reduction:
    edges = graph.get_noloop_edges()
    if len(edges) > 0:      # then len(graph.vertices) >= 2
        if debug:
            print(com2 + "Reducing noloop edge " + str(edges[0]) + ".")
        part1, known = calculate_yamada(graph.edge_remove(edges[0]), known=known, level=level+1, return_known=True, debug=debug)
        part2, known = calculate_yamada(graph.edge_contract(edges[0]), known=known, level=level+1, return_known=True, p=' + ', debug=debug)
        known[graph.get_pdcode()] = part1 + part2
        res = known[graph.get_pdcode()] * Poly(str((-1)**(n%2))+'x^'+str(n))
        if debug:
            print(com2 + 'Result ' + str(res) + '\t(n=' + str(n) + ').')
        if return_known:
            return res, known
        return res

    known[graph.get_pdcode()] = Poly('1')
    res = Poly(str((-1)**(n%2))+'x^'+str(n))        # no crossing, no vertex = empty graph
    if debug:
        print(com2 + "Empty graph. Result " + str(res))
    if return_known:
        return res, known
    return res

# Boundary links
def calculate_boundary_links(graph, debug=False):
    return

# APS bracket
def calculate_APS(graph, debug=False):
    return

def find_matching_structure(data):
    if not data:
        return '0_1'
    if len(data) == 0:
        return data
    elif type(list(data.keys())[0]) is str:
        to_del = list(data.keys())
        for prob in to_del:
            res = find_point_matching({prob.split(':')[0].strip(): prob.split(':')[1].strip()})
            data[res] = data[prob]
        for e in to_del:
            data.pop(e)
    else:
        for key in data.keys():
            to_del = list(data[key].keys())
            for prob in to_del:
                res = find_point_matching({prob.split(':')[0].strip(): prob.split(':')[1].strip()})
                data[key][res] = data[key][prob]
            for e in to_del:
                data[key].pop(e)
    return data

def find_point_matching(data):
    possible = []
    for key in data.keys():
        d = polvalues[key]
        #TODO clean it
        if '{' not in data[key] and '|' not in data[key] and '[' not in data[key] and 'Too' not in data[key]:
            v = ' '.join([str(-int(_)) for _ in data[key].strip().split()])
        else:
            v = -1
        if data[key] in d.keys():
            res = d[data[key]].split('|')
        elif v in d.keys():
            res = d[v].split('|')
        else:
            return 'Unknown polynomial values (' + str(key) + ' ' + str(data[key]) + ').'
        if not possible:
            possible = res
        else:
            possible = set(possible) & set(res)
    return '|'.join(possible)