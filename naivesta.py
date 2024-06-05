import zeoapi.dag as dag



def make_a_layout(dag, layout):
    start = dag.find_node_without_dep()
    assert start is not None, "No node without dependencies found"
    if traversal(start, None, None, layout):
        return layout

def find_index_by_content(lst, content):
    for i in range(len(lst)):
        if lst[i] == content:
            return i
    return -1

def mirror(dir):
    switch = {"east": "west", "west": "east", "north": "south", "south": "north"}
    return switch[dir]



def traversal(pos, downstream, pipeport, layout):
    
    if pos.op == "input":
        return True
    choices = ...
    choice choice =  
    if pipeport == "east":
        pipew = downstream.map.height
    elif pipeport == "south":
        pipew = downstream.map.width

    for choice in choices:
        if choice[Odir][0] == pipeport or :
            new_slab = slab()
            h = eval(choice[height]);
            pshape = [ for parent in pos.parents]
            new_slab.height = h(pos.shape[0], ...)
            w = eval(choice[width]);
            new_slab.width = w(pos.shape[1], ...)
            if choice[Odir][0] == "east":
                new_slab.x = downstream.map.x - new_slab.width
                new_slab.y = downstream.map.y
            elif choice[Odir][0] == "south":
                new_slab.x = downstream.map.x
                new_slab.y = downstream.map.y - new_slab.height
            if layout.add_slab(new_slab):
                pos.map = new_slab
                lst = [traversal(parent, pos, mirror(choice), layout) for parent in pos.parents]
                if all(lst):
                    return True
            else:
                layout.delete_slab(new_slab)
                pos.map = None
    return False




