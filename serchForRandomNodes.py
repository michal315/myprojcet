# Python3 program to print DFS traversal
# from a given given graph
import csv
from collections import defaultdict
import collections
from collections import namedtuple
from ways import load_map_from_csv
from statistics import mean
from Ucs import  ucs_rout
import datetime
from main import find_idastar_route
import myRoads
import astar
import idastar
from Ucs import calculateCostFunctionUcs
import random

# This class represents a directed graph using
# adjacency list representation
class Graph:

	# Constructor
    def __init__(self):
        self.graph = defaultdict(list)

# function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

# A function used by DFS
    def DFSUtil(self, v, visited,possibleTargetsNodes,depth,maxRandomDepth):
# Mark the current node as visited# and print it4\
        if depth>=maxRandomDepth:
            return

        visited[v] = True
        possibleTargetsNodes.append(v)


        # Recur for all the vertices
        # adjacent to this vertex
        for i in self.graph[v]:
            if visited[i] == False:
                self.DFSUtil(i, visited,possibleTargetsNodes,depth+1,maxRandomDepth)




# The function to do DFS traversal. It uses
# recursive DFSUtil()
    def DFS(self, v):
        visited = [False] * (len(self.graph))
        possibleTargetsNodes=list()
        maxRandomDepth=random.randint(2, 8)
        self.DFSUtil(v, visited,possibleTargetsNodes,0,maxRandomDepth)

        if (len(possibleTargetsNodes)) - 1 > 1:
            randomTargetIndex = random.randint(1, (len(possibleTargetsNodes)) - 1)
        else:
            randomTargetIndex = 1
        row = (v, possibleTargetsNodes[randomTargetIndex])
        #print('row:', row)
        with open('problems.csv', mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(row)


        possibleTargetsNodes.clear()
        return row


def find_astar_route(source, target):

    total_path=astar.find_route(source, target)
  #  print("total _ path :",total_path)
    myRoads.plotPath(total_path)# Driver code


g = Graph()
def CreateGraph(roads):
    for source_links in roads.junctions():
        for target_links in  source_links[3]:   #source_links[3] is tuple
            sourceNode=source_links[0]
            targetNode=target_links[1]

            g.addEdge(sourceNode, targetNode)

    TOTALUCSTIME=0
    for i in range (100): #100
        randomSourceNode=random.randint(0, len(roads))
        row=g.DFS(randomSourceNode)
        source=row[0]
        dest=row[1]
        astar.find_route(source,dest)
        idastar.find_route(source,dest)
        ucs_rout(source,dest)
#        datetime_object_start = datetime.datetime.now()
      #  print("start time:",datetime_object_start)
        #find_idastar_route(source, dest)
      #  date_time_object_finish=datetime.datetime.now()
       # print("end time:", date_time_object_finish)
#        TOTALUCSTIME=TOTALUCSTIME+datetime_object_start.second()-date_time_object_finish.second()
    #    print("total time:",datetime_object_start.second()-date_time_object_finish.second())
       # find_astar_route(source, dest)
       # resultedPath=ucs_rout(source, dest)
       # myRoads.plotPath(resultedPath)

 #   print("AVG TIME: ",TOTALUCSTIME/100)

   # for item in resultedPath:
      #  print(item.state) #printing the node in the pathfrom the start to the target





#print("Following is DFS from (starting from vertex 2)")


