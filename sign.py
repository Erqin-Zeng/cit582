from fastecdsa.curve import secp256k1
from fastecdsa.keys import export_key, gen_keypair

from fastecdsa import curve, ecdsa, keys, point
from hashlib import sha256

def sign(m):
	#generate public key
	#Your code here
	#G = secp256k1.G
	#n = G.order()
	private_key, public_key = ecdsa.gen_keypair()


	public_key = public_key

	#generate signature
	#Your code here

	#z = sha256(m)
	r, s = ecdsa.sign(m, private_key)



	#r = pow(x1, 1, n)
	#s = 0

	assert isinstance( public_key, point.Point )
	assert isinstance( r, int )
	assert isinstance( s, int )
	return( public_key, [r,s] )