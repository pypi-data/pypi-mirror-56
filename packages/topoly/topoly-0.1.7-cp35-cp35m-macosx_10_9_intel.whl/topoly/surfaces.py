"""
The module with functions for spanning and analyzing the minimal surfaces.

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

def find_lasso(curve, begin=0, end=-1, reduce=True, bridgedist=3, enddist=3, piercedist=10, debug=True):
    # calculate the lasso type for a curve with one bridge
    return

def find_piercings(loop, tail, reduce=True, bridgedist=3, enddist=3, piercedist=10, debug=True):
    # calculate the lasso type for a given loop and tail
    return

def calculate_GLN(curve1, curve2):
    # calculate the Gauss Linking Number between curve1 and curve2
    return

def lasso_smooth(curve, begin=0, end=-1):
    # smooth the structure, keeping the lasso type fixed
    return

def find_all_lassos(curve, bridges, reduce=True, bridgedist=3, enddist=3, piercedist=10, debug=True):
    # find all piercings through all closed loops, closed by bridges given
    return