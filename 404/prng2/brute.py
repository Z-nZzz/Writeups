from LFSR import LFSR
from generator import CombinerGenerator
import random as rd
import bitarray
from Cryptodome.Util.number import bytes_to_long long_to_bytes

def xor(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

#Getting the first bytes of the keystream using the provided plaintext
def get_key(enc,plain):
    key = b''
    key += xor(enc,plain)
    return key

with open("flag.png.part",'rb') as f:
    flagpart = f.read()

with open("flag.png.enc",'rb') as f:
    flagenc = f.read(len(flagpart))

with open('key.bin', 'w+b') as f:
    f.write(get_key(flagenc, flagpart))

#Polynomial representation
poly = [[19,5,2,1], [19,6,2,1], [19,9,8,5]] 
# x^19+x^9+x^8+x^5,  x^19+x^6+x^2+x, x^19+x^5+x^2+x
n = pow(2, 19)
m = pow(2, 18)

#combine function
combine = lambda x1,x2,x3 : (x1 and x2)^(x1 and x3)^(x2 and x3)

#List of candidate for the 3 initial states
llstate = [[], [], []]

for j in range(3):
    moy = 0
    for k in range(m,n):
        error = 0
        x = bin(k)[2:]
        state =[0]*(19 - len(x)) + [int(xi) for xi in x ]
        # initialize states
        #state1 = [rd.randint(0,1) for _ in range(max(poly1))] 
        #state2 = [rd.randint(0,1) for _ in range(max(poly2))]
        #state3 = [rd.randint(0,1) for _ in range(max(poly3))]

#Create LFSR
        L = LFSR(fpoly=poly[j],state=state)

        with open("key.bin","rb") as f:
	        key = f.read()
        bIn = bitarray.bitarray()
        bIn.frombytes(key)
        key = bIn
        for i in range(len(key)):
            random = L.generateBit()
            b = key[i]
            if random != b :
                error+=1
        #Now we check if the correlation is arround 75% so the number of error should be arround 70 hence the < 85
        if error < 85:
            llstate[j].append(state)
        moy += error
    print(moy/(n-m))

print(len(llstate[0]))
print(len(llstate[1]))
print(len(llstate[2]))

for state1 in llstate[0]:
    for state2 in llstate[1]:
        for state3 in llstate[2]:
    #Create LFSRs
            error = 0
            L1 = LFSR(fpoly=poly[0],state=state1)
            L2 = LFSR(fpoly=poly[1],state=state2)
            L3 = LFSR(fpoly=poly[2],state=state3)

#Create (secure) generator
            generator = CombinerGenerator(combine,L1,L2,L3)
            with open("key.bin","rb") as f:
                key = f.read()

            for i in range(len(key)):
                random = generator.generateByte()
                byte = key[i:i+1]
                for a,b in zip (bin(bytes_to_long(byte)), bin(bytes_to_long(random))):
                    if a!=b :
                        error +=1
            if error <=0 :
                print("state1 :", state1)
                print("state2 :", state2)
                print("state3 :", state3)



