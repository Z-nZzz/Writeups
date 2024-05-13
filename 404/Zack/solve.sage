from sage.all import *
from Cryptodome.Util.number import getPrime, inverse, getRandomRange, getPrime
import json
import math
import json
import zlib
import base64
from secrets import ENCFLAG

def decode(data):
    data = base64.b64decode(data)
    data = zlib.decompress(data)
    data = json.loads(data.decode("utf-8"))
    return data

input = decode (ENCFLAG)

B = input["public_key"]
ciphertext = input ["encrypted"]

m = len(B)

# Construct lattice basis
L = Matrix(ZZ, m+1, m+1)
for i in range(m):
    L[i] = [0]*i + [1] + [0]*(m-i-1) +  [B[i]]
L[m] = [0]*m + [-ciphertext]

# Perform LLL reduction
B_LLL = L.LLL()

# Check if the reduction succeeded
if B_LLL:
    for i in range(m): 
        if B_LLL[i, 0] == 0 or B_LLL[i, 0] == 1:
            message = list(B_LLL[i])[:-3]
            print(int(''.join(map(str, message)), 2).to_bytes((len(message) + 7) // 8, byteorder='big'))   



