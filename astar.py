from ways import load_map_from_csv, compute_distance
from collections import namedtuple
import ways.info as info
import heapq
import myRoads
import matplotlib.pyplot as plt

SearchParams = namedtuple('SearchParams', 'heuristic links w')

max_speed = max(max(t) for t in info.SPEED_RANGES)


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
    return astar(start, goal, search_params)


def reconstruct_path(cameFrom, current, gScore, P):
    total_path = [current]
    total_cost_of_path = 0
    H = []
    G = []
    while current in cameFrom:
        current = cameFrom[current]
        total_path.insert(0, current)
        total_cost_of_path = total_cost_of_path + gScore[current]

    printToFile(total_cost_of_path)

    return total_path


def printToFile(cost):
    with open("results/AStarRuns.txt", "a") as text_file:
        text_file.write(" {0}".format(cost))


def astar(start, goal, P):
    INFINITY = 1000000000
    openSet = PrioritySet()
    cameFrom = dict()

    gScore = {start: 0}
    fScore = {start: P.heuristic(start)}

    openSet.add(start, fScore[start])

    # while openset not empty
    while not openSet.empty():
        current = openSet.get()
        if current == goal:
            # plt.xlabel('H')
            # naming the y axis
            # plt.ylabel('G')

            # plt.show()
            return reconstruct_path(cameFrom, current, gScore, P)

        for link in P.links(current):
            neighbor = link.target
            tentative_cost = gScore.get(current, INFINITY) + P.w(link)
            if tentative_cost < gScore.get(neighbor, INFINITY):
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_cost
                fScore[neighbor] = gScore[neighbor] + P.heuristic(neighbor)
                #plt.plot(P.heuristic(neighbor), gScore[neighbor], 'or')
                if neighbor not in openSet:
                    openSet.add(neighbor, fScore[neighbor])

    return None


class PrioritySet(object):
    def __init__(self):
        self.heap = []
        self.set = set()

    def add(self, d, pri):
        if d not in self.set:
            heapq.heappush(self.heap, (pri, d))
            self.set.add(d)

    def get(self):
        pri, d = heapq.heappop(self.heap)
        self.set.remove(d)
        return d

    def __contains__(self, item):
        return item in self.set

    def empty(self):
        return len(self.heap) == 0
