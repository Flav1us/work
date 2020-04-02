def a(arg1, arg2):
    return arg1*arg2

def x(a, b):
    for c in b:
        yield a(*c)

b = [(1, 2), (3, 4)]

for i in x(a, b):
    print(i)