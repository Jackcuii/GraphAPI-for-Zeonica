def g():
    def f(x):
        if a == 1:
            return x + 1
        elif a == 2:
            return x + 2
        elif a == 3:
            return x + 3
        else:
            raise ValueError("Invalid value for a, must be 1, 2, or 3")
    for a in [1,2,3]:	
        yield f	

# 示例如何使用
gr = g()
print(next(gr)(1))
print(next(gr)(1))
print(next(gr)(1))

def k(x):
    return 1, (("south" if x == 1 else "north"))

print(k(1))
print(k(2))

