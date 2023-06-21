import csv
import numpy as np
from pqueue import PQueue

#################################################################################
#                                                                               #
#  Nodes haben die Form: [(Knotennummer, (Längengrad, Breitengrad)), ...]       #
#  Edges haben die Form: [[(Knotennummer1, Knotennummer2), distance], ...]      #
#                                                                               #
#################################################################################


class Graph:
    def __init__(self, _edges, _nodes):
        self.nodes = self.init_nodes(_nodes)
        self.edges = self.init_edges(_edges)
        self.map_index = [i for i in range(len(self.nodes))]
        self.node_index = [node[0] for node in self.nodes]
        self.data = dict(zip(self.node_index, self.map_index))

        self.calc_distance()    # calculate distance of edges

    @staticmethod
    def init_edges(_edges):
        with open(_edges, 'r') as edgedata:
            reader = csv.reader(edgedata)
            edges = []
            for row in reader:
                edges.append([(int(row[0]), int(row[1])), 0])
            edges.sort(key=lambda x: x[0])
            return edges

    @staticmethod
    def init_nodes(_nodes):
        with open(_nodes, 'r') as nodedata:
            reader = csv.reader(nodedata)
            nodes = []
            for (index, lg, bg) in reader:
                nodes.append((int(index), (float(lg), float(bg))))
            nodes.sort(key=lambda x: x[0])
            return nodes

    def num_nodes(self):
        return len(self.nodes)

    def num_edges(self):
        return len(self.edges)

    def from_node(self, e):
        return e[0]

    def to_node(self, e):
        return e[1]

    def out_edges(self, u):
        #alle ausgehende Kanten von u
        return [edge for edge in self.edges if edge[0][0] == u]

    def in_edges(self, u):
        #alle eingehende Kanten zu u
        return [edge for edge in self.edges if edge[0][1] == u]

    def is_edge(self, u, v):
        return any([edge for edge in self.edges if edge[0] == (u, v)])

    def set_node_value(self, u, value):
        pass

    def node_value(self, u):
        return self.nodes[self.data[u]][1]

    def set_edge_value(self, e, value):
        e[1] = value

    def edge_value(self, e):
        return next(edge[1] for edge in self.edges if edge[0] == e)

    def calc_distance(self):
        for edge in self.edges:
            b = 111.3 * np.cos((float(self.nodes[self.data[edge[0][0]]][1][1])+float(self.nodes[self.data[edge[0][1]]][1][0]))/2)

            dist = np.sqrt((b*(float(self.nodes[self.data[edge[0][0]]][1][0]) - float(self.nodes[self.data[edge[0][1]]][1][0])))**2 \
                            + (111.3*(float(self.nodes[self.data[edge[0][0]]][1][1]) - float(self.nodes[self.data[edge[0][1]]][1][1])))**2)

            self.set_edge_value(edge, dist)

    def get_min_lg(self):
        return min(self.nodes, key=lambda x: x[1][0])[1][0]


    def get_max_lg(self):
        return max(self.nodes, key=lambda x: x[1][0])[1][0]


    def get_min_bg(self):
        return min(self.nodes, key=lambda x: x[1][1])[1][1]


    def get_max_bg(self):
        return max(self.nodes, key=lambda x: x[1][1])[1][1]

    def get_node_from_name(self, u):
        return [node for node in self.nodes if node[0] == u]


    def edge_value(self, e):
        return next(edge[1] for edge in self.edges if edge[0] == e)

    def djikstra(self, s, t):
        grey_nodes = {}
        black_nodes = {}

        prev_node = {}
        dist_node = {node[0]: np.inf for node in self.nodes}
        grey_nodes[s] = 1
        dist_node[s] = 0

        pqueue = PQueue()
        pqueue.push(s, dist_node[s])

        while len(grey_nodes) > 0:
            u = pqueue.pop_min()
            grey_nodes.pop(u)
            black_nodes[u] = 1

            if u == t:
                break

            edges_to_check = [edge for edge in self.out_edges(u) if edge[0][1] not in black_nodes]

            for edge in edges_to_check:
                v = edge[0][1]
                if v not in grey_nodes:
                    grey_nodes[v] = 1
                    dist_node[v] = dist_node[u] + edge[1]
                    pqueue.push(v, dist_node[u] + edge[1])
                    prev_node[v] = edge

                else:
                    if dist_node[u] + edge[1] < dist_node[v]:
                        dist_node[v] = dist_node[u] + edge[1]
                        pqueue.decrease_key(v, dist_node[u] + edge[1])
                        prev_node[v] = edge

        if dist_node[t] == np.inf:
            print("no route found")
            return "Kein Weg gefunden"

        P = []
        u = t
        while u != s:
            P.append(prev_node[u])
            u = prev_node[u][0][0]

        return P
