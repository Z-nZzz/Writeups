from LFSR import LFSR
from generator import CombinerGenerator
import random as rd

def xor(b1, b2):
	return bytes(a ^ b for a, b in zip(b1, b2))

#Polynomial representation
poly1 = [19,5,2,1] # x^19+x^5+x^2+x
poly2 = [19,6,2,1] # x^19+x^6+x^2+x
poly3 = [19,9,8,5] # x^19+x^9+x^8+x^5

#the states found by my brute.py script ->
state1 = [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1]
state2 = [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0]
state3 = [1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1]
#combine function
combine = lambda x1,x2,x3 : (x1 and x2)^(x1 and x3)^(x2 and x3)

#Create LFSRs
L1 = LFSR(fpoly=poly1,state=state1)
L2 = LFSR(fpoly=poly2,state=state2)
L3 = LFSR(fpoly=poly3,state=state3)

#Create (secure) generator
generator = CombinerGenerator(combine,L1,L2,L3)

#read the encrypted flag
with open("flag.png.enc","rb") as f:
	enc_flag = f.read()

#decrypt the flag
flag = b''
key = b""
for i in range(len(clear_flag)):
	random = generator.generateByte()
	byte = enc_flag[i:i+1]
	key+=random
	flag += xor(byte,random)

#write decrypted flag
with open("flag.png","w+b") as f:
	f.write(flag)
