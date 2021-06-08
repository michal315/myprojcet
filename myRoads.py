from statistics import mean
from ways.Node import Node
from ways import load_map_from_csv, compute_distance, info
from ways.draw import plot_path
from ways.info import ROAD_TYPES, SPEED_RANGES
#from ways.draw import   plot_path
import matplotlib.pyplot as plt
ROADS = load_map_from_csv()
MAX_SPEED = max(max(t) for t in info.SPEED_RANGES)


def cost(link):
    dist = link.distance
    speed_range = info.SPEED_RANGES[link.highway_type]
    return dist / max(speed_range)


def get_childs(state):
    result = []
    for link in ROADS[state][3]:
        result.append((link[1], cost(link)))
    return result


def hccs(node, target):
    current_junction = ROADS[node.state]
    # print('current_ junction :',roads[node.state])
    neighbors = []

    for link in current_junction[3]:

        #  maxSpeed=max(info.SPEED_RANGES[link[3]])
        cost = heuristic_function(link[1], target)
        newNode = Node(link[1], node, cost)  # child

        neighbors.append(newNode)

    return neighbors


def heuristic_function(state, target):
    state_road = ROADS[state]
    target_road = ROADS[target]

    distance = compute_distance(
        state_road.lat,
        state_road.lon,
        target_road.lat,
        target_road.lon)

    return distance / MAX_SPEED


def plotPath(path):
    print("path:", path)
    plot_path(ROADS, path)
