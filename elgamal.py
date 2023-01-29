import random

from params import p
from params import g

def keygen():
    sk = random.randint(1, p)
    pk = pow(g, sk, p)
    return pk, sk

def encrypt(pk,m):
    r = random.randint(1,(p-1)/2)
    c1 = pow(g, r, p)
    c2 = pow(pow(pk, r)*m, 1, p)
    return [c1, c2]

def decrypt(sk,c):
    m = pow(c[1]/(pow(c[0],sk)),1,p)
    return m

