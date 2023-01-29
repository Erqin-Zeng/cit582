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
    c2modp = pow(c[1], p)
    bottom_modp = pow(1/c[0], sk, p)
    m = pow(c2modp*bottom_modp, 1, p)
    return m
