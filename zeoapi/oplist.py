from zeoapi.ops import *
llist = {"torch.ops.aten.addmm.default": addmm.addmm,
        "torch.ops.aten.view.default": transform.transform,
        "torch.ops.aten.t.default": transpose.transpose,
        "torch.ops.aten.relu.default": relu.relu } 

