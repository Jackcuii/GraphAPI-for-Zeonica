class DAGnode:
    def __init__(self, name, op, shape):
        self.name = name
        self.op = op
        self.res = shape
        self.map = None
        self.parents = []
        self.children = []

class DAG:
    def __init__(self):
        self.nodes = {}
    def add_node(self, node):
        self.nodes[node.name] = node
    def add_edge(self, parent, child):
        self.nodes[parent].children.append(child)
        self.nodes[child].parents.append(parent)
    def remove_edge(self, parent, child):
        self.nodes[parent].children.remove(child)
        self.nodes[child].parents.remove(parent)
    def remove_node(self, node):
        for parent in self.nodes[node].parents:
            self.nodes[parent].children.remove(node)
        for child in self.nodes[node].children:
            self.nodes[child].parents.remove(node)
        del self.nodes[node]
    def get_roots(self):
        roots = []
        for node in self.nodes:
            if self.nodes[node].parents == []:
                roots.append(node)
        return roots
    def get_leaves(self):
        leaves = []
        for node in self.nodes:
            if self.nodes[node].children == []:
                leaves.append(node)
        return leaves
    def get_node(self, name):
        return self.nodes[name]
    def get_children(self, name):
        return self.nodes[name].children
    def get_parents(self, name):
        return self.nodes[name].parents
    def get_shape(self, name):
        return self.nodes[name].shape
    def get_op(self, name):
        return self.nodes[name].op
    def get_all_nodes(self):
        return self.nodes
    def get_all_edges(self):
        edges = []
        for node in self.nodes:
            for child in self.nodes[node].children:
                edges.append((node, child))
        return edges
    def get_all_edges_with_op(self):
        edges = []
        for node in self.nodes:
            for child in self.nodes[node].children:
                edges.append((node, child, self.nodes[node].op))
        return edges
    def get_all_edges_with_shape(self):
        edges = []
        for node in self.nodes:
            for child in self.nodes[node].children:
                edges.append((node, child, self.nodes[node].shape))
        return edges
    def get_all_edges_with_op_shape(self):
        edges = []
        for node in self.nodes:
            for child in self.nodes[node].children:
                edges.append((node, child, self.nodes[node].op, self.nodes[node].shape))
        return edges
    def print_dag(self): # display the DAG with graphviz
        import graphviz
        dot = graphviz.Digraph()
        for node in self.nodes:
            dot.node(node, label=node+":"+self.nodes[node].op)
        for node in self.nodes:
            for child in self.nodes[node].children:
                dot.edge(node, child)
        dot.view()
