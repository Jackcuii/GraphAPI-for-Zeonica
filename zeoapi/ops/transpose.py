import zeoapi.helper

def transpose(dest, args, seq, var_dict):
    assert len(args)==1, "Interpret [addmm] fail, please check it."
    # TO-DO: support multiple width and type
    # TO-DO: enable real LOAD/STORE
    # seq+=make_instr_1op("LOAD32", "_", var_dict[args
    seq += make_instr_2op("32TRANSPOSE", args[0], var_dict[args[0]][1], dest, var_dict[dest][1] ) 



# test
#seq=[]
#dictt={ "Y": ("f32",[4,5]), "b": ("f32",[4,5]), "W": ("f32",[4,3]), "X":("f32",[3,5])}
#addmm("Y", ["b","W","X"], seq, dictt)
