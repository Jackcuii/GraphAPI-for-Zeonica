class Node:
    def __init__(self, no, op):
        self.no = no
        self.op = op


class DAG:
    def __init__(self):
        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)
        self.out_degree = defaultdict(int)
        self.vertices = set()

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.in_degree[v] += 1
        self.out_degree[u] += 1
        self.vertices.add(u)
        self.vertices.add(v)

    def get_in_degree(self):
        return self.in_degree

    def get_out_degree(self):
        return self.out_degree

    def get_graph(self):
        return self.graph

    def get_vertices(self):
        return self.vertices

    def get_edges(self):
        edges = []
        for u in self.graph:
            for v in self.graph[u]:
                edges.append((u, v))
        return edges

    def __str__(self):
        return str(self.graph)
    
    def find_node_without_dep(self):
        for node in self.vertices:
            if self.in_degree[node] == 0:
                return node
        return None