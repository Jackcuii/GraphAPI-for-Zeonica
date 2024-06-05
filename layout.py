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
        if not self.detect_space_collsion(slab):
            self.slabs.append(slab)
            return True
        return False
    @staticmethod
    def detect_space_collsion(self, new):
        # check the new slab with all the existing slabs
        for slab in self.slabs:
            if not (slab.x + slab.width < new.x or slab.y + slab.height < new.y or slab.x > new.x + new.width or slab.y > new.y + new.height):
                return True
        if new.x + new.width > self.width or new.y + new.height > self.height:
            return True
        return False

    def draw_the_layout():
        # use matplotlib to draw the layout
        pass
