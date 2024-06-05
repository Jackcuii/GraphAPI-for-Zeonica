from zeoapi.helper import *
from zeoapi.tracer import *
from zeoapi.dag import *
#import zeoapi.config

def addmm(dest, args, var_dict, graph):
    assert len(args)==3, "Interpret [addmm] fail, please check it."
    # TO-DO: support multiple width and type
    # TO-DO: enable real LOAD/STORE
    # seq+=make_instr_1op("LOAD32", "_", var_dict[args
    print("addmm", dest, args)
    if config["LME"]:
        graph.add_node(DAGnode(dest, "addlmm", Dimension(var_dict[dest][1])))
        graph.add_edge(args[0], dest)
        graph.add_edge(args[1], dest) # caution the turn!
    else:
        graph.add_node(DAGnode(dest+"_mm", "mm", Dimension(var_dict[dest][1])))
        graph.add_edge(args[0], dest+"_mm")
        graph.add_edge(args[1], dest+"_mm")
        graph.add_node(DAGnode(dest, "add", Dimension(var_dict[dest][1])))
        graph.add_edge(dest+"_mm", dest)
        graph.add_edge(args[2], dest)
    #seq += [make_instr_3op("F32MATRIX_MUL", args[1], var_dict[args[1]][1], args[2], var_dict[args[2]][1], "_", [ var_dict[args[1]][1][0], var_dict[args[2]][1][0] ])]
    #seq += [make_instr_3op("F32MATRIX_ADD", args[0], var_dict[args[0]][1], "_", [ var_dict[args[1]][1][0], var_dict[args[2]][1][0] ], dest, var_dict[dest][1] )] 



# test
#seq=[]
#dictt={ "Y": ("f32",[4,5]), "b": ("f32",[4,5]), "W": ("f32",[4,3]), "X":("f32",[3,5])}
#addmm("Y", ["b","W","X"], seq, dictt)
