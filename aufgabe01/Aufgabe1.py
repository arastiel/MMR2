import time
import datetime as dt

class GraphAdjMatr:
    def __init__(self, graph_matrix, node_names):
        self.graph_matrix = graph_matrix
        self.node_names = node_names
        self.node_names_dict = {i: 1 for i in node_names}
        self.edges_dict = {i: 1 for i in self.calc_edges()}

    def num_nodes(self):
        return f'Number nodes: %s, Nodes(with value): %s' % (len(self.graph_matrix), self.node_names_dict)

    def num_edges(self):
        return f'Number of edges: %s, Edges(with value): %s' % (len(self.edges_dict), self.edges_dict)

    def from_node(self, e):
        if e in self.edges_dict:
            return e[0]
        return 0

    def to_node(self, e):
        if e in self.edges_dict:
            return e[1]
        return 0

    def out_edges(self, u):
        return f'Number of edges from %s: %s, Edges: %s' % (u, len(self.calc_from_node(u)), self.calc_from_node(u))

    def in_edges(self, u):
        return f'Number of edges to %s: %s, Edges: %s' % (u, len(self.calc_to_node(u)), self.calc_to_node(u))

    def set_node_value(self, u, value):
        if u in self.node_names_dict:
            self.node_names_dict[u] = value
            return True
        return False

    def node_value(self, u):
        if u in self.node_names_dict:
            return self.node_names_dict[u]
        return False

    def set_edge_value(self, e, value):
        if e in self.edges_dict:
            self.edges_dict[e] = value
            return True
        return False

    def edge_value(self, e):
        if e in self.edges_dict:
            return self.edges_dict[e]
        return False

    def edge_does_exist(self, u, v):
        if (u, v) in self.calc_edges():
            return True
        return False

    # Hilfsfunktionen

    def calc_to_node(self, e):
        to_node = []
        for node in range(len(self.graph_matrix)):
            if self.graph_matrix[node][self.node_names.index(e)] == 1:
                to_node.append((self.node_names[node], e))
        return to_node

    def calc_from_node(self, e):
        from_node = []
        for next_node in range(len(self.graph_matrix)):
            if self.graph_matrix[self.node_names.index(e)][next_node] == 1:
                from_node.append((e, self.node_names[next_node]))
        return from_node

    def calc_edges(self):
        edges = []
        for node in range(len(self.graph_matrix)):
            for next_node in range(len(self.graph_matrix)):
                if self.graph_matrix[node][next_node] == 1:
                    #print(self.node_names[node], self.node_names[next_node])
                    if [self.node_names[node], self.node_names[next_node]] not in edges:
                        edges.append((self.node_names[node], self.node_names[next_node]))
        return edges


class GraphAdjList:
    def __init__(self, graph_list):
        self.graph_list = graph_list
        self.node_values = {i: 1 for i in self.graph_list.keys()}
        self.edges = {i: 1 for i in self.calc_edges()}

    def num_nodes(self):
        #return f'Number nodes: %s, Nodes: %s' % (len(self.graph_matrix), self.node_names_dict)
        return f'Number nodes: %s, Nodes(with value): %s' % (len(self.graph_list), self.node_values)

    def num_edges(self):
        return f'Number of edges: %s, Edges(with value): %s' % (len(self.edges), self.edges)

    def from_node(self, e):
        if e in self.edges:
            return e[0]
        return 0

    def to_node(self, e):
        if e in self.edges:
            return e[1]
        return 0

    def out_edges(self, u):
        return f'Number of edges from %s: %s, Edges: %s' % (u, len(self.calc_from_node(u)), self.calc_from_node(u))

    def in_edges(self, u):
        return f'Number of edges to %s: %s, Edges: %s' % (u, len(self.calc_to_node(u)), self.calc_to_node(u))

    def set_node_value(self, u, value):
        if u in self.node_values:
            self.node_values[u] = value
            return True
        return False

    def node_value(self, u):
        if u in self.node_values:
            return self.node_values[u]
        return False

    def set_edge_value(self, e, value):
        if e in self.edges:
            self.edges[e] = value
            return True
        return False

    def edge_value(self, e):
        if e in self.edges:
            return self.edges[e]
        return False

    def edge_does_exist(self, u, v):
        if (u, v) in self.edges:
            return True
        return False

    # Hilfsfunktionen

    def calc_edges(self):
        # calc edges (u,v)
        edges = []
        for u in self.graph_list:
            for v in self.graph_list[u]:
                edges.append((u, v))
        return edges

    def calc_from_node(self, u):
        u_edges = [edge for edge in self.edges if edge[0] == u]
        return u_edges

    def calc_to_node(self, u):
        u_edges = [edge for edge in self.edges if edge[1] == u]
        return u_edges




if __name__ == '__main__':
    g = [[0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 1, 0, 0],
         [1, 0, 1, 0]]

    g_names = ["A", "B", "C", "D"]

    # if len(g) == len(g_names):
    #    graph = GraphAdjMatr(g, g_names)

    start1 = time.time_ns()
    s1 = dt.datetime.now()

    graph = GraphAdjMatr(g, g_names)

    print("--------------------------")
    print("\nGraph per Adjazenzmatrix\n")
    print("--------------------------")

    print(graph.num_nodes())
    print(graph.num_edges())
    print(graph.from_node(("A", "C")))
    print(graph.to_node(("C", "A")))
    print(graph.edge_does_exist("C", "A"))
    print(graph.out_edges("D"))
    print(graph.in_edges("A"))


    graph.set_node_value("D", 14)
    print(graph.node_value("D"))
    graph.set_edge_value(("A", "C"), 4)
    print(graph.edge_value(("A", "C")))

    end1 = time.time_ns()
    e1 = dt.datetime.now()

    print(f'time(with time): %s' % (end1 - start1))
    print(f'time(with datetime): %s' % ((e1-s1).microseconds))

    print("--------------------------")
    print("\nGraph per Adjazenzliste\n")
    print("--------------------------")

    g2 = {"A": ["C"],
          "B": ["C"],
          "C": ["B"],
          "D": ["A", "C"]
          }

    start2 = time.time_ns()
    s2 = dt.datetime.now()

    graph2 = GraphAdjList(g2)

    print(graph2.num_nodes())
    print(graph2.num_edges())
    print(graph2.from_node(("A", "C")))
    print(graph2.to_node(("C", "A")))
    print(graph2.edge_does_exist("C", "A"))
    print(graph2.out_edges("D"))
    print(graph2.in_edges("A"))

    graph2.set_node_value("D", 14)
    print(graph2.node_value("D"))
    graph2.set_edge_value(("A", "C"), 4)
    print(graph2.edge_value(("A", "C")))

    end2 = time.time_ns()
    e2 = dt.datetime.now()

    print(f'time(with time): %s' % (end2 - start2))
    print(f'time(with datetime): %s' % ((e2-s2).microseconds))

    '''
    Theoriefragen:
    
    Adjazenzmatrix wird bei vielen Knoten und wenig Edges mehr Speicherbedarf benötigen als eine Adjazenzliste
    Zeitbedarf ist relativ gleich?
    
    '''


