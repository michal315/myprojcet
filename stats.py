'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''
import collections
from collections import namedtuple

from myRoads import ROADS
from ways import load_map_from_csv
from statistics import mean
import serchForRandomNodes
from Ucs import ucs_rout
from Ucs import calculateCostFunctionUcs

import astar

def map_statistics(roads):
    #print('****roads is :', roads[1])
    '''return a dictionary containing the desired information
    You can edit this function as you wish'''
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])

    road_links = str((roads['links'] for road in roads))

    links_counter = len([link for link in (roads.iterlinks())])
    # calculate max and min degree
    maxOutBranch = 0
    minOutBranch = -1
    avgOutBranch = 0
    i = 0
    j = 0
    maxDistance = 0
    minDistance = 0
    avgDistance = 0
    for links in roads.junctions():
        i = i + 1
        avgOutBranch += len(links[3])

        if (maxOutBranch < len(links[3])):
            maxOutBranch = len(links[3])
        if (minOutBranch > len(links[3]) or minOutBranch < 0):
            minOutBranch = len(links[3])

    avgOutBranch = avgOutBranch / i

    ppp = roads.junctions()

    flat_links = []
    for links in roads.iterlinks():
        flat_links.append(links.highway_type)
        links_distance = links.distance
        j = j + 1
        avgDistance += links_distance
        if (maxDistance < links_distance):
            maxDistance = links_distance;
        if (minDistance > links_distance):
            minDistance = links_distance

    avgDistance = avgDistance / j

    return {
        'Number of junctions': len(roads),
        'Number of links': links_counter,
        'Outgoing branching factor': Stat(max=maxOutBranch, min=minOutBranch, avg=avgOutBranch),
        'Link distance': Stat(max=maxDistance, min=minDistance, avg=avgDistance),
        # value should be a dictionary
        # mapping each road_info.TYPE to the no' of links of this type
        'Link type histogram': collections.Counter(flat_links)  # tip: use collections.Counter

    }








def print_stats():
    for k, v in map_statistics(ROADS).items():
        print('{}: {}'.format(k, v))


if __name__ == '__main__':
    from sys import argv

    assert len(argv) == 1
    print_stats()
    serchForRandomNodes.CreateGraph(ROADS)


    #find_ucs_rout(30, 55, calculateCostFunctionUcs)
