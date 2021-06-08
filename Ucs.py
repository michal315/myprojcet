import csv
import math

import myRoads
from myRoads import get_childs, heuristic_function, hccs
from ways.Node import Node
from ways import info, compute_distance
from ways.PriorityQueue import PriorityQueue

new_limit = math.inf


# Function to sort the list of tuples by its second item
def Sort_Tuple(tup):
    # getting length of list of tuples
    lst = len(tup)
    for i in range(0, lst):

        for j in range(0, lst - i - 1):
            if (tup[j]['cost'] > tup[j + 1]['cost']):
                temp = tup[j]
                tup[j] = tup[j + 1]
                tup[j + 1] = temp
    return tup


def make_node(state, parent, cost, h=0):
    node = {'stat': state, 'cost': cost, 'parent': parent}
    return node


def writeTotalCostFromSourceToDest(total_cost):
    with open('UCSRuns.txt', mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(total_cost)


def calculateCostFunctionUcs(distanceFromNode, typeOfRoad):
    maxSpeed = max(info.SPEED_RANGES[typeOfRoad])
    cost = (1000 * distanceFromNode) / maxSpeed
    return cost


def returnCostNode(node):
    return node['cost']


def expand_junction(roads, node, calculateCostFunctionUcs):
    current_junction = roads[node.state]
    # print('current_ junction :',roads[node.state])
    neighbors = []

    for link in current_junction[3]:
        distanceFromNode = link[2]  # the distance between the two nodes
        roadType = link[3]
        #  maxSpeed=max(info.SPEED_RANGES[link[3]])
        cost = calculateCostFunctionUcs(distanceFromNode, roadType)
        newNode = Node(link[1], node, cost)  # child
        neighbors.append(newNode)

    return neighbors


def createChildren(Roads, junction_id, parent, calculateCostFunctionUcs):
    current_junction = Roads[junction_id]
    neighbors = []

    for link in current_junction[3]:
        distanceFromNode = link[2]  # the distance between the two nodes
        roadType = link[3]
        #  maxSpeed=max(info.SPEED_RANGES[link[3]])
        cost = calculateCostFunctionUcs(distanceFromNode, roadType)
        g_node = parent['g'] + cost

    # h_node = compute_distance(lat1, lon1, lat2, lon2) #lat1 is of the father , lat2 is of the chile ( node-> link[1])
    # f_node =g_node+h_node

    # node = {'stat': link[1], 'f': f_node,'g':cost,'h': h_node,'perant': parent}

    #  neighbors.append(node)

    return neighbors


def f(node):
    return node.cost


def ucs_rout(init_state, goal_state):

    node = Node(init_state)
    frontier = PriorityQueue(f)  # Priority Queue
    frontier.append(node)
    closed_list = set()
    while frontier:
        if len(closed_list) % 1000 == 0:
            x = 2
        node = frontier.pop()
        if node.state == goal_state:
            return node.pathRe()

        closed_list.add(node.state)
        # n is neighbors (children) node list
        n = expand_junction(myRoads.ROADS, node, calculateCostFunctionUcs)
        for neighbor in n:
            if neighbor.state not in closed_list and neighbor not in frontier:
                frontier.append(neighbor)
            elif neighbor in frontier and neighbor.cost < frontier[neighbor]:
                del frontier[neighbor]
                frontier.append(neighbor)

    return None
