class slab():
    def __init__(self, x, y, width, height, op):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.op = op

class Layout():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.slabs = []
    def add_slab(self, slab):
        pass
    @staticmethod
    def detect_space_collsion(self, new):
        # check the new slab with all the existing slabs
        for slab in self.slabs:
            if slab.x < new.x + new.width and new.x < slab.x + slab.width and slab.y < new.y + new.height and new.y < slab.y + slab.height:
                return True
        if new.x + new.width > self.width or new.y + new.height > self.height:
            return True
        return False
    