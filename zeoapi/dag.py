class DAGnode:
    def __init__(self, name, op, shape):
        self.name = name
        self.op = op
        self.res = None
        self.shape = shape
        self.map = None
        self.start = None
        self.parents = []
        self.children = []
    def __str__(self):
        s = self.name + f"[{self.op}]" + f"({self.res})"
        s = s + ("mapped" if self.map else "unmapped")
        s += "\n"
        for parent in self.parents:
            s += "<-" + parent.name + "\n"
        for child in self.children:
            s += "->" + child.name + "\n"
        return s 

class DAG:
    def __init__(self):
        self.nodes = {}
        self.tmp_blocked_lst = []  # [(parent, child), ...]
        self.tmp_cut_lst = []
    def add_node(self, node):
        self.nodes[node.name] = node
    def delete_node(self, node):
        self.nodes.pop(node.name)
    def add_edge(self, parent, child):
        self.nodes[parent].children.append(self.nodes[child])
        self.nodes[child].parents.append(self.nodes[parent])
    def delete_node_and_link(self, node):
        # the node has a parent and a childern, linke them
        print("d&l", node)
        node.parents[0].children.remove(node)
        node.children[0].parents.remove(node)
        self.add_edge(node.parents[0].name, node.children[0].name)
        self.nodes.pop(node.name)
        del node
    def delete_edge(self, parent, child):
        self.nodes[parent].children.remove(self.nodes[child])
        self.nodes[child].parents.remove(self.nodes[parent])
    def block_node(self, node):
        self.tmp_blocked_lst.append(node)
        for child in node.children:
            self.tmp_cut_lst.append((node, child))
            self.delete_edge(node.name, child.name)
        for parent in node.parents:
            self.tmp_cut_lst.append((parent, node))
            self.delete_edge(parent.name, node.name)
        self.delete_node(node)
    def revert_block(self):
        for node in self.tmp_blocked_lst:
            self.add_node(node)
        for edge in self.tmp_cut_lst:
            self.add_edge(edge[0].name, edge[1].name)
        self.tmp_blocked_lst = []
        self.tmp_cut_lst = []
        

    def print_dag(self): # display the DAG with graphviz
        import graphviz
        dot = graphviz.Digraph()
        for node in self.nodes:
            dot.node(node, label=node+":"+self.nodes[node].op)
        for node in self.nodes:
            for child in self.nodes[node].children:
                dot.edge(node, child.name)
        dot.view()
    def find_node_without_son(self):
        for node in self.nodes:
            if self.nodes[node].children == []:
                return self.nodes[node]
        return None