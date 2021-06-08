'''
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''

# do NOT import ways. This should be done from other files
# simply import your modules and call the appropriate functions

from Ucs import ucs_rout
import time

from Ucs import calculateCostFunctionUcs

import idastar
import astar


def find_ucs_rout(source, target):
    resultedPath = ucs_rout(source, target)
    for item in resultedPath:
        print(item.state, end=' ')

    return resultedPath


def find_astar_route(source, target):

    res = astar.find_route(source, target)
    for item in res:
        print(item, end=' ')


def find_idastar_route(source, target):
    return idastar.find_route(source, target)


def dispatch(argv):
    from sys import argv
    source, target = int(argv[2]), int(argv[3])

    if argv[1] == 'ucs' or argv[1] == 'UCS':
        path = find_ucs_rout(source, target)
    elif argv[1] == 'astar' or argv[1] == 'ASTAR':
        # call get randome souce and random target
        find_astar_route(source, target)
    elif argv[1] == 'idastar' or argv[1] == 'IDASTAR':
        path = find_idastar_route(source, target)
        print(path)


if __name__ == '__main__':
    from sys import argv
    dispatch(argv)
