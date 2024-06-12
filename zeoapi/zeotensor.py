
dircs = ["SW", "SE", "NW", "NE"]

class ZeoTensor: # TODO: Auto process wrap in constructor
    def __init__(self, dim, dirc, wrap):
        assert type(dim) == list
        self.dim = Dimension(dim)
        assert dirc[0] in dircs
        self.dirc = dirc
        self.wrap = Dimension(wrap)
    def __str__(self):
        return f"Tensor({self.dim.shape}, {self.dirc[0]}{self.dirc[1]}, {self.wrap.shape})"
class Dimension:
    def __init__(self, shape=[]):
        self.shape = shape
    def __item__(self, index):
        if index >= len(self.shape):
            return 1
        return self.shape[index]

mir = {"NORTH": "SOUTH", "SOUTH": "NORTH", "EAST": "WEST", "WEST": "EAST"}


class Flow:
    def __init__(self, s):
        assert s in mir.keys(), "Invalid flow direction"
        self.dir = s
    def __neg__(self):
        return Flow(mir[self.dir])

'''
a = ZeoTensor([2, 3], ("SW", 1), [1, 4])
print(a)
'''
