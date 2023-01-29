import random

from params import p
from params import g


def keygen():
    sk = random.randint(1, p)
    pk = pow(g, sk, p)
    return pk, sk


def encrypt(pk, m):
    q = (p-1)/2
    r = random.randint(1, q)
    c1 = pow(g, r, p)
    c1_2 = pow(pk, r, p)
    c2 = pow(c1_2*m, 1, p)
    return [c1, c2]


def decrypt(sk, c):
    c1_a = pow(c[0], sk)
    c2_c1_a = c[1]/c1_a
    m = pow(c2_c1_a, 1, p)
    return m
