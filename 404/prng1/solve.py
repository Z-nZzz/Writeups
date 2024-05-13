#from my_random import Generator
from solve_random import Generator
from Cryptodome.Util.number import long_to_bytes
def xor(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

def get_blocks(data,block_size):
	return [data[i:i+block_size] for i in range(0,len(data),block_size)]

def pad(data,block_size):
	return data+b'\x00'*(block_size-len(data)%block_size)

#Using the custom generator (see solve_random.py) to decrypt
def decrypt(data,block_size):
	padded_data = pad(data,block_size)
	data_blocks = get_blocks(padded_data,block_size)
	generator = Generator()
	encrypted = b''

	for block in data_blocks:

		rd = generator.get_random_bytes(block_size)
		xored = xor(block,rd)
		encrypted+= xored
	return encrypted

#Getting the first bytes of the keystream using the plaintext
def get_key(encdata,plaindata,block_size):
	padded_data = pad(plaindata,block_size)
	enc_blocks = get_blocks(encdata,block_size)
	plain_blocks = get_blocks(padded_data,block_size)
	encrypted = b''

	for plainblock, encblock in zip(enc_blocks, plain_blocks):
		xored = xor(encblock,plainblock)
		encrypted+= xored
	return encrypted

BLOCK_SIZE = 4

with open("flag.png.part",'rb') as f:
	flagpart = f.read()

with open("flag.png.enc",'rb') as f:
	flagenc = f.read(len(flagpart))

with open('key.bin', 'w+b') as f:
	f.write(get_key(flagenc, flagpart, BLOCK_SIZE))

f = open("flag.png.enc",'rb')
f.read(2000)
flag = f.read()

g = open('flag.png', 'w+b')
g.write(flagpart[:2000])
g.write(decrypt(flag,BLOCK_SIZE))

'''
flag = None

with open("flag.png",'rb') as f:
	flag = f.read()

with open('flag.png.enc', 'w+b') as f:
	f.write(encrypt(flag,BLOCK_SIZE))
'''
