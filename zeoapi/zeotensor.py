
dircs = ["SW", "SE", "NW", "NE"]

class ZeoTensor: # TODO: Auto process wrap in constructor
    def __init__(self, dim, dirc, wrap, flow):
        assert type(dim) == Dimension
        self.dim = dim
        assert dirc[0] in dircs
        self.dirc = dirc
        assert type(wrap) == Dimension
        self.wrap = wrap
        self.flow = flow
    def __str__(self):
        return f"Tensor({self.dim.shape}, {self.dirc[0]}{self.dirc[1]}, {self.wrap.shape}, {self.flow})"
    def get_vertical_size(self):
        if self.flow == Flow("SOUTH"):
            if self.dirc[1] == 1:
                return self.dim[0]
            else:
                return self.dim[1]
        elif self.flow == Flow("EAST"):
            if self.dirc[1] == 1:
                return self.dim[1]
            else:
                return self.dim[0]
    def get_horizontal_size(self):
        if self.flow == Flow("SOUTH"):
            if self.dirc[1] == 1:
                return self.dim[1]
            else:
                return self.dim[0]
        elif self.flow == Flow("EAST"):
            if self.dirc[1] == 1:
                return self.dim[0]
            else:
                return self.dim[1]

class Dimension:
    def __init__(self, shape=[]):
        self.shape = shape
    def __item__(self, index):
        if index >= len(self.shape):
            return 1
        return self.shape[index]
    def __getitem__(self, index):
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
    def __str__(self):
        return self.dir
    def __eq__(self, other):
        return self.dir == other.dir

'''
a = ZeoTensor([2, 3], ("SW", 1), [1, 4])
print(a)
'''
