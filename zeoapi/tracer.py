import re
import json
var_dict={}

instr_seq = [];

'''
formal_type_parser(item: string) -> string

parse a "xxxx: f32[...]" format string to its semanteme.
and register it to the var_dict
then return the var name
'''

def formal_type_parser(item):
  #print("formal type:", item)
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
  zeoapi.oplist.llist[name](dest, args, instr_seq, var_dict)
  #print("SEQ: ", instr_seq)


anons = 0
def find_anon(args):
  #print("pre-anon:", args)
  args = re.findall("\(.+\)",args)[0][1:-1]
  while True:
    global anons
    found = re.search("\[.+\]",args)
    if not found:
      break
    #print(found.group())
    formal_type_parser("anon"+str(anons)+": f32"+found.group())  # need adapt when extend types
    args = re.sub("\[.+\]", "anon"+str(anons), args)
    #print("now args",args)
    anons+=1
  #print("anoned: ", args)
  return args

def literal(line):
  line = line.split(" = ")
  #print(line)
  dest = formal_type_parser(line[0][4:])
  func_call = re.findall(".+;",line[1])
  if not func_call==[]:
    func_call = func_call[0][:-1]
  else:
    func_call = line[1]
  
  #print(func_call)
  func_name = re.findall(".+\(", func_call)[0][:-1]
  func_args = find_anon(func_call).split(", ")
  semantic(dest, func_name, func_args)

def code_process(code):
  code = code.split("\n")
  para_line = code[3]
  #print("paraline is ",para_line)
  para_line = re.findall("\(.+\):", para_line)[0][1:-2]
  para_line = para_line.split("], ")
  #print(para_line)
  para_line = [ item+"]" for item in para_line ]
  para_line[len(para_line)-1]=para_line[len(para_line)-1][:-1]
  para_line[0] = para_line[0][6:] # omit self
  # para_line = [for item in re.findall(".+, ", para_line) if item.count(": ")]para_line.split(", ")
  # para_line = para_line[1:] # omit self
  para_line = [ formal_type_parser(item) for item in para_line ]

    # process the operators part.
  code = code[5:-2]
  #print("code is",code,"jaahhahie")
  for line in code:
    literal(line)

def jsonize():
  file = open("./instr-sequence.json","w")
  jsonized = json.dumps({"version": "0.1" , "mode": "test", "instrs": instr_seq}, indent=4)
  #print(jsonized)
  file.write(jsonized)

forward_code=""
backward_code=""

def trace_a_module(model, backward=True):
  print("Now you are in a test mode. All the opreators are interpreted into pseudo instrs.")
  print("LOAD/STORE are not arranged.")
  import torch
  from functorch.compile import aot_module, \
          make_boxed_func, ts_compile
  def run_func(func, *inputs):
    res = func(*inputs)
    loss = res.sum()
    loss.backward()
  def f_compiler(fx_module: torch.fx.GraphModule, _):
    print("compiler called")
    global forward_code
    forward_code += str(fx_module._graph.python_code(root_module="self", verbose=True).src)
    #print(forward_code)
    return make_boxed_func(fx_module.forward)
  def b_compiler(fx_module: torch.fx.GraphModule, _):
    print("compiler called")
    global backward_code
    backward_code += str(fx_module._graph.python_code(root_module="self", verbose=True).src)
    return make_boxed_func(fx_module.forward)
  from torch._subclasses import FakeTensorMode
  with FakeTensorMode(allow_non_fake_inputs=True):
    a=torch.randn(1,28,28, requires_grad=True,device="cpu") 
    aot_print_fn = aot_module(model, fw_compiler=f_compiler,bw_compiler=b_compiler)
    run_func(aot_print_fn, a)
  #print("hahah:",forward_code)
  #print("hahah")
  code_process(forward_code)
  if(backward):
    code_process(backward_code)
  jsonize() 



