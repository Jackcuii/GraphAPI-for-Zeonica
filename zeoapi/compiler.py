from zeoapi.dag import *
from zeoapi.zeotensor import *
from zeoapi.layout import *
from zeoapi.zeoconf import *


DATA_WIDTH = 4 # 4 Bytes, for FP32

# A cell is an infrastructure for compilation of a single CGRA FU
class Mesh:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[cell() for i in range(w)] for j in range(h)]
    def cell_query(self, x, y):
        return self.cells[x][y]



class cell:
    def __init__(self, op = None, addrhead = 0x0, text = "", preset = []):
        self.op = op
        self.addrhead = addrhead
        self.text = text
        self.preset = preset
        self.addrhead += len(preset) * DATA_WIDTH

    # make a loop running given constant $count times
    def make_count_loop(self, loopbody, count, name, iter_val_reg, cmp_reg):
        self.text += f"MOV, {iter_val_reg}, {count}\n"
        self.text += f"{name}_LOOP:\n"
        self.text += loopbody
        self.text += f"SUB, {iter_val_reg}, {iter_val_reg}, 0x1\n"
        self.text += f"I32_CMP_GT, {iter_val_reg}, 0, {cmp_reg}\n"
        self.text += f"JEQ, {name}_LOOP, {cmp_reg}, 1\n"
        

    def output(self, x, y):
        if self.text == "": 
            return
        asm = open(f"./asms/{x}_{y}.cgraasm", "w")
        #ps = open(f"{x}_{y}.prst", "w")
        asm.write(self.text)
        #for i in self.preset:
            #ps.write(i)
        asm.close()
        #ps.close()


def compile(graph, layout, mesh):
    print(graph.nodes.values())
    for node in graph.nodes.values():
        print(node.name, node.map, node.res)
    for node in graph.nodes.values():
        slab = node.map
        if slab is None:
            print(f"Node {node.name} is not mapped")
            continue
        else:
            print(f"Node {node.name} is mapped to {slab}")
        if slab.op == "addlmm_schdlr":
            addlmm_schdlr_compile(mesh, slab, node)
        elif slab.op == "relu":
            relu_compile_inf(mesh, slab, node)
        elif slab.op == "addlmm":
            for nd in graph.nodes.values():
                if node in nd.children:
                    info = nd.res
                    if info is None:
                        continue
                    if info.flow == Flow("SOUTH"):
                        rounds = info.get_vertical_size()
                    elif info.flow == Flow("EAST"):
                        rounds = info.get_horizontal_size()
            addlmm_compile(mesh, slab, node, rounds)

    for i in range(layout.width):
        for j in range(layout.height):
            cell = mesh.cell_query(i, j)
            print(f"Outputting {i}_{j}.cgraasm")
            #print(cell.text)
            cell.output(i, j)
            

mirror = {"NORTH":"SOUTH", "SOUTH":"NORTH", "EAST":"WEST", "WEST":"EAST"}

def addlmm_schdlr_compile(mesh, slab, node):
    slabinfo = node.res
    flow = slabinfo.flow 
    if flow == Flow("SOUTH"):
        y = slab.y
        assert(type(slabinfo) == ZeoTensor)
        rounds = slabinfo.get_vertical_size()
        for i in range(slab.x, slab.x + slab.width):
            cell = mesh.cell_query(i, y)
            cell.op = "addlmm_schdlr"
            lb1 = "SEND, 0, NET_SEND_SOUTH\n"
            cell.make_count_loop(lb1, i - slab.x, "SENDZERO", "$0", "$1")
            lb2 = "WAIT, $0, NET_RECV_NORTH\nSEND ,$0, NET_SEND_SOUTH\n"
            cell.make_count_loop(lb2, rounds, "SENDDATA", "$1", "$2")
            cell.make_count_loop(lb1, slab.width - i + slab.x - 1, "SENDZEROAFTER", "$0", "$1")
    elif flow == Flow("EAST"):
        x = slab.x
        assert(type(slabinfo) == ZeoTensor)
        rounds = slabinfo.get_horizontal_size()
        for j in range(slab.y, slab.y + slab.height):
            cell = mesh.cell_query(x, j)
            cell.op = "addlmm_schdlr"
            lb1 = "SEND, 0, NET_SEND_EAST\n"
            cell.make_count_loop(lb1, j - slab.y, "SENDZERO", "$0", "$1")
            lb2 = "WAIT, $0, NET_RECV_WEST\nSEND ,$0, NET_SEND_EAST\n"
            cell.make_count_loop(lb2, rounds, "SENDDATA", "$1", "$2")
            cell.make_count_loop(lb1, slab.height - j + slab.y - 1, "SENDZEROAFTER", "$0", "$1")
    return

def relu_compile_inf(mesh, slab, node):
    slabinfo = node.res
    flow = slabinfo.flow
    for i in range(slab.x, slab.x + slab.width):
        for j in range(slab.y, slab.y + slab.height):
            cell = mesh.cell_query(i, j)
            cell.op = "relu"
            cell.text += "RELU_INF_LOOP:\n"
            cell.text += f"WAIT, $0, NET_RECV_{-flow}\n"
            cell.text += "F32_CMP_GT, $1, $0, 0\n"
            cell.text += "JNE, ELSE, $1, 1\n"
            cell.text += "IF:\n"
            cell.text += f"SEND, $0, NET_SEND_{flow}\n"
            cell.text += "JMP, END\n"
            cell.text += "ELSE:\n"
            cell.text += f"SEND, 0, NET_SEND_{flow}\n"
            cell.text += "END:\n"
            cell.text += "JMP, RELU_INF_LOOP\n"

def addlmm_compile(mesh, slab, node, rounds):
    slabinfo = node.res
    flow = slabinfo.flow
    for i in range(slab.x, slab.x + slab.width):
        for j in range(slab.y, slab.y + slab.height):
            cell = mesh.cell_query(i, j)
            cell.op = "addlmm"
            cell.text += "MOV, $0, 0\n"
            lb = "WAIT, $1, NET_RECV_WEST\n"
            lb += "WAIT, $2, NET_RECV_NORTH\n"
            lb += "MAC, $0, $1, $2\n"
            lb += "SEND, $1, NET_SEND_EAST\n"
            lb += "SEND, $2, NET_SEND_SOUTH\n"
            cell.make_count_loop(lb, rounds, "MAC", "$4", "$3")
            # here may need color mechanism
            #send out the result
            if(flow == Flow("EAST")):
                cell.text += "SEND, $0, NET_SEND_EAST\n"
                lb1 = "WAIT, $0, NET_RECV_WEST\n"
                lb1 += "SEND, $0, NET_SEND_EAST\n"
                cell.make_count_loop(lb1, i - slab.x, "SENDRES", "$0", "$1")
            elif(flow == Flow("SOUTH")):
                cell.text += "SEND, $0, NET_SEND_SOUTH\n"
                lb1 = "WAIT, $0, NET_RECV_NORTH\n"
                lb1 += "SEND, $0, NET_SEND_SOUTH\n"
                cell.make_count_loop(lb1, j - slab.y, "SENDRES", "$0", "$1")









