import re

var_dict={}

operation_sequence = "";
wrapped=[operation_sequence]
'''
formal_type_parser(item: string) -> string

parse a "xxxx: f32[...]" format string to its semanteme.
and register it to the var_dict
then return the var name
'''
import zeoapi.ops
import importlib

def formal_type_parser(item):
    item = item.split(": ")
    name = item[0]
    assert item[1][3]=='[', "FATAL: Sorry, we only support i16, i32, i64, f16, f32, f64 now."
    type = item[1][:2]
    item[1] = item[1][3:]
    dimension = eval(item[1])
    var_dict[name] = (type, dimension)
    return name

def semantic(dest, name, args):
    import zeoapi.oplist
    zeoapi.oplist.list[name](dest, args)


def literal(line):
    line = line.split(" = ")
    dest = formal_type_parser(line[0])
    func_call = re.findall(".+;",line)[0][:-1]
    func_name = re.findall(".+(", func_call)[0][:-1]
    func_args = re.findall("(.+)",func_name)[0][1:-1].split(", ")
    semantic()


    

def code_process(code):
    code = code.split("\n")
    para_line = code[0]
    para_line = re.findall("\(.+\):", para_line)[0][1:-2]
    para_line = para_line.split(", ")
    para_line = [ helper(item) for item in para_line ]

    # process the operators part.
    code = code[1:]
    for line in code:
        literal(line)

def jsonize():
def trace_a_module(model):
    print("Now you are in a test mode. All the opreators are interpreted into pseudo instrs.")
    print("LOAD/STORE are not arranged.")



code="aefueafi frhihirgte(frwf, gwrhgur, hg,    iwrg):\nfwjruhuwrhufwhoghworighowhgohworhg\nwhguhu"

code_process(code)

