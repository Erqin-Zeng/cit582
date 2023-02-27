import math

def num_BTC(b):
    n=int(b/210000) 
    m=pow(b,1,210000)
    c = float(50*210000*(2-pow(0.5,n-1))+ 50*pow(0.5,n)*m) 
    return c
