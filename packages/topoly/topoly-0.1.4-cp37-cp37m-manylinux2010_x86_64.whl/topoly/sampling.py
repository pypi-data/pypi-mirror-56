"""
The module with the functions for sampling of the polymers.

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

from itertools import product, permutations
import random

def generate_loop(n, equilateral=True):
    # generating the loop of length n beads
    return

def generate_lasso(n_loop, n_tail, equilateral=True):
    # generating the lasso with n_loop beads in the loop and n_tail in the tail
    return

def generate_theta(n1, n2, n3, equilateral=True):
    # generating the theta-curve with n1, n2 and n3 beads in the arcs
    return

def generate_braid(strings, crossings, n=-1, returns=False):
    # generating the one-dimensional braid representation on a given number of strings and number of crossings
    # n is the number of braids to be returned (-1 denotes all).
    # returns is the boolean parameter allowing for arc connecting.
    # TODO add filtering only non-trivial braids
    braids = []
    for braid in product(range(-strings+1, strings, 1), repeat=crossings):
        if 0 not in list(braid):
            braids.append(' '.join([str(x) for x in list(braid)]))
    if n > 0:
        random.shuffle(braids)
        braids = braids[:n]
    return braids