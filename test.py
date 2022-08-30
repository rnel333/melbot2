a, b, c = 1, 2, 3

def f(x):
    rtn = a * x + b
    return rtn


result = f(f(f(c)))
print(result)