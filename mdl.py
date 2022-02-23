from math import floor


import math

def choose(n, k):
    if 0 < k <= n:
        p = 1
        for i in range(0, min(k, n-k)-1):
            p = floor((p * (n-i)) / (i+1))
        return p
    else:
        return 0

def log2(n):
    return math.log2(n)


def log2_zero(n):
    if n == 0:
        return 0
    else:
        return log2(n)

def log2_choose(n, k):
    if n == 0 or k == 0:
        return 0
    else:
        return log2_zero(choose(n, k))

def log2_star(n):
    if n <= 1:
        return 0
    else:
        return 1 + log2_star(log2(n))

def unviversal_integer(n):
    NORMALIZATION_CONSTANT = 2.865064
    if n <= 0:
        return 0
    c = log2(NORMALIZATION_CONSTANT)
    logstar_n = log2_star(n)
    return logstar_n + c


