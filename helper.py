def make_instr_1op(name, src, srcdim):
    #assert len(src)==1, "make_instr_1op expect 1 operand."
    tmp_dict = {"instr": name, "args":[ {"symbol": src, "dim": srcdim} ] }
    return tmp_dict

def make_instr_2op(name, src, srcdim, dst, dstdim):
    tmp_dict = {"instr": name, "args":[ {"symbol": src, "dim": srcdim},  
        {"symbol": dst, "dim": dstdim} ] }
    return tmp_dict

def make_instr_3op(name, src1, sr1cdim, src2, src2dim, dst, dstdim):
    tmp_dict = {"instr": name, "args":[ {"symbol": src1, "dim": src1dim}, {"symbol": src2, "dim": src2dim}, {"symbol": dst, "dim": dstdim} ] }
    return tmp_dict
