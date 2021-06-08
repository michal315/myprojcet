from ways import load_map_from_csv, compute_distance
from collections import namedtuple
import ways.info as info
import heapq
import myRoads

SearchParams = namedtuple('SearchParams', 'heuristic links w')
max_speed = max(max(t) for t in info.SPEED_RANGES)


def calculateCostFunctionUcs(distanceFromNode, typeOfRoad):
    maxSpeed = max(info.SPEED_RANGES[typeOfRoad])
    cost = (1000 * distanceFromNode) / maxSpeed
    return cost


def find_route(start, goal):

    roads = myRoads.ROADS

    goal_node = roads[goal]

    def heuristic(node_index):

        node = roads[node_index]
        distance = compute_distance(
            node.lat, node.lon, goal_node.lat, goal_node.lon)
        return distance / max_speed

    def links(node_index):
        node = roads[node_index]
        return node.links

    def speed(link):
        dist = link.distance
        speed_range = info.SPEED_RANGES[link.highway_type]
        return dist / max(speed_range)

    search_params = SearchParams(heuristic, links, speed)
    return idastar(start, goal, search_params)


INFINITY = 1000000000
FOUND = 'FOUND'


def idastar(start, goal, P):
    bound = P.heuristic(start)
    path = [start]

    while True:
        t = search(goal, path, 0, bound, P)
        if t == FOUND:
            calculateTotalCost(path)
            return path
        if t == INFINITY:
            return None
        bound = t


def search(goal, path, g, bound, P):
    node = path[-1]

    f = g + P.heuristic(node)

    if f > bound:
        return f
    if node == goal:
        return FOUND

    _min = INFINITY
    for link in P.links(node):
        neighbor = link.target
        if neighbor not in path:
            path.append(neighbor)

            t = search(goal, path, g + P.w(link), bound, P)
            if t == FOUND:
                return FOUND
            if t < _min:
                _min = t
            path.pop()

    return _min


def h(node_index, goal):

    node = myRoads.ROADS[node_index]
    goal_node = myRoads.ROADS[goal]
    distance = compute_distance(
        node.lat,
        node.lon,
        goal_node.lat,
        goal_node.lon)
    return distance / max_speed


def printToFile(cost):
    with open("results/IDAStarRuns.txt", "a") as text_file:
        text_file.write(" {0}".format(cost))


def calculateTotalCost(path):
    total = 0
    start = path[0]
    goal = path[-1]
    current_junction = myRoads.ROADS[start]
    for item in path[1:]:

        for link in current_junction[3]:
            if(link[1] == item):
                # the distance between the two nodes
                distanceFromNode = link[2]
                roadType = link[3]
                #  maxSpeed=max(info.SPEED_RANGES[link[3]])
                cost = calculateCostFunctionUcs(
                    distanceFromNode, roadType) + h(item, goal)
                total = total + cost
                current_junction = myRoads.ROADS[item]

        printToFile(total)
