from zeoapi.helper import *
from zeoapi.dag import *
from zeoapi.zeotensor import *

def relu(dest, args, var_dict, graph):
    assert len(args)==1, "Interpret [relu] fail, please check it."
    # TO-DO: support multiple width and type
    # TO-DO: enable real LOAD/STORE
    # seq+=make_instr_1op("LOAD32", "_", var_dict[args
    print("relu", dest, args)
    graph.add_node(DAGnode(dest, "relu", Dimension(var_dict[dest][1])))
    graph.add_edge(args[0], dest)
    #seq += [make_instr_2op("F32RELU", args[0], var_dict[args[0]][1], dest, var_dict[dest][1] )] 



# test
#seq=[]
#dictt={ "Y": ("f32",[4,5]), "b": ("f32",[4,5]), "W": ("f32",[4,3]), "X":("f32",[3,5])}
#addmm("Y", ["b","W","X"], seq, dictt)
