from zeoapi.dag import *
from zeoapi.zeotensor import *
from zeoapi.layout import *
from zeoapi.zeoconf import *
from copy import deepcopy

tmp_deleted = []

def make_a_layout(dag, layout):
    preprocess_dag(dag)
    dag.print_dag()
    dag.start = dag.find_node_without_son()
    assert dag.start is not None, "No node without dependencies found"
    
    for dir in [ "SW", "SE", "NW", "NE"]:
        for i in [0,1]:
            for d in ["SOUTH","EAST"]:
                print(dag.start)
                output = ZeoTensor(dag.start.shape, (dir, i), Dimension([]), Flow(d))
                dag.start.res = output
                print("\33[32mStart from state:", output, "\33[0m")
                if traversal(dag.start, "Upstream", layout, dag, (layout.width, layout.height)):
                    print("\33[32mLayout found\33[0m")
                    dag.revert_block()
                    return True
    dag.start.res = None
    print("No layout found")
    dag.revert_block()
    return False

def preprocess_dag(dag):
    for node in list(dag.nodes.values()):
        if node.op == "input":
            if node.children[0].op == "transpose" or node.children[0].op == "transform":
                node.shape = deepcopy(node.children[0].shape)
                dag.delete_node_and_link(node.children[0])
    for node in list(dag.nodes.values()):
        if node.op == "input" and node.children[0].op == "addlmm":
            node.op = "preplaced"  # Caution: a hack, may cause bugs in complex cases
    for node in list(dag.nodes.values()):
        if node.op == "preplaced":
            dag.block_node(node)
    

def find_index_by_content(lst, content):
    for i in range(len(lst)):
        if lst[i] == content:
            return i
    return -1

def mirror(dir):
    switch = {"east": "west", "west": "east", "north": "south", "south": "north"}
    return switch[dir]


def conf_lookup(opname):
    return "OP_" + opname + "_uwp"


def traversal(pos, travDir, layout, dag, coord): 
    if pos.op == "input" or pos.op == "preplaced":
        return True
    print("\33[31mTraversing", pos.op, "\33[0m")
    kernelclass = eval(conf_lookup(pos.op))
    sargv, dargv = [], []
    if travDir is 'Upstream':
        choices =  kernelclass.aPipeG()
        sargv, dargv = [p.shape for p in pos.parents], [pos.res]
    elif travDir is 'Downstream':
        assert 0, "not implemented"
    else:
        assert 0, "Invalid traversal direction"

    ret = False
    for f in choices:
        ssargv, ddargv = f(sargv, dargv)
        print("\33[36m")
        print("ssargv:")
        for i in range(len(ssargv)):
            print(ssargv[i])
        print("ddargv:")
        for i in range(len(ddargv)):
            print(ddargv[i])
        print("\33[0m")
        x, y = coord
        w, h = kernelclass.setWH (ssargv, ddargv)
        if ssargv[0].flow == Flow("EAST"):
            x -= w
            if pos == dag.start:
                y -= h
        elif ssargv[0].flow == Flow("SOUTH"):
            y -= h
            if pos == dag.start:
                x -= w

        slab = Slab(x, y, w, h, pos.op)
        if layout.add_slab(slab):
            pos.map = slab
            assert len(ssargv) == len(pos.parents)
            for i in range(len(ssargv)):
                pos.parents[i].res = ssargv[i]
            if all([traversal(parent, travDir, layout, dag, (x, y)) for parent in pos.parents]): # TODO change the search order
                ret = True
                break
            else:
                layout.delete_slab(slab)
                pos.map = None
                continue
        else:
            continue
    return ret






