from zeoapi.ops import *
list = {"torch.ops.aten.addmm.default": addmm,
        "torch.ops.aten.view.default": transform,
        "torch.ops.aten.t.default": transpose,
        "torch.ops.aten.relu.default": relu } 

