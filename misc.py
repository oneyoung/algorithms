rem = lambda a, b: a % b


def gcd(a, b):
    m, n = (a, b) if a > b else (b, a)
    if n:
        return gcd(rem(m, n), n)
    else:
        return m
