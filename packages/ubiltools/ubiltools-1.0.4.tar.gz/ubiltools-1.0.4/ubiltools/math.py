def gcd(x, y):
    x = abs(x)
    y = abs(y)
    while x:
        x, y = y % x, x
    return y
