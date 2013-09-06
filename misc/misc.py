rem = lambda a, b: a % b


def gcd(a, b):
    ''' get gcd of a and b '''
    m, n = (a, b) if a > b else (b, a)
    if n:
        return gcd(rem(m, n), n)
    else:
        return m


def mod(n, p, m):
    ''' (n**p)%m '''
    # let p = a(i)*2^i + a(i-1)*2^(i-1) + ... + a(1)*2^1 + a(0)  // a(i) = 0|1
    # so n^p = A(i)*A(i-1)*...*A(1)*A(0)   // let A(j) = n^(a(j)*2^j)
    # and we have a*b mod m = ((a mod m)*(b mod m)) mod m
    # n^p mod m = (A(i)*A(i-1)*...*A(1)*A(0)) mod m
    # = (((A(i)*...A(1)) mod m) * (A(0) mod m)) mod m
    # = (m(i)*m(i-1)*...*m(0)) mod m  // m(i) = A(i) mod m
    # ** further m(i) = A(i) mod m = n^(a(j)*2^j) mod m
    # = n^(a(j)*(2^(j-1) + 2^(j-1))) mod m
    # if a(j) == 0, m(j) = 1 mod m = 1
    # if a(j) == 1, m(j) = B(j - 1)^2 mod m  // B(j) = n^(2^j) mod m
    # ** B(0) = n mod m
    #  B(j) = B(j - 1)^2 mod m
    x = 1
    b = n % m
    for a in bin(p)[2:][::-1]:
        if int(a):
            x = (x * b) % m
        b = (b * b) % m
    return x
