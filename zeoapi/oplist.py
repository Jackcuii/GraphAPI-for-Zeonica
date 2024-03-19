from zeoapi.ops import *
llist = {"torch.ops.aten.addmm.default": addmm.addmm,
        "torch.ops.aten.view.default": transform.transform,
        "torch.ops.aten.t.default": transpose.transpose,
        "torch.ops.aten.relu.default": relu.relu,
        "torch.ops.aten.mm.default": mm.mm,
        "torch.ops.aten.sum.dim_IntList": sum.sum,
        "torch.ops.aten.threshold_backward.default": threshold_backward.threshold_backward } 

