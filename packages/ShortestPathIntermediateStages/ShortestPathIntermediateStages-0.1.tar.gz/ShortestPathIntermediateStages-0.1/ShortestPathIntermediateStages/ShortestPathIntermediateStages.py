import networkx as nx

class ShortestPathIntermediateStages:

    def __init__(self, graph=nx.DiGraph()):
        """Generic shortest path class with respective attributes.

        Args:
            graph - directed networkx graph

        Attributes:
            path (list) - representing the path by its corresponding nodes
            source - source node
            sink - sink node
            intermediate (list) - ordered list of nodes
        """
        self.graph = graph
        self.path = []
        self.source = None
        self.sink = None
        self.intermediate = []


    def calc_SPIS(self, source, sink, intermediate, weight=None):
        """Function to calculate the shortest path distance from source to sink
            such that all intermediate nodes are visited

        Args:
            G - representing a directed networkx graph
            weight - representing the weight function defined over the set of arcs of G

        Returns:
            PathObject (dict) - representing the shortest path along with its features
        """
        # update source, sink, intermediate attributes
        self.source = source
        self.sink = sink
        self.intermediate = intermediate

        # ordered list of nodes to be visited
        nodelist = [self.source] + [node for node in self.intermediate] + [self.sink]

        # shortest path from source to sink via intermediate nodes
        shortestpath = [nx.dijkstra_path(self.graph, nodelist[i], nodelist[i+1], weight=weight)[:-1] for i in
                        range(len(nodelist) - 1)]
        shortestpath_new = [item for sublist in shortestpath for item in sublist] + [nodelist[-1]]

        # update path attribute
        self.path = shortestpath_new

        # create pathObject
        pathObject = {
            'source node': self.source,
            'sink node': self.sink,
            'intermediate nodes': self.intermediate,
            'path': self.path
        }

        return pathObject