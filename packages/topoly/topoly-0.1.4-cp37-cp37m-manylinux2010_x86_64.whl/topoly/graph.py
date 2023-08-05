"""
The graph class containing the methods to calculate the graph (and knot) polynomials.
The graphs are stored as extended PD codes, including the information on vertices and crossings in planar projection.

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
# until here

import re
import random
import numpy as np
# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
from topoly_knot import *
from topoly_homfly import *
from topoly_lmpoly import *
from manipulation import chain_close, chain_reduce, check_cuda
from itertools import combinations, product
from copy import deepcopy
from mpl_toolkits import mplot3d
from polynomial import polynomial as Poly
import logging


plot_colors = ['blue', 'red', 'green', 'yellow', 'cyan', 'magenta']
available_invariants = ['alexander', 'conway', 'jones', 'homfly', 'yamada', 'kauffman_bracket', 'kauffman_polynomial', 'blmho', 'gln', 'writhe']
closures = {"closed": 0, "mass_center": 1, "two_points": 2, "one_point": 3, "rays": 4}


class Graph:
    def __init__(self, init_data='', bridges='', breaks=''):
        self.vertices = []
        self.crossings = []
        self.pdcode = ''
        self.emcode = ''
        self.coordinates = {}
        self.coordinates_W = []
        self.bridges = []
        self.breaks = []
        self.abstract_graph = {}
        self.arcs = []
        self.abstract_arcs = []
        self.loops = []
        self.thetas = []
        self.connected_components = []
        self.noloop_edges = []

        self.known = {}
        self.Alexander_poly = ''
        self.Jones_poly = ''
        self.HOMFLY_poly = ''
        self.Yamada_poly = ''

        self.level = 0
        self.communicate = ''


        self.edges = set()

        if bridges:
            self.bridges = bridges

        if breaks:
            self.breaks = breaks

        if type(init_data) is list:
            self.read_coordinates(init_data)
            self.coords2em()
            self.em2pd()
            # self.em2gauss()

        elif type(init_data) is str and '[' in init_data:
            self.pdcode = init_data
            self.generate_coords()
            self.pd2em()
            # self.em2gauss()

        # elif type(init_data) is str and 'o' in init_data:
        #     self.gausscode = init_data
        #     self.gauss2em()
        #     self.em2pd()
        #     self.generate_coords()

        else:
            self.emcode = init_data
            self.em2pd()
            # self.em2gauss()
            self.generate_coords()

        self.generate_vertices()
        self.generate_crossings()
        self.generate_edges()
        # self.remove_double_verts()
        self.generate_identifier()
        # self.generate_abstract_graph()
        return

    ### getting ###
    def get_pdcode(self):
        return self.pdcode

    def get_emcode(self):
        return self.emcode


    def get_vertices(self):
        return self.vertices

    def get_crossings(self):
        return self.crossings

    def get_coordinates(self):
        return self.coordinates

    def get_coordinates_W(self):
        return self.coordinates_W

    def get_bridges(self):
        return self.bridges

    def get_breaks(self):
        return self.breaks

    def get_abstract_graph(self):
        return self.abstract_graph

    def get_arcs(self):
        return self.arcs

    def get_loops(self):
        if not self.loops:
            self.loops = self.find_loops()
        return self.loops

    def get_thetas(self):
        if not self.thetas:
            self.thetas = self.find_thetas()
        return self.thetas

    def get_connected_components(self):
        if not self.connected_components:
            self.connected_components = self.find_connected_components()
        return self.connected_components

    def get_noloop_edges(self):
        noloop = []
        for e in self.edges:
            n = 0
            for v in self.vertices:
                if e in v:
                    n += 1
            if n == 2:
                noloop.append(e)
        return noloop

    def get_abstract_arcs(self):
        return self.abstract_arcs


    ### generating and translating ###
    def coords2em(self):
        if len(self.coordinates_W) == 1:
            code = find_link_homfly_code(self.coordinates_W)
        else:
            code = find_link_yamada_code(self.coordinates_W)
        code = code.decode('utf-8').strip().replace('\n',';')
        self.emcode = code
        return

    def em2pd(self):
        # translates the extended EM code to PD code
        result = ''
        letters = 'abcd'
        intervals = []
        for cross in self.emcode.split(';'):
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
                interval = [start, end]
                interval_rev = list(reversed(interval))
                if interval_rev in intervals:
                    code_tmp.append(str(intervals.index(interval_rev)))
                    intervals[intervals.index(interval_rev)] = 0
                else:
                    intervals.append(interval)
                    code_tmp.append(str(len(intervals)-1))
            if typ == '-':
                code_tmp = list(reversed(code_tmp))
            if typ == '+':
                code_tmp = [code_tmp[1], code_tmp[0], code_tmp[3], code_tmp[2]]
            result += re.sub('[-+]', 'X', typ) + '[' + ','.join(code_tmp) + '];'
        self.pdcode = result[:-1].strip()
        return

    def update_pdcode(self):
        code = ''
        for vert in self.vertices:
            code += 'V[' + ','.join(vert) + '];'
        for cross in self.crossings:
            code += 'X[' + ','.join(cross) + '];'
        self.pdcode = code[:-1]

    def pd2em(self):
        self.emcode = ''
        return

    def generate_vertices(self):
        self.vertices = []
        for element in self.pdcode.split(';'):
            if element[0] == 'V':
                self.vertices.append(element.strip('V[]').split(','))
        return

    def generate_crossings(self):
        self.crossings = []
        for element in self.pdcode.split(';'):
            if element[0] == 'X':
                self.crossings.append(element.strip('X[]').split(','))
        return

    def generate_edges(self):
        for cross in self.crossings:
            self.edges |= set(cross)
        for vert in self.vertices:
            self.edges |= set(vert)
        return

    def generate_abstract_graph(self):
        vertices = {}
        vert_dict = {}
        cross_dict = {}
        for k in range(len(self.vertices)):
            vert_dict[k] = self.vertices[k]
        for k in range(len(self.crossings)):
            cross_dict[k] = self.crossings[k]
        for key in list(vert_dict.keys()):
            self.abstract_graph[key] = []
            for v in vert_dict[key]:
                if v not in vertices.keys():
                    vertices[v] = []
                vertices[v].append(key)

        for key in list(vertices.keys()):
            if len(vertices[key]) == 2:
                self.abstract_arcs.append([tuple(vertices[key]), [key]])
                self.abstract_graph[vertices[key][0]].append([vertices[key][1], len(self.abstract_arcs)-1])
                if vertices[key][0] != vertices[key][1]:
                    self.abstract_graph[vertices[key][1]].append([vertices[key][0], len(self.abstract_arcs)-1])
                vertices.pop(key)
            else:
                vertices[key] = vertices[key][0]

        while vertices:
            arc = [list(vertices.keys())[0]]
            v0 = vertices[arc[-1]]
            vertices.pop(arc[-1])
            while arc[-1] not in vertices.keys():
                for cross in [cross_dict[key] for key in cross_dict.keys()]:
                    if arc[-1] in cross and cross[cross.index(arc[-1])-2] not in arc:
                        arc.append(cross[cross.index(arc[-1])-2])
            v = vertices[arc[-1]]
            self.abstract_arcs.append([(v0, v), arc])
            self.abstract_graph[v0].append([v, len(self.abstract_arcs)-1])
            self.abstract_graph[v].append([v0, len(self.abstract_arcs)-1])
            vertices.pop(arc[-1])
        return

    def generate_identifier(self):
        self.identifier = []
        for arc in self.arcs:
            self.identifier.append((arc[0], arc[-1]))
        if len(self.identifier) == 1:
            self.identifier = self.identifier[0]
        else:
            self.identifier = tuple(self.identifier)
        return

    def generate_coords(self):
        self.coordinates = []
        return

    def generate_boundary_links(self):
        return

    def generate_double_branched_cover(self):
        return

    def read_coordinates(self, input_data):
        for c in input_data:
            chain = ''
            arc = []
            for atom in c:
                coords = ' '.join([str(x) for x in atom[1:]])
                ind = int(atom[0])
                chain += str(ind) + ' ' + coords + '\n'
                arc.append(ind)
                self.coordinates[ind] = atom[1:]
            chain_W, unable = chain_read_from_string(chain.encode('utf-8'))
            self.coordinates_W.append(chain_W)
            self.arcs.append(arc)
        return

    def create_disjoined_components(self):
        components = self.find_connected_components()
        for cross in self.crossings:
            k = 0
            while k < len(components):
                l = k + 1
                while l < len(components):
                    if cross[0] in components[k] and cross[1] in components[1]:
                        components[k] |= components[l]
                        components.pop(l)
                    l += 1
                k += 1
        subgraphs = ['' if len(element) != 0 else 'V' for element in components]
        for k in range(len(components)):
            for vertex in self.vertices:
                if len(vertex) > 0 and all(v in components[k] for v in vertex):
                    subgraphs[k] += 'V' + str([int(_) for _ in vertex]).replace(' ','') + ';'
            for cross in self.crossings:
                if all(c in components[k] for c in cross):
                    subgraphs[k] += 'X' + str([int(_) for _ in cross]).replace(' ','') + ';'
        for k in range(len(subgraphs)):
            subgraphs[k] = Graph(subgraphs[k][:-1])
        return subgraphs

    ### finding ###
    def find_crossing_sign(self,n):
        edges_num= len(self.crossings)*2 + len(self.vertices)
        paths = []
        checked = []
        while len(checked) < edges_num:
            # searching for starting crossing
            for cross in self.crossings:
                if cross[0] not in checked:
                    path = [cross[0], cross[2]]
                    break
            while True:
                b = False
                for c in self.crossings:
                    if path[-1] in c and c[c.index(path[-1])-2] not in path:
                        path.append(c[c.index(path[-1]) - 2])
                        break
                    if path[-1] in c and c[c.index(path[-1])-2] == path[0] and c != cross:
                        b = True
                        break
                for v in self.vertices:
                    if path[-1] in v and v[v.index(path[-1])-1] not in path:
                        path.append(v[v.index(path[-1])-1])
                    if path[-1] in v and v[v.index(path[-1])-1] == path[0]:
                        b = True
                        break
                if b:
                    break
            paths.append(path)
            checked = [item for sublist in paths for item in sublist]
        sign = 0
        for path in paths:
            if self.crossings[n][1] in path:
                sign = path.index(self.crossings[n][1]) - path.index(self.crossings[n][3])
            if sign == 1-len(path):
                sign = 1
            elif sign == len(path)-1:
                sign = -1
        return sign

    def find_connected_components(self):
        # 0.1 case
        if len(self.crossings) == 0 and len(self.vertices) == 0:
            return [set()]
        connected = []
        # connected are 0-2 and 1-3
        for c in self.crossings:
            connected.append((c[0], c[2]))
            connected.append((c[1], c[-1]))
        # vertex connects edges
        for v in self.vertices:
            connected.append(tuple(v))
        return self.find_connections(connected)

    def find_loops(self):
        vertices = list(self.abstract_graph.keys())
        for v1, v2 in combinations(vertices,2):
            print(v1,v2,list(self.find_path(v1,v2)))
            for pot_loop in combinations([path for path in self.find_path(v1, v2)], 2):
                if not set(pot_loop[0]) & set(pot_loop[1]):
                    self.loops.append(pot_loop[0]+list(reversed(pot_loop[1])))
        return self.loops

    def find_thetas(self):
        vertices = list(self.abstract_graph.keys())
        for k in range(len(vertices)):
            v1 = vertices[k]
            for l in range(k):
                v2 = vertices[l]
                for pot_loop in combinations([path for path in self.find_path(v1, v2)], 3):
                    if not set(pot_loop[0]) & set(pot_loop[1]) and not(set(pot_loop[2]) & set(pot_loop[1])) and not(set(pot_loop[0]) & set(pot_loop[2])):
                        self.thetas.append([v1, v2, list(pot_loop)])
        return self.thetas

    def find_connections(self, array):
        out = []
        while len(array) > 0:
            first, rest = array[0], array[1:]
            first = set(first)
            lf = -1
            while len(first) > lf:
                lf = len(first)
                rest2 = []
                for r in rest:
                    if len(first.intersection(set(r))) > 0:
                        first |= set(r)
                    else:
                        rest2.append(r)
                rest = rest2
            out.append(first)
            array = rest
        return out

    def find_reidemeister_1(self, num_cross=-1):
        # num_cross is the number of crossings to be returned
        crossings = []
        for k in range(len(self.crossings)):
            c = self.crossings[k]
            for i in range(4):
                if c[i - 1] == c[i]:  # crossing to be reduced:
                    crossings.append([k, i])
                    break
            if len(crossings) == num_cross:
                return crossings
        return crossings

    def find_reidemeister_1v(self, num_cross=-1):
        # num_cross is the number of crossings to be returned
        crossings = []
        for l in range(len(self.crossings)):
            c = self.crossings[l]
            for k in range(len(self.vertices)):
                v = self.vertices[k]
                if len(v) == 2:
                    for i in range(4):
                        if [c[i], c[i-1]] == v or [c[i-1], c[i]] == v:
                            crossings.append([l,i,k])
                            break
            if len(crossings) == num_cross:
                return crossings
        return crossings

    def find_reidemeister_2(self, num_cross=-1):
        # num_cross is the number of crossings to be returned
        crossings = []
        for k in range(len(self.crossings)):
            c1 = self.crossings[k]
            for j in range(k):
                c2 = self.crossings[j]
                for i in range(4):
                    if c1[i] == c2[i] and c1[i-1] == c2[i-3]:
                        crossings.append([k, j, c1[i], c1[i-1]])
                        break
                    elif c1[i] == c2[i] and c1[i-3] == c2[i-1]:
                        crossings.append([k, j, c1[i], c1[i-3]])
                        break
                if len(crossings) == num_cross:
                    return crossings
        return crossings

    def find_reidemeister_2v(self, num_cross=-1):
        # num_cross is the number of crossings to be returned
        crossings = []
        for l in range(len(self.vertices)):
            v = self.vertices[l]
            if len(v) == 2:
                for k in range(len(self.crossings)):
                    c1 = self.crossings[k]
                    for j in range(k):
                        c2 = self.crossings[j]
                        for i in range(4):
                            if c1[i] == c2[i] and ([c1[i-1], c2[i-3]] == v or [c2[i-3], c1[i-1]] == v):
                                crossings.append([k, j, c1[i], l])
                                break
                            elif c1[i-1] == c2[i-3] and ([c1[i], c2[i]] == v or [c2[i], c1[i]] == v):
                                crossings.append([k, j, c1[i-1], l])
                                break
                            elif c1[i] == c2[i] and ([c1[i-3], c2[i-1]] == v or [c2[i-1], c1[i-3]] == v):
                                crossings.append([k, j, c1[i], l])
                                break
                            elif c1[i-3] == c2[i-1] and ([c1[i], c2[i]] == v or [c2[i], c1[i]] == v):
                                crossings.append([k, j, c1[i-3], l])
                                break
                        if len(crossings) == num_cross:
                            return crossings
        return crossings

    def find_reidemeister_3(self, num_cross=-1):
        # num_cross is the number of crossings to be returned
        crossings = []
        for i in range(len(self.crossings)):
            for j in range(i):
                for k in range(j):
                    c1, c2, c3 = self.crossings[i], self.crossings[j], self.crossings[k]
                    for m in range(4):
                        # checking if the crosings form a triangle
                        if c1[m] in c3 and c1[m - 1] in c2 and c3[(c3.index(c1[m]) - 3) % 4] in c2:
                            c3, c2 = c2, c3
                        if c1[m] in c2 and c1[m - 1] in c3 and c2[(c2.index(c1[m]) - 3) % 4] in c3:
                            # the edges have to be consecutive counterclockwise
                            if c3.index(c1[m-1]) - c3.index(c2[(c2.index(c1[m]) - 3) % 4]) not in (1, -3):
                                continue
                            comm12 = c1[m]
                            comm13 = c1[m - 1]
                            comm23 = c2[(c2.index(c1[m]) - 3) % 4]
                            if (1,1) not in [(c1.index(comm12)%2, c2.index(comm12)%2), (c1.index(comm13)%2, c3.index(comm13)%2), (c2.index(comm23)%2, c3.index(comm23)%2)]:
                                continue
                            crossings.append([self.crossings.index(c1), self.crossings.index(c2), self.crossings.index(c3), comm12, comm13, comm23])
                            break
                    if len(crossings) == num_cross:
                        return crossings
        return crossings

    def find_reidemeister_4(self, num_cross=-1):
        # num_cross is the number of crossings to be returned
        crossings = []
        for i in range(len(self.crossings)):
            for j in range(i):
                for k in range(len(self.vertices)):
                    c1, c2, v = self.crossings[i], self.crossings[j], self.vertices[k]
                    if len(v) != 3:
                        continue
                    for l in range(3):
                        if v[l] in c2 and v[l-1] in c1:
                            c1, c2 = c2, c1
                        if v[l] in c1 and v[l-1] in c2:
                            i1 = (c1.index(v[l]) - 3) % 4
                            i2 = (c2.index(v[l-1]) - 1) % 4
                            if c1[i1] == c2[i2] and (i1 % 2) == (i2 % 2):
                                comm12 = c1[i1]
                                comm1v = v[l]
                                comm2v = v[l-1]
                                crossings.append([k, self.crossings.index(c1), self.crossings.index(c2), comm12, comm1v, comm2v])
                                break
                    if len(crossings) == num_cross:
                        return crossings
        return crossings

    def find_reidemeister_5(self, num_cross=-1):
        # num_cross is the number of crossings to be returned
        crossings = []
        for k in range(len(self.crossings)):
            c = self.crossings[k]
            for j in range(len(self.vertices)):
                v = self.vertices[j]
                if len(v) != 3:
                    continue
                for i in range(4):
                    if c[i] in v and c[i-1] in v and abs(v.index(c[i])-v.index(c[i-1])) in [1,len(v)-1]:
                        if i % 2 == 0:
                            crossings.append([j, k, i, i-1])
                        else:
                            crossings.append([j, k, i-1, i])
                        break
                if len(crossings) == num_cross:
                    return crossings
        return crossings


    ### manipulation ###
    def reidemeister_1(self, arg_list, debug=False):
        ci, i = arg_list
        # ci is the index of the crossing to be reduced
        # i is the index of the edge in the crossing to be reduced
        # so self.crossings[ci][i] == self.crossings[ci][i-1]
        trans = {self.crossings[ci][i-2]: self.crossings[ci][i-3]}
        if i % 2 == 1:
            n = 1
        else:
            n = -1
        if debug:
            print("Reidemeister 1:\tRemoving crossing " + str(self.crossings[ci]) + ". Updating: " + str(trans) + ". Sign " + str(n) + ".")
        self.crossings.pop(ci)
        self.update(trans)
        if debug:
            print("\tResult: " + self.get_pdcode())
        return n

    def reidemeister_1v(self, arg_list, debug=False):
        ci, i, vi = arg_list
        # ci is the index of the crossing to be reduced
        # i is the index of the edge in the crossing to be reduced
        # vi is the index of the vertex to be removed
        # so self.crossings[ci][i] == self.crossings[ci][i-1]
        if i % 2 == 1:
            n = 1
        else:
            n = -1
        v0 = self.vertices[vi]
        v = [self.crossings[ci][i-2], self.crossings[ci][i-3]]
        if debug:
            print("Reidemeister 1:\tRemoving crossing " + str(self.crossings[ci]) + ". Swapping vertices: " + str(v0) + " -> " + str(v) + ". Sign " + str(n) + ".")
        self.crossings.pop(ci)
        self.vertices.pop(vi)
        self.vertices.append(v)
        self.update()
        if debug:
            print("\tResult: " + self.get_pdcode())
        return n

    def reidemeister_2(self, arg_list, debug=False):
        c1, c2, comm1, comm2 = arg_list
        # c1 and c2 are the indices of the crossings to be reduced
        # comm1 and comm2 are the common edges in the crossings
        cross1 = self.crossings[c1]
        cross2 = self.crossings[c2]
        if cross1[cross1.index(comm1)-2] == cross1[cross1.index(comm2)-2]:
            cross2, cross1 = cross1, cross2
        v1 = [cross1[cross1.index(comm1)-2].strip(), cross2[cross2.index(comm1)-2].strip()]
        v2 = [cross1[cross1.index(comm2)-2].strip(), cross2[cross2.index(comm2)-2].strip()]
        trans = {cross1[cross1.index(comm1)-2]: cross2[cross2.index(comm1)-2],
                  cross1[cross1.index(comm2)-2]: cross2[cross2.index(comm2)-2]}
        if debug:
            print("Reidemeister 2:\tRemoving crossings " + str(self.crossings[c1]) + ", " + str(self.crossings[c2]) + ". "
                "Adding vertices: V" + str(v1) + " and V" + str(v2) + ".")
            #Updating: " + str(trans) + "." + str(v1) + ' ' + str(v2))
        for cross in list(reversed(sorted([c1, c2]))):
            self.crossings.pop(cross)
        self.vertices.append(v1)
        self.vertices.append(v2)
        self.update()
        self.remove_double_verts()
        # self.update(trans)
        if debug:
            print("\tResult: " + self.get_pdcode())
        return

    def reidemeister_2v(self, arg_list, debug=False):
        c1, c2, comm, vi = arg_list
        # c1 and c2 are the indices of the crossings to be reduced
        # comm1 and comm2 are the common edges in the crossings
        # vi is the index of vertex to be removed
        cross1 = self.crossings[c1]
        cross2 = self.crossings[c2]
        v = self.vertices[vi]
        if cross1[cross1.index(comm)-2] == cross1[cross1.index(comm)-2]:
            cross2, cross1 = cross1, cross2
        if v[1] in cross1:
            v = [v[1],v[0]]
        v1 = [cross1[cross1.index(comm)-2].strip(), cross2[cross2.index(comm)-2].strip()]
        v2 = [cross1[cross1.index(v[0])-2].strip(), cross2[cross2.index(v[1])-2].strip()]

        if debug:
            print("Reidemeister 2v:\tRemoving crossings " + str(self.crossings[c1]) + ", " + str(self.crossings[c2]) + ", and vertex " + str(self.vertices[vi]) + ". Adding vertices: V" + str(v1) + " and V" + str(v2) + ".")
            #Updating: " + str(trans) + "." + str(v1) + ' ' + str(v2))
        for cross in list(reversed(sorted([c1, c2]))):
            self.crossings.pop(cross)
        self.vertices.pop(vi)
        self.vertices.append(v1)
        self.vertices.append(v2)
        self.update()
        self.remove_double_verts()
        # self.update(trans)
        if debug:
            print("\tResult: " + self.get_pdcode())
        return

    def reidemeister_3(self, arg_list, debug=False):
        c1, c2, c3, comm12, comm13, comm23 = arg_list
        # c1, c2, c3 are the indices of the crossings to be reduced
        # comm12, comm13, and comm23 are the common edges between the crossings
        cross1 = self.crossings[c1]
        cross2 = self.crossings[c2]
        cross3 = self.crossings[c3]

        # new crossings
        cn1 = [c for c in cross1]
        cn1[cross1.index(comm12)-2] = cross2[cross2.index(comm12)-2]
        cn1[cross1.index(comm13)-2] = cross3[cross3.index(comm13)-2]
        cn2 = [c for c in cross2]
        cn2[cross2.index(comm12)-2] = cross1[cross1.index(comm12)-2]
        cn2[cross2.index(comm23)-2] = cross3[cross3.index(comm23)-2]
        cn3 = [c for c in cross3]
        cn3[cross3.index(comm13)-2] = cross1[cross1.index(comm13)-2]
        cn3[cross3.index(comm23)-2] = cross2[cross2.index(comm23)-2]

        if debug:
            print("Reidemeister 3:\tRemoving crossing " + str(self.crossings[c1]) + ", " + str(self.crossings[c2]) + ", " + str(self.crossings[c3]) + ". Adding: " + str(cn1) + ", " + str(cn2) + ", " + str(cn3) + ".")

        # updating the list of crossings
        for i in list(reversed(sorted([c3, c2, c1]))):
            self.crossings.pop(i)
        for c in [cn1, cn2, cn3]:
            self.crossings.append(c)
        self.update_pdcode()
        if debug:
            print("\tResult: " + self.get_pdcode())
        return

    def reidemeister_4(self, arg_list, debug=False):
        vi, c1, c2, comm12, comm1v, comm2v = arg_list
        # vi, c1, and c2 are the indices of the vertex and edges to be reduced
        # comm12, comm1v, and comm2v are the edges common between the crossings and crossings and vertex

        cross1 = self.crossings[c1]
        cross2 = self.crossings[c2]
        v = self.vertices[vi]
        miss = list(set(v) - {comm1v, comm2v})[0]       # TODO generalize for large number of crossings

        if (cross1.index(comm12) % 2) == 1:     # crosing over
            c = [miss, cross2[cross2.index(comm12)-2], comm12, cross1[cross1.index(comm12)-2]]
        else:                           # crossing under
            c = [cross2[cross2.index(comm12)-2], comm12, cross1[cross1.index(comm12) - 2], miss]
        vn = [comm12, cross2[cross2.index(comm2v)-2], cross1[cross1.index(comm1v)-2]]

        # updating data
        if debug:
            print("Reidemeister 4:\tRemoving crossing " + str(self.crossings[c1]) + ", " + str(self.crossings[c2]) + " and vertex " + str(self.vertices[vi]) + ". Adding crossing: " + str(c) + " and vertex " + str(vn) + ".")

        for cross in list(reversed(sorted([c1, c2]))):
            self.crossings.pop(cross)
        self.vertices.pop(vi)
        self.crossings.append(c)
        self.vertices.append(vn)
        self.update_pdcode()
        if debug:
            print("\tResult: " + self.get_pdcode())
        return

    def reidemeister_5(self, arg_list, debug=False):
        vi, ci, i, j = arg_list
        # vi and ci are indices of the vertex and the crossing to be reduced
        # i and j are the indices of the edges in the crossing adjacent to the vertex
        # i is the undercrossing, j is the uppercrossing

        vert = self.vertices[vi]
        cross = self.crossings[ci]

        # new vertex
        vn = [v for v in vert]
        vn[vn.index(cross[i])] = cross[j-2]
        vn[vn.index(cross[j])] = cross[i-2]
        if i < j:
            n = 1
        else:
            n = -1

        if debug:
            print("Reidemeister 5:\tRemoving crossing " + str(self.crossings[ci]) + ". Updating vertex " + str(self.vertices[vi]) + "->" + str(vn) + ". Sign " + str(n) + ".")

        self.crossings.pop(ci)
        self.vertices.pop(vi)
        self.vertices.append(vn)
        self.update_pdcode()
        if debug:
            print("\tResult: " + self.get_pdcode())
        return n

    def invert_crossing(self, crossing):
        g = deepcopy(self)
        g.crossings.append(g.crossings[crossing][1:] + [g.crossings[crossing][0]])
        g.crossings.pop(crossing)
        g.update_pdcode()
        return g

    def smooth_crossing(self, crossing, smoothing):
        # Smoothings denote the connection of edges. The edges are joined by two-valent vertices.
        # The unnecessary vertices are subsequently reduced.
        g = deepcopy(self)

        if smoothing == 0:
            g.vertices.append(g.crossings[crossing])
        if smoothing == 1:
            g.vertices.append(g.crossings[crossing][:2])
            g.vertices.append(g.crossings[crossing][2:4])
        if smoothing == -1:
            g.vertices.append([g.crossings[crossing][0], g.crossings[crossing][3]])
            g.vertices.append(g.crossings[crossing][1:3])

        # cleaning
        g.crossings.pop(crossing)
        g.remove_double_verts()

        # TODO handle missing loops
        return g

    def contract_edge(self, edge, debug=False):
        g = deepcopy(self)
        nvert = []
        to_remove = []
        e = str(edge)
        for k in range(len(g.vertices)):      # to keep the orientation
            # TODO check the list additions
            if e in g.vertices[k]:
                to_remove.append(k)
                if nvert:
                    nvert += g.vertices[k][g.vertices[k].index(e)+1:] + g.vertices[k][:g.vertices[k].index(e)]
                    break
                else:
                    nvert = g.vertices[k][g.vertices[k].index(e) + 1:] + g.vertices[k][:g.vertices[k].index(e)]
        for k in list(reversed(to_remove)):
            g.vertices.pop(k)
        g.vertices.append(nvert)
        g.update_pdcode()
        return g

    def contract_edge_vertex(self, v, c, i):
        g = deepcopy(self)
        vert = g.vertices[v]
        cross = g.crossings[c]
        vert[vert.index(cross[i])] = cross[i-3]
        vert[vert.index(cross[i-1])] = cross[i-2]
        g.vertices[v] = vert
        g.crossings.pop(c)
        return g

    def remove_edge(self, edge, debug=False):
        g = deepcopy(self)
        for v in g.vertices:
            if edge in v:
                v.pop(v.index(edge))
        g.edges.discard(edge)
        g.remove_double_verts()
        g.update_pdcode()
        return g

    def remove_loop(self,v,k):
        g = deepcopy(self)
        g.vertices[v].pop(k)
        g.vertices[v].pop(k-1)
        g.remove_double_verts()
        return g

    def remove_edge_vertex(self, v, c, i):
        g = deepcopy(self)
        cross = g.crossings[c]
        to_remove = list(reversed(sorted([g.vertices[v].index(cross[i]), g.vertices[v].index(cross[i - 1])])))
        for k in to_remove:
            g.vertices[v].pop(k)
        trans = {cross[i - 2]: cross[i - 3]}
        g.crossings.pop(c)
        g.update(trans)
        return g

    def remove_double_verts(self):
        split_double_vertices = []
        trans = {}
        for component in self.find_connected_components():
            verts = []
            other_verts = False  # if there exists any vertex with valency > 2
            for k in range(len(self.vertices) - 1, -1, -1):
                vert = self.vertices[k]
                if any(v in component for v in vert):
                    if len(vert) > 2:
                        other_verts = True
                        continue
                    verts.append(k)
            if not other_verts:
                verts = verts[:-1]
            split_double_vertices.append(verts)

        # bulding translating dictionary
        for vert_list in split_double_vertices:
            for k in vert_list:
                vert = sorted(self.vertices[k])
                if vert[1] in trans.keys():
                    trans[vert[0]] = trans[vert[1]]
                elif vert[1] in [trans[key] for key in list(trans)]:
                    for key in list(trans):
                        if trans[key] == vert[1]:
                            trans[key] = vert[0]
                            break
                elif vert[0] in trans.keys():
                    for key in list(trans):
                        if key == vert[0]:
                            trans[vert[1]] = trans[key]
                else:
                    trans[vert[1]] = vert[0]

        # removing unnecessary vertices
        for vert_list in list(reversed(sorted(split_double_vertices))):
            for vert in vert_list:
                self.vertices.pop(vert)

        # updating
        self.update(trans)
        return

    def update(self, trans={}):
        # filling in the untranslated edges
        for key in self.edges:
            if key not in trans.keys():
                trans[key] = key

        # making the translation
        self.crossings = [[trans[c[i]] for i in range(4)] for c in self.crossings]
        self.vertices = [[trans[v[i]] for i in range(len(v))] for v in self.vertices]
        self.update_pdcode()
        return

    def close(self, method='two_points', direction=0):
        if method == 'closed':
            return
        for k in range(len(self.coordinates_W)):
            self.coordinates_W[k] = chain_close(self.coordinates_W[k], method, direction)
        self.coords2em()
        self.em2pd()
        self.generate_vertices()
        self.generate_crossings()
        self.generate_edges()
        # self.remove_double_verts()
        self.generate_identifier()
        return

    def reduce(self, method='kmt'):
        for k in range(len(self.coordinates_W)):
            self.coordinates_W[k] = chain_reduce(self.coordinates_W[k], method)
        self.coords2em()
        self.em2pd()
        self.generate_vertices()
        self.generate_crossings()
        self.generate_edges()
        # self.remove_double_verts()
        self.generate_identifier()
        return

    ### simplification ###
    def simplify(self, method='Reidemeister', steps=1000, debug=False):
        # returns the power from Reidemeister moves 1 and 5
        # TODO implement moves 4.2, 4.3 and 4.4 from Yamada's paper!
        n = 0
        if method == 'Easy':
            return self.simplify_reidemeister_deterministic(debug)
        if method == 'Reidemeister':
            return self.simplify_reidemeister(steps,debug)

    def simplify_reidemeister(self, steps=1000, debug=False):
        n = 0
        steps = 0
        previous = [set([tuple(x) for x in self.vertices]), set([tuple(x) for x in self.crossings])]
        n += self.simplify_reidemeister_deterministic(debug)
        for step in range(steps):
            changed = False
            # do a R3 move if it reduces the number of crossings or a random R3 move, which will not restore some previous graph
            crossings = self.find_reidemeister_3()
            if not crossings:
                break
            done = False  # if the move was done
            for cross in crossings:
                g = deepcopy(self)
                g.reidemeister_3(cross, debug=False)
                g.simplify_reidemeister_deterministic(debug=False)
                if len(g.crossings) < len(self.crossings):
                    self.reidemeister_3(cross, debug)
                    previous.append([set([tuple(x) for x in self.vertices]), set([tuple(x) for x in self.crossings])])
                    n += self.simplify_reidemeister_deterministic(debug)
                    done = True
                    changed = True
                    break
            if not done:
                random.shuffle(crossings)
                for cross in crossings:
                    g = deepcopy(self)
                    g.reidemeister_3(cross, debug=False)
                    data = [set([tuple(x) for x in g.vertices]), set([tuple(x) for x in g.crossings])]
                    if data not in previous:
                        self.reidemeister_3(cross, debug=debug)
                        previous.append(
                            [set([tuple(x) for x in self.vertices]), set([tuple(x) for x in self.crossings])])
                        changed = True
                        break
                n += self.simplify_reidemeister_deterministic(debug)
            if not changed:
                break
        return n

    def simplify_reidemeister_deterministic(self, debug=False):
        n = 0
        k = len(self.crossings) + 1
        while len(self.crossings) < k:
            k = len(self.crossings)
            for arg_list in list(reversed(self.find_reidemeister_1())):
                n += 2 * self.reidemeister_1(arg_list, debug=debug)
            for arg_list in list(reversed(self.find_reidemeister_1v(num_cross=1))):
                n += 2 * self.reidemeister_1v(arg_list, debug=debug)
            for arg_list in self.find_reidemeister_2(num_cross=1):
                self.reidemeister_2(arg_list, debug=debug)
            for arg_list in self.find_reidemeister_2v(num_cross=1):
                self.reidemeister_2v(arg_list, debug=debug)
            for arg_list in self.find_reidemeister_4(num_cross=1):
                self.reidemeister_4(arg_list, debug=debug)
            for arg_list in list(reversed(self.find_reidemeister_1())):
                n += 2 * self.reidemeister_1(arg_list, debug=debug)
            for arg_list in list(reversed(self.find_reidemeister_1v(num_cross=1))):
                n += 2 * self.reidemeister_1v(arg_list, debug=debug)
            for arg_list in self.find_reidemeister_5(num_cross=1):
                n += self.reidemeister_5(arg_list, debug=debug)
        return n

    def simplify_sono(self):
        return

    def simplify_knot_pull(self):
        return

    def simplify_kmt(self):
        return

    def idealize(self):
        return


    ### calculations ###
    def invariant(self, invariant, closure='two_points', tries=200, direction=0, reduce_method='kmt', matrix=False,
                  density=1, level=0, max_cross=15, chirality=False, cuda=True, beg=-1, end=-1, debug=False):
        # TODO after transcribing the class to C and writting methods for other polynomials for CUDA, make a general
        # function, not calculation of the matrix separatelly in each polynomial function...

        if invariant not in available_invariants:
            raise AttributeError('The chosen invariant not supported (yet?). The available invariants: ' + str(available_invariants))

        if invariant == 'alexander' and matrix and cuda and check_cuda():
            return self.alexander_cuda(closure=closure, tries=tries, direction=direction, reduce=reduce_method,
                               density=density, level=level, debug=debug)
        result = {}
        additional = []
        if closure == 'closed':
            tries = 1
        for subgraph in self.generate_subchain(matrix=matrix, density=density, beg=beg, end=end):
            statistics = []
            print(min(subgraph.coordinates.keys()),max(subgraph.coordinates.keys()))
            for k in range(tries):
                res = subgraph.point_invariant(invariant=invariant,
                                               closure=closure, direction=direction, reduce=reduce_method, debug=debug)
                statistics.append(res)
            res = self.analyze_statistics(statistics, level=level)
            if res != 0:
                additional.append(subgraph.identifier)
                result[subgraph.identifier] = res
        if additional and density > 1:
            for subgraph in self.generate_subchain_detailed(additional, density=density):
                statistics = []
                for k in range(tries):
                    res = subgraph.point_invariant(invariant=invariant,
                                                   closure=closure, direction=direction, reduce=reduce_method,
                                                   debug=debug)
                    statistics.append(res)
                result[subgraph.identifier] = self.analyze_statistics(statistics, level=level)
        if len(result) == 1:
            key = list(result.keys())[0]
            result = result[key]
        return result

    def point_invariant(self, invariant, closure='two_points', direction=0, reduce='kmt', debug=False):
        g = deepcopy(self)
        print("coordinates:")
        print(g.coordinates_W[0])
        g.close(method=closure, direction=direction)
        print("closed:")
        print(g.coordinates_W[0])
        print("reduced:")
        g.reduce(method=reduce)
        print(g.coordinates_W[0])

        res = ''
        if invariant == 'alexander':
            res = 'Alexander: ' + str(g.point_alexander(debug=debug).print_short().split('|')[1].strip())
        elif invariant == 'conway':
            res = 'Conway: ' + str(g.point_conway(debug=debug).print_short().split('|')[1].strip())
        elif invariant == 'jones':
            res = 'Jones: ' + str(g.point_jones(debug=debug).print_short())
        elif invariant == 'homfly':
            res = 'HOMFLY-PT: ' + str(g.point_homfly(debug=debug))
        elif invariant == 'yamada':
            res = 'Yamada: ' + str(g.point_yamada(debug=debug).print_short().split('|')[1].strip())
        elif invariant == 'kauffman_bracket':
            res = 'Kauffman bracket: ' + str(g.point_kauffman_bracket(debug=debug).print_short().split('|')[1].strip())
        elif invariant == 'kauffman_polynomial':
            res = 'Kauffman polynomial: ' + str(g.point_kauffman_polynomial(debug=debug).print_short())
        elif invariant == 'blmho':
            res = 'BLM/Ho: ' + str(g.point_blmho(debug=debug).print_short())
        elif invariant == 'aps':
            res = 'APS: ' + str(g.point_aps(debug=debug))
        elif invariant == 'gln':
            res = 'GLN: ' + str(g.point_gln(debug=debug))
        elif invariant == 'writhe':
            res = 'Writhe: ' + str(g.point_writhe(debug=debug))
        return res

    def alexander_cuda(self, closure='two_points', tries=200, direction=0, reduce='kmt',
                               density=1, level=0, debug=False):
        closure_int = closures[closure]
        matrix = find_alexander_fingerprint_cuda(self.coordinates_W[0], density, level, closure_int, tries)
        return

    def alexander(self, matrix=False, closure='two_points', tries=200, direction=0, reduce='kmt',
                  density=1, level=0, debug=False):
        result = {}
        additional = []
        if closure == 'closed':
            tries = 1
        for subgraph in self.generate_subchain(matrix=matrix, density=density):
            statistics = []
            for k in range(tries):
                g = deepcopy(subgraph)
                g.close(method=closure, direction=direction)
                g.reduce(method=reduce)
                statistics.append('Alexander: ' + str(g.point_alexander(debug=debug).print_short().split('|')[1].strip()))
            res = self.analyze_statistics(statistics, level=level)
            if res != 0:
                additional.append(subgraph.identifier)
            result[subgraph.identifier] = res
        if additional and density > 1:
            for subgraph in self.generate_subchain_detailed(additional, density=density):
                statistics = []
                for k in range(tries):
                    g = deepcopy(subgraph)
                    g.close(method=closure, direction=direction)
                    g.reduce(method=reduce)
                    statistics.append('Alexander: ' + str(g.point_alexander(debug=debug).print_short().split('|')[1].strip()))
                result[subgraph.identifier] = self.analyze_statistics(statistics, level=level)
        if len(result) == 1:
            key = list(result.keys())[0]
            result = result[key]
        return result

    def conway(self, matrix=False, closure='two_points', tries=200, direction=0, reduce='kmt',
                  density=1, level=0, debug=False):
        result = {}
        additional = []
        if closure == 'closed':
            tries = 1
        for subgraph in self.generate_subchain(matrix=matrix, density=density):
            statistics = []
            for k in range(tries):
                g = deepcopy(subgraph)
                g.close(method=closure, direction=direction)
                g.reduce(method=reduce)
                statistics.append('Conway: ' + str(g.point_conway(debug=debug).print_short().split('|')[1].strip()))
            res = self.analyze_statistics(statistics, level=level)
            if res != 0:
                additional.append(subgraph.identifier)
            result[subgraph.identifier] = res
        if additional and density > 1:
            for subgraph in self.generate_subchain_detailed(additional, density=density):
                statistics = []
                for k in range(tries):
                    g = deepcopy(subgraph)
                    g.close(method=closure, direction=direction)
                    g.reduce(method=reduce)
                    statistics.append('Conway: ' + str(g.point_conway(debug=debug).print_short().split('|')[1].strip()))
                result[subgraph.identifier] = self.analyze_statistics(statistics, level=level)
        if len(result) == 1:
            key = list(result.keys())[0]
            result = result[key]
        return result

    def jones(self, matrix=False, closure='two_points', tries=200, direction=0, reduce='kmt',
                  density=1, level=0, debug=False):
        result = {}
        additional = []
        if closure == 'closed':
            tries = 1
        for subgraph in self.generate_subchain(matrix=matrix, density=density):
            statistics = []
            for k in range(tries):
                g = deepcopy(subgraph)
                g.close(method=closure, direction=direction)
                g.reduce(method=reduce)
                statistics.append('Jones: ' + str(g.point_jones(debug=debug).print_short()))
            res = self.analyze_statistics(statistics, level=level)
            if res != 0:
                additional.append(subgraph.identifier)
            result[subgraph.identifier] = res
        if additional and density > 1:
            for subgraph in self.generate_subchain_detailed(additional, density=density):
                statistics = []
                for k in range(tries):
                    g = deepcopy(subgraph)
                    g.close(method=closure, direction=direction)
                    g.reduce(method=reduce)
                    statistics.append('Jones: ' + str(g.point_jones(debug=debug).print_short()))
                result[subgraph.identifier] = self.analyze_statistics(statistics, level=level)
        if len(result) == 1:
            key = list(result.keys())[0]
            result = result[key]
        return result

    def homfly(self, matrix=False, closure='two_points', tries=200, direction=0, reduce='kmt',
                  density=1, level=0, debug=False):
        result = {}
        additional = []
        if closure == 'closed':
            tries = 1
        for subgraph in self.generate_subchain(matrix=matrix, density=density):
            statistics = []
            for k in range(tries):
                g = deepcopy(subgraph)
                g.close(method=closure, direction=direction)
                g.reduce(method=reduce)
                statistics.append('HOMFLY-PT: ' + str(g.point_homfly(debug=debug)))
            res = self.analyze_statistics(statistics, level=level)
            if res != 0:
                additional.append(subgraph.identifier)
            result[subgraph.identifier] = res
        if additional and density > 1:
            for subgraph in self.generate_subchain_detailed(additional, density=density):
                statistics = []
                for k in range(tries):
                    g = deepcopy(subgraph)
                    g.close(method=closure, direction=direction)
                    g.reduce(method=reduce)
                    statistics.append('HOMFLY-PT: ' + str(g.point_homfly(debug=debug)))
                result[subgraph.identifier] = self.analyze_statistics(statistics, level=level)
        if len(result) == 1:
            key = list(result.keys())[0]
            result = result[key]
        return result

    def yamada(self, matrix=False, closure='two_points', tries=200, direction=0, reduce='kmt',
                  density=1, level=0, debug=False):
        result = {}
        additional = []
        if closure == 'closed':
            tries = 1
        for subgraph in self.generate_subchain(matrix=matrix, density=density):
            statistics = []
            for k in range(tries):
                g = deepcopy(subgraph)
                g.close(method=closure, direction=direction)
                g.reduce(method=reduce)
                res = g.point_yamada(debug=debug)
                if not isinstance(res,str):
                    res = str(res.print_short().split('|')[1].strip())
                statistics.append('Yamada: ' + res)
            res = self.analyze_statistics(statistics, level=level)
            if res != 0:
                additional.append(subgraph.identifier)
            result[subgraph.identifier] = res
        if additional and density > 1:
            for subgraph in self.generate_subchain_detailed(additional, density=density):
                statistics = []
                for k in range(tries):
                    g = deepcopy(subgraph)
                    g.close(method=closure, direction=direction)
                    g.reduce(method=reduce)
                    res = g.point_yamada(debug=debug)
                    if not isinstance(res, str):
                        res = str(res.print_short().split('|')[1].strip())
                    statistics.append('Yamada: ' + res)
                    result[subgraph.identifier] = self.analyze_statistics(statistics, level=level)
        if len(result) == 1:
            key = list(result.keys())[0]
            result = result[key]
        return result

    def kauffman_bracket(self, matrix=False, closure='two_points', tries=200, direction=0, reduce='kmt',
                  density=1, level=0, debug=False):
        result = {}
        additional = []
        if closure == 'closed':
            tries = 1
        for subgraph in self.generate_subchain(matrix=matrix, density=density):
            statistics = []
            for k in range(tries):
                g = deepcopy(subgraph)
                g.close(method=closure, direction=direction)
                g.reduce(method=reduce)
                statistics.append('Kauffman bracket: ' + str(g.point_kauffman_bracket(debug=debug).print_short().split('|')[1].strip()))
            res = self.analyze_statistics(statistics, level=level)
            if res != 0:
                additional.append(subgraph.identifier)
            result[subgraph.identifier] = res
        if additional and density > 1:
            for subgraph in self.generate_subchain_detailed(additional, density=density):
                statistics = []
                for k in range(tries):
                    g = deepcopy(subgraph)
                    g.close(method=closure, direction=direction)
                    g.reduce(method=reduce)
                    statistics.append('Kauffman bracket: ' + str(g.point_kauffman_bracket(debug=debug).print_short().split('|')[1].strip()))
                result[subgraph.identifier] = self.analyze_statistics(statistics, level=level)
        if len(result) == 1:
            key = list(result.keys())[0]
            result = result[key]
        return result

    def kauffman_polynomial(self, matrix=False, closure='two_points', tries=200, direction=0, reduce='kmt',
                  density=1, level=0, debug=False):
        result = {}
        additional = []
        if closure == 'closed':
            tries = 1
        for subgraph in self.generate_subchain(matrix=matrix, density=density):
            statistics = []
            for k in range(tries):
                g = deepcopy(subgraph)
                g.close(method=closure, direction=direction)
                g.reduce(method=reduce)
                statistics.append('Kauffman polynomial: ' + str(g.point_kauffman_polynomial(debug=debug).print_short()))
            res = self.analyze_statistics(statistics, level=level)
            if res != 0:
                additional.append(subgraph.identifier)
            result[subgraph.identifier] = res
        if additional and density > 1:
            for subgraph in self.generate_subchain_detailed(additional, density=density):
                statistics = []
                for k in range(tries):
                    g = deepcopy(subgraph)
                    g.close(method=closure, direction=direction)
                    g.reduce(method=reduce)
                    statistics.append('Kauffman polynomial: ' + str(g.point_kauffman_polynomial(debug=debug).print_short()))
                result[subgraph.identifier] = self.analyze_statistics(statistics, level=level)
        if len(result) == 1:
            key = list(result.keys())[0]
            result = result[key]
        return result

    def blmho(self, matrix=False, closure='two_points', tries=200, direction=0, reduce='kmt',
                  density=1, level=0, debug=False):
        result = {}
        additional = []
        if closure == 'closed':
            tries = 1
        for subgraph in self.generate_subchain(matrix=matrix, density=density):
            statistics = []
            for k in range(tries):
                g = deepcopy(subgraph)
                g.close(method=closure, direction=direction)
                g.reduce(method=reduce)
                statistics.append('BLM/Ho: ' + str(g.point_blmho(debug=debug).print_short()))
            res = self.analyze_statistics(statistics, level=level)
            if res != 0:
                additional.append(subgraph.identifier)
            result[subgraph.identifier] = res
        if additional and density > 1:
            for subgraph in self.generate_subchain_detailed(additional, density=density):
                statistics = []
                for k in range(tries):
                    g = deepcopy(subgraph)
                    g.close(method=closure, direction=direction)
                    g.reduce(method=reduce)
                    statistics.append('BLM/Ho: ' + str(g.point_blmho(debug=debug).print_short()))
                result[subgraph.identifier] = self.analyze_statistics(statistics, level=level)
        if len(result) == 1:
            key = list(result.keys())[0]
            result = result[key]
        return result

    def aps(self, matrix=False, closure='two_points', tries=200, direction=0, reduce='kmt',
                  density=1, level=0, debug=False):
        result = {}
        additional = []
        if closure == 'closed':
            tries = 1
        for subgraph in self.generate_subchain(matrix=matrix, density=density):
            statistics = []
            for k in range(tries):
                g = deepcopy(subgraph)
                g.close(method=closure, direction=direction)
                g.reduce(method=reduce)
                statistics.append('APS: ' + str(g.point_aps(debug=debug)))
            res = self.analyze_statistics(statistics, level=level)
            if res != 0:
                additional.append(subgraph.identifier)
            result[subgraph.identifier] = res
        if additional and density > 1:
            for subgraph in self.generate_subchain_detailed(additional, density=density):
                statistics = []
                for k in range(tries):
                    g = deepcopy(subgraph)
                    g.close(method=closure, direction=direction)
                    g.reduce(method=reduce)
                    statistics.append('APS: ' + str(g.point_aps(debug=debug)))
                result[subgraph.identifier] = self.analyze_statistics(statistics, level=level)
        if len(result) == 1:
            key = list(result.keys())[0]
            result = result[key]
        return result

    def gln(self, matrix=False, closure='two_points', tries=200, direction=0, reduce='kmt',
                  density=1, level=0, debug=False):
        result = {}
        additional = []
        if closure == 'closed':
            tries = 1
        for subgraph in self.generate_subchain(matrix=matrix, density=density):
            statistics = []
            for k in range(tries):
                g = deepcopy(subgraph)
                g.close(method=closure, direction=direction)
                g.reduce(method=reduce)
                statistics.append('GLN: ' + str(g.point_gln(debug=debug)))
            res = self.analyze_statistics(statistics, level=level)
            if res != 0:
                additional.append(subgraph.identifier)
            result[subgraph.identifier] = res
        if additional and density > 1:
            for subgraph in self.generate_subchain_detailed(additional, density=density):
                statistics = []
                for k in range(tries):
                    g = deepcopy(subgraph)
                    g.close(method=closure, direction=direction)
                    g.reduce(method=reduce)
                    statistics.append('GLN: ' + str(g.point_gln(debug=debug)))
                result[subgraph.identifier] = self.analyze_statistics(statistics, level=level)
        if len(result) == 1:
            key = list(result.keys())[0]
            result = result[key]
        return result

    def writhe(self, matrix=False, closure='two_points', tries=200, direction=0, reduce='kmt',
                  density=1, level=0, debug=False):
        result = {}
        additional = []
        if closure == 'closed':
            tries = 1
        for subgraph in self.generate_subchain(matrix=matrix, density=density):
            statistics = []
            for k in range(tries):
                g = deepcopy(subgraph)
                g.close(method=closure, direction=direction)
                g.reduce(method=reduce)
                statistics.append('Writhe: ' + str(g.point_writhe(debug=debug)))
            res = self.analyze_statistics(statistics, level=level)
            if res != 0:
                additional.append(subgraph.identifier)
            result[subgraph.identifier] = res
        if additional and density > 1:
            for subgraph in self.generate_subchain_detailed(additional, density=density):
                statistics = []
                for k in range(tries):
                    g = deepcopy(subgraph)
                    g.close(method=closure, direction=direction)
                    g.reduce(method=reduce)
                    statistics.append('Writhe: ' + str(g.point_writhe(debug=debug)))
                result[subgraph.identifier] = self.analyze_statistics(statistics, level=level)
        if len(result) == 1:
            key = list(result.keys())[0]
            result = result[key]
        return result

    def point_alexander(self, debug=False):
        p_red = calc_alexander_poly(self.coordinates_W[0])
        # TODO is it the right condition?
        if not p_red:
            p_red = '1'
        coefs = p_red.split()
        if int(coefs[0]) < 0:
            coefs = [str(-int(_)) for _ in coefs]
        p = Poly('0')
        for k in range(len(coefs)):
            power = k - int((len(coefs)-1)/2)
            p += Poly(coefs[k]) * Poly('x**' + str(power))
        return p

    def point_conway(self, debug=False):
        com1 = ''
        com2 = ''
        if debug:
            if self.level > 0:
                for k in range(self.level - 1):
                    com1 += '|  '
                    com2 += '|  '
                com1 += '|->'
                com2 += '|  '
            com1 += self.communicate + self.get_pdcode()
            print(com1)
        # calculating Jones polynomial

        n = self.simplify(debug=debug)  # returns power of x as a result of 1st and 5th Reidemeister move
        if debug:
            print(com2 + "After simplification: " + self.get_pdcode() + '\tn=' + str(n))

        # known cases, to speed up calculations:
        if self.get_pdcode() in self.known.keys() and self.known[self.get_pdcode()]:
            res = self.known[self.get_pdcode()]
            if debug:
                print(com2 + 'Known case.')
                print(com2 + "Result " + self.communicate + str(res))
            return res
        if len(self.vertices) == 1 and not self.crossings:  # bouquet of circles:
            # number of circles in bouquet = len(set(graph.vertices[0]))
            self.known[self.get_pdcode()] = Poly('1')
            res = self.known[self.get_pdcode()]
            if debug:
                print(com2 + "It's a circle.")
            return res
        if len(self.vertices) == 2 and not self.crossings:  # bouquet of circles:
            # number of circles in bouquet = len(set(graph.vertices[0]))
            self.known[self.get_pdcode()] = Poly('0')
            res = self.known[self.get_pdcode()]
            if debug:
                print(com2 + "It's a split sum of two circles.")
            return res

        # split sum:
        subgraphs = self.create_disjoined_components()
        if len(subgraphs) > 1:
            if debug:
                print(com2 + "It's a split graph.")
                for subgraph in subgraphs:
                    print(subgraph.pdcode)
            self.known[self.get_pdcode()] = Poly('0')
            res = self.known[self.get_pdcode()]
            if debug:
                print(com2 + 'Result ' + str(res) + '\t(n=' + str(n) + ').')
            return res

        # crossing reduction:
        if len(self.crossings) > 0:
            # the skein relation
            k = random.randint(0, len(self.crossings) - 1)
            sign = self.find_crossing_sign(k)
            if debug:
                print(com2 + "Reducing crossing " + str(self.crossings[k]) + " by skein relation. It is " +
                      str(sign) + " crossing.")
            g1 = self.smooth_crossing(k, sign)
            g1.communicate = str(sign) + 'x*'
            g1.level += 1
            part1 = g1.point_conway(debug=debug)
            self.known = g1.known

            g2 = self.invert_crossing(k)
            g2.communicate = ' + '
            g2.level += 1
            part2 = g2.point_conway(debug=debug)
            self.known = g2.known

            self.known[self.get_pdcode()] = Poly(str(sign)) * Poly('x') * part1 + part2
            res = self.known[self.get_pdcode()]
            if debug:
                print(com2 + 'Result ' + str(res) + '\t(n=' + str(n) + ').')
            return res

        self.known[self.get_pdcode()] = Poly('1')
        res = Poly('1')  # no crossing, no vertex = empty graph
        if debug:
            print(com2 + "Empty graph. Result " + str(res))
        return

    def point_jones(self, debug=False):
        com1 = ''
        com2 = ''
        if debug:
            if self.level > 0:
                for k in range(self.level - 1):
                    com1 += '|  '
                    com2 += '|  '
                com1 += '|->'
                com2 += '|  '
            com1 += self.communicate + self.get_pdcode()
            print(com1)
        # calculating Jones polynomial

        n = self.simplify(debug=debug)  # returns power of x as a result of 1st and 5th Reidemeister move
        if debug:
            print(com2 + "After simplification: " + self.get_pdcode() + '\tn=' + str(n))

        # known cases, to speed up calculations:
        if self.get_pdcode() in self.known.keys() and self.known[self.get_pdcode()]:
            res = self.known[self.get_pdcode()]
            if debug:
                print(com2 + 'Known case.')
                print(com2 + "Result " + self.communicate + str(res))
            return res
        if len(self.vertices) == 1 and not self.crossings:  # bouquet of circles:
            # number of circles in bouquet = len(set(graph.vertices[0]))
            self.known[self.get_pdcode()] = Poly('1')
            res = self.known[self.get_pdcode()]
            if debug:
                print(com2 + "It's a circle.")
            return res
        if len(self.vertices) == 2 and not self.crossings:  # bouquet of circles:
            # number of circles in bouquet = len(set(graph.vertices[0]))
            self.known[self.get_pdcode()] = Poly('-t**0.5-t**-0.5')
            res = self.known[self.get_pdcode()]
            if debug:
                print(com2 + "It's a split sum of two circles.")
            return res

        # split sum:
        subgraphs = self.create_disjoined_components()
        if len(subgraphs) > 1:
            if debug:
                print(com2 + "It's a split graph.")
                for subgraph in subgraphs:
                    print(subgraph.pdcode)
            self.known[self.get_pdcode()] = Poly('1')
            for k in range(len(subgraphs)):
                subgraph = subgraphs[k]
                subgraph.level = self.level + 1
                subgraph.known = self.known
                subgraph.communicate = ' * '
                res_tmp = subgraph.point_jones(debug=debug)
                self.known = subgraph.known
                self.known[self.get_pdcode()] *= res_tmp
            self.known[self.get_pdcode()] *= Poly('-t**0.5-t**-0.5')
            res = self.known[self.get_pdcode()]
            if debug:
                print(com2 + 'Result ' + str(res) + '\t(n=' + str(n) + ').')
            return res

        # crossing reduction:
        if len(self.crossings) > 0:
            # the skein relation
            k = random.randint(0,len(self.crossings)-1)
            sign = self.find_crossing_sign(k)
            if debug:
                print(com2 + "Reducing crossing " + str(self.crossings[k]) + " by skein relation. It is " +
                      str(sign) + " crossing.")
            g1 = self.smooth_crossing(k, sign)
            g1.communicate = str(sign) + '*t^' + str(sign) + '(t^0.5 - t^-0.5)*'
            g1.level += 1
            part1 = g1.point_jones(debug=debug)
            self.known = g1.known

            g2 = self.invert_crossing(k)
            g2.communicate = ' +t^' + str(2*sign) + '* '
            g2.level += 1
            part2 = g2.point_jones(debug=debug)
            self.known = g2.known

            self.known[self.get_pdcode()] = Poly(str(sign)) * Poly('t**0.5-t**-0.5') * Poly('t**' + str(sign)) * part1 + Poly('t**' + str(2*sign)) * part2
            res = self.known[self.get_pdcode()]
            if debug:
                print(com2 + 'Result ' + str(res) + '\t(n=' + str(n) + ').')
            return res

        self.known[self.get_pdcode()] = Poly('1')
        res = Poly('1')  # no crossing, no vertex = empty graph
        if debug:
            print(com2 + "Empty graph. Result " + str(res))
        return

    def point_homfly(self, debug=False):
        code = self.emcode.replace(';','\n')
        print()             # TODO WTF? With this print it works?
        res = lmpoly(code.encode('utf-8')).replace('\n','|')
        return res

    def point_yamada(self, max_crossings=10, debug=False):
        com1 = ''
        com2 = ''
        if debug:
            if self.level > 0:
                for k in range(self.level - 1):
                    com1 += '|  '
                    com2 += '|  '
                com1 += '|->'
                com2 += '|  '
            com1 += self.communicate + self.get_pdcode()
            print(com1)
        # calculating Yamada polynomial

        n = self.simplify(debug=debug)  # returns power of x as a result of 1st and 5th Reidemeister move
        if len(self.crossings) > max_crossings:
            return "Too many crossings."
        if debug:
            print(com2 + "After simplification: " + self.get_pdcode() + '\tn=' + str(n))

        # known cases, to speed up calculations:
        if self.get_pdcode() in self.known.keys() and self.known[self.get_pdcode()]:
            res = self.known[self.get_pdcode()] * Poly(str((-1) ** (n % 2)) + 'x^' + str(n))
            if debug:
                print(com2 + 'Known case.')
                print(com2 + "Result " + self.communicate + str(res))
            return res
        if len(self.vertices) == 1 and not self.crossings:  # bouquet of circles:
            # number of circles in bouquet = len(set(graph.vertices[0]))
            self.known[self.get_pdcode()] = Poly(-1) * (
                        Poly('-x-1-x^-1') ** len(set([x.strip() for x in self.vertices[0]])))
            res = self.known[self.get_pdcode()] * Poly(str((-1) ** (n % 2)) + 'x^' + str(n))
            if debug:
                print(com2 + "It's a bouquet of " + str(
                    len(set([x.strip() for x in
                             self.vertices[0]]))) + " circles.\n" + com2 + "Result " + self.communicate + str(res))
            return res
        if len(self.vertices) == 2 and not self.crossings and len(self.vertices[1]) == 3:
            if set([x.strip() for x in self.vertices[0]]) == set(
                    [x.strip() for x in self.vertices[1]]):  # trivial theta
                self.known[self.get_pdcode()] = Poly('-x^2-x-2-x^-1-x^-2')
                res = self.known[self.get_pdcode()] * Poly(str((-1) ** (n % 2)) + 'x^' + str(n))
                if debug:
                    print(com2 + "It's a trivial theta.\n" + com2 + "Result " + self.communicate + str(res))
                return res
            elif len(set([x.strip() for x in self.vertices[0]]) & set(
                    [x.strip() for x in self.vertices[1]])) == 1:  # trivial handcuff
                self.known[self.get_pdcode()] = Poly('0')
                res = self.known[self.get_pdcode()]
                if debug:
                    print(com2 + "It's a trivial handcuff graph.\n" + com2 + "Result " + str(res))
                return res

        # other simplifying cases
        for v in range(len(self.vertices)):
            vert = self.vertices[v]
            if len(vert) > 3:
                for k in range(len(vert)):
                    if vert[k] == vert[k - 1]:
                        # bouquet with one loop
                        if debug:
                            print(com2 + "Removing loop.")
                        g = self.remove_loop(v, k)
                        g.level += 1
                        g.communicate = ' * '
                        res_tmp = g.point_yamada(debug=debug)
                        self.known = g.known

                        self.known[self.get_pdcode()] = Poly('-1') * Poly('x+1+x^-1') * res_tmp
                        res = self.known[self.get_pdcode()] * Poly(str((-1) ** (n % 2)) + 'x^' + str(n))
                        if debug:
                            print(com2 + 'Result ' + str(res) + '\t(n=' + str(n) + ').')
                        return res

        # split sum:
        subgraphs = self.create_disjoined_components()
        if len(subgraphs) > 1:
            if debug:
                print(com2 + "It's a split graph.")
            self.known[self.get_pdcode()] = Poly('1')
            for k in range(len(subgraphs)):
                subgraph = subgraphs[k]
                subgraph.level = self.level + 1
                subgraph.known = self.known
                subgraph.communicate = ' * '
                res_tmp = subgraph.point_yamada(debug=debug)
                self.known = subgraph.known
                self.known[self.get_pdcode()] *= res_tmp

            res = self.known[self.get_pdcode()] * Poly(str((-1) ** (n % 2)) + 'x^' + str(n))
            if debug:
                print(com2 + 'Result ' + str(res) + '\t(n=' + str(n) + ').')

            return res

        # crossing reduction:
        if len(self.crossings) > 0:
            # two ways of removing the crossing.
            g = self.invert_crossing(0)
            g.simplify()
            if len(g.crossings) < len(self.crossings):
                # the skein-like relation
                if debug:
                    print(com2 + "Reducing crossing " + str(self.crossings[0]) + " by skein relation.")
                g1 = self.smooth_crossing(0, 1)
                g1.communicate = ' (x-x^-1)* '
                g1.level += 1
                part1 = g1.point_yamada(debug=debug)
                self.known = g1.known

                g2 = self.smooth_crossing(0, -1)
                g2.communicate = ' -(x-x^-1)* '
                g2.level += 1
                part2 = g2.point_yamada(debug=debug)
                self.known = g2.known

                g3 = self.invert_crossing(0)
                g3.communicate = ' + '
                g3.level += 1
                part3 = g3.point_yamada(debug=debug)
                self.known = g3.known

                self.known[self.get_pdcode()] = Poly('x-x^-1') * (part1 - part2) + part3
                res = Poly(str((-1) ** (n % 2)) + 'x^' + str(n)) * self.known[self.get_pdcode()]
                if debug:
                    print(com2 + 'Result ' + str(res) + '\t(n=' + str(n) + ').')
                return res
            else:
                # removing the crossing with introduction of new vertex
                if debug:
                    print(com2 + "Reducing crossing " + str(self.crossings[0]) + " by crossing removal.")
                g1 = self.smooth_crossing(0, 1)
                g1.level += 1
                g1.communicate = ' x* '
                part1 = g1.point_yamada(debug=debug)
                self.knonw = g1.known

                g2 = self.smooth_crossing(0, -1)
                g2.level += 1
                g2.communicate = ' +x^-1* '
                part2 = g2.point_yamada(debug=debug)
                self.knonw = g2.known

                g3 = self.smooth_crossing(0, 0)
                g3.level += 1
                g3.communicate = ' + '
                part3 = g3.point_yamada(debug=debug)
                self.knonw = g3.known

                self.known[self.get_pdcode()] = Poly('x') * part1 + Poly('x^-1') * part2 + part3
                res = self.known[self.get_pdcode()] * Poly(str((-1) ** (n % 2)) + 'x^' + str(n))
                if debug:
                    print(com2 + 'Result ' + str(res) + '\t(n=' + str(n) + ').')

                return res

        # edge reduction:
        edges = self.get_noloop_edges()
        if len(edges) > 0:  # then len(graph.vertices) >= 2
            if debug:
                print(com2 + "Reducing noloop edge " + str(edges[0]) + ".")
            g1 = self.remove_edge(edges[0])
            g1.level += 1
            g1.communicate = ''
            part1 = g1.point_yamada(debug=debug)
            self.known = g1.known

            g2 = self.contract_edge(edges[0])
            g2.level += 1
            g2.communicate = ' + '
            part2 = g2.point_yamada(debug=debug)
            self.known = g2.known

            self.known[self.get_pdcode()] = part1 + part2
            res = self.known[self.get_pdcode()] * Poly(str((-1) ** (n % 2)) + 'x^' + str(n))
            if debug:
                print(com2 + 'Result ' + str(res) + '\t(n=' + str(n) + ').')
            return res

        self.known[self.get_pdcode()] = Poly('1')
        res = Poly(str((-1) ** (n % 2)) + 'x^' + str(n))  # no crossing, no vertex = empty graph
        if debug:
            print(com2 + "Empty graph. Result " + str(res))
        return res

    def point_kauffman_bracket(self, B='A**-1', d='-A**2-A**-2', debug=False):
        # calculating Kaufman Bracket polynomial

        res = Poly('0')
        n = len(self.crossings)
        for state in product([-1,1],repeat=n):
            a = int((n + sum(state))/2)
            b = int((n - sum(state))/2)
            g = deepcopy(self)
            for smooth in state:
                g = g.smooth_crossing(0,smooth)
            parta = Poly('A**' + str(a))
            partb = Poly('B**' + str(b))
            partd = Poly('d**' + str(len(g.vertices)-1))
            res += parta * partb * partd
        res = res({'B': B, 'd': d})
        return res

    def point_kauffman_polynomial(self, debug=False):
        n = self.simplify(debug=debug)
        l = self.point_writhe()
        res = Poly('a**' + str(-l))
        res *= self.KauffmanPolynomial_L(debug=debug)
        return res

    def KauffmanPolynomial_L(self, debug=False):
        com1 = ''
        com2 = ''
        if debug:
            if self.level > 0:
                for k in range(self.level - 1):
                    com1 += '|  '
                    com2 += '|  '
                com1 += '|->'
                com2 += '|  '
            com1 += self.communicate + self.get_pdcode()
            print(com1)
        # calculating Yamada polynomial

        n = int(self.simplify(debug=debug)/2)  # returns power of x as a result of 1st and 5th Reidemeister move
        if debug:
            print(com2 + "After simplification: " + self.get_pdcode() + '\tn=' + str(n))

        # known cases, to speed up calculations:
        if self.get_pdcode() in self.known.keys() and self.known[self.get_pdcode()]:
            res = self.known[self.get_pdcode()] * Poly('a^' + str(n))
            if debug:
                print(com2 + 'Known case.')
                print(com2 + "Result " + self.communicate + str(res))
            return res
        if len(self.vertices) == 1 and not self.crossings:  # bouquet of circles:
            # number of circles in bouquet = len(set(graph.vertices[0]))
            self.known[self.get_pdcode()] = Poly(1)
            res = self.known[self.get_pdcode()] * Poly('a^' + str(n))
            if debug:
                print(com2 + "It's a bouquet of " + str(
                    len(set([x.strip() for x in
                             self.vertices[0]]))) + " circles.\n" + com2 + "Result " + self.communicate + str(res))
            return res
        if len(self.vertices) == 2 and not self.crossings:
            self.known[self.get_pdcode()] = Poly('a+a**-1-z') * Poly('z**-1')
            res = self.known[self.get_pdcode()] * Poly('a^' + str(n))
            if debug:
                print(com2 + "It's a split sum of two circles.\n" + com2 + "Result " + self.communicate + '(' + str(res) + ')')
            return res

        # split sum:
        subgraphs = self.create_disjoined_components()
        if len(subgraphs) > 1:
            if debug:
                print(com2 + "It's a split graph.")
            self.known[self.get_pdcode()] = Poly('1')
            for k in range(len(subgraphs)):
                subgraph = subgraphs[k]
                subgraph.level += 1
                subgraph.known = self.known
                subgraph.communicate = ' * '
                res_tmp = subgraph.KauffmanPolynomial_L(debug=debug)
                self.known = subgraph.known
                self.known[self.get_pdcode()] *= res_tmp
            self.known[self.get_pdcode()] *= Poly('a+a**-1-z')*Poly('z**-1')
            res = self.known[self.get_pdcode()] * Poly('a^' + str(n))
            if debug:
                print(com2 + 'Result ' + str(res) + '\t(n=' + str(n) + ').')
            return res

        # crossing reduction:
        if len(self.crossings) > 0:
            # two ways of removing the crossing.
            g = self.invert_crossing(0)
            g.simplify()
            if len(g.crossings) < len(self.crossings):
                # the skein-like relation
                if debug:
                    print(com2 + "Reducing crossing " + str(self.crossings[0]) + " by skein relation.")
                g1 = self.smooth_crossing(0, 1)
                g1.communicate = ' z* '
                g1.level += 1
                part1 = g1.KauffmanPolynomial_L(debug=debug)
                self.known = g1.known

                g2 = self.smooth_crossing(0, -1)
                g2.communicate = ' +z* '
                g2.level += 1
                part2 = g2.KauffmanPolynomial_L(debug=debug)
                self.known = g2.known

                g3 = self.invert_crossing(0)
                g3.communicate = ' - '
                g3.level += 1
                part3 = g3.KauffmanPolynomial_L(debug=debug)
                self.known = g3.known

                self.known[self.get_pdcode()] = Poly('z') * (part1 + part2) - part3
                res = self.known[self.get_pdcode()] * Poly('a^' + str(n))
                if debug:
                    print(com2 + 'Result ' + str(res) + '\t(n=' + str(n) + ').')
                return res

        self.known[self.get_pdcode()] = Poly('1')
        res = self.known[self.get_pdcode()]  # no crossing, no vertex = empty graph
        if debug:
            print(com2 + "Empty graph. Result " + str(res))
        return res


    def point_blmho(self, debug=False):
        res = self.KauffmanPolynomial_L(debug=debug)
        res = res({'a': 1, 'z': 'x'})
        if debug:
            print('After substitution: ' + str(res))
        return res

    def point_writhe(self, debug=False):
        res = sum([self.find_crossing_sign(k) for k in range(len(self.crossings))])
        return res

    ### plotting ###
    def plot(self):
        # matplotlib.use('TkAgg')
        # fig = plt.figure()
        # ax = plt.axes(projection="3d")
        # for k in range(len(self.arcs)):
        #     arc = self.arcs[k]
        #     X = np.array([float(self.coordinates[_][0]) for _ in arc])
        #     Y = np.array([float(self.coordinates[_][1]) for _ in arc])
        #     Z = np.array([float(self.coordinates[_][2]) for _ in arc])
        #     if len(self.arcs) == 1:
        #         ax.scatter3D(X,Y,Z,c=np.array(range(len(arc))),cmap='hsv')
        #     else:
        #         ax.plot3D(X,Y,Z,plot_colors[k])
        # plt.show()
        return

    def plot_projection(self):
        return

    def plot_matrix(self):
        return

    ### printing ###
    def to_txt(self, numbers=True):
        return

    def to_json(self):
        return

    def print_info(self):
        return

    ### others ###
    def identify(self):
        return

    def is_virtual(self):
        return

    def find_path(self, start, end):
        fringe = [(start, [])]
        while fringe:
            state, path = fringe.pop()
            if path and state == end:
                yield path
                continue
            for next_state, edge in self.abstract_graph[state]:
                if edge in path:
                    continue
                if next_state == start:
                    continue
                fringe.append((next_state, path+[edge]))
        return

    def generate_subchain(self, matrix=False, density=1, beg=-1, end=-1):
        if not matrix:
            return [self.cut_chain(beg,end)]
        subgraphs = []
        beg = max(min(list(self.coordinates.keys())),beg)
        end = max(max(list(self.coordinates.keys())),end)
        for k in range(beg, end+1, density):
            for l in range(beg, k-5, density):
                subgraphs.append(self.cut_chain(beg=l, end=k))
        return subgraphs

    def analyze_statistics(self, statistics, level=0):
        counter = {}
        if len(statistics) == 0:
            counter[0] = 1
        else:
            for e in statistics:
                v = str(e)
                if v not in counter.keys():
                    counter[v]=0
                counter[v] += 1
            for v in counter.keys():
                counter[v] = float(counter[v])/len(statistics)
        # TODO make it better
        for key in counter.keys():
            val = key.split(':')[1].strip()
            if val == '1' and counter[key] >= 1-level:
                return 0
        return counter

    def generate_subchain_detailed(self, additional, density=1):
        if not additional:
            return []

    def cut_chain(self,beg=-1,end=-1):
        if beg < 0:
            beg = min(list(self.coordinates.keys()))
        if end < 0:
            end = max(list(self.coordinates.keys()))
        coords = [[key] + self.coordinates[key] for key in range(beg, end+1)]
        return Graph([coords])