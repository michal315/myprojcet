from ways import load_map_from_csv



class Node:
    #state : the node name
    #path_cost = cost

    def __init__(self, state, parent=None, cost=0,lat=0,lon=0):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.lat=lat
        self.lon=lon

        #self.depth = 0
        #if parent:
          #  self.depth = parent.depth + 1

    # dict on python 3.7+ preserves insertion order.
    # This is #a quick way to create a set which preserves it as well.
    # required for presentation purposes only.
    def ordered_set(coll):
        return dict.fromkeys(coll).keys()

    def expand(self, problem):
        return self.ordered_set([self.cost])


    def costT(self):
        countcost=0
        path_back = []
        node=self
        while node:
            path_back.append(node)
            node = node.parent
            countcost=countcost+node.cost
        return countcost






    def pathRe(self):
        path_back = []
        node=self
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __repr__(self):
        return f"<{self.state}>"

    def __lt__(self, node):
        return self.state < node.state

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.state)