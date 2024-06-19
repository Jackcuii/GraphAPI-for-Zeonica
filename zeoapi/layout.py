import matplotlib.pyplot as plt

class Slab():
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
    def detect_space_collsion(self, new):
        # check the new slab with all the existing slabs
        print("detecting space collision", f"(x:{new.x}, y:{new.y}, w:{new.width}, h:{new.height})")
        for slab in self.slabs:
            if not (slab.x + slab.width <= new.x or slab.y + slab.height <= new.y or slab.x >= new.x + new.width or slab.y >= new.y + new.height):
                print("\33[35mIntersect")
                self.print_all_slabs()
                print("\33[0m")
                return True
        if (new.x + new.width > self.width) or (new.y + new.height > self.height or new.x < 0 or new.y < 0):
            print("\33[35mOut of bound\33[0m")
            return True
        return False
    def delete_slab(self, slab):
        self.slabs.remove(slab)
    def draw_the_layout(self):
        # use matplotlib to draw the layout
        # (0,0) at left top , and x increase to right, y increase to down
        self.print_all_slabs()
        fig, ax = plt.subplots()
        for slab in self.slabs:
            #write op in middle of the rect
            rect = plt.Rectangle((slab.x, slab.y), slab.width, slab.height, fill=True, edgecolor='r', facecolor='none')
            ax.text(slab.x + slab.width/2, slab.y + slab.height/2, slab.op, fontsize=12, ha='center', va='center')
            ax.add_patch(rect)
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.invert_yaxis()
        plt.show()
    def print_all_slabs(self):
        for slab in self.slabs:
            print(f"{slab.op}(x:{slab.x}, y:{slab.y}, w:{slab.width}, h:{slab.height})")

