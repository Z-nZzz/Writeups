# Poor Random Number Generator [1/2]

- **Category** : Crypto
- **Difficulty** : easy
- **Description** : "J'ai chiffré le fichier flag.png. Malheureusement, une partie du clair a fuité. Cependant, j'ai confiance en mon algorithme de chiffrement : un One Time Pad, c'est incassable !"
- **Files provided** : encrypt.py, my_random.py, flag.png.enc and flag.png.part

## Solution : 
**TL;DR** : It's an **LFSR like** random generator used to encrypt the flag file like a one time pad, and we have enough plain data to recover an entire state of the registers so we can run the cipher with it as an initial state to decrypt the remaining part of the image. Run **_python3 solve.py_** with solve_random.py and the 2 flag.* in the same directory and **flag.png** shoud spawn.

We do not need to care about how this pseudo LFSR is implemented or how the feedback function work in the Generator class of my_random.py we just need an entire state of length 2000 because every byte of the keystream depends only on the 2000 previous ones, and hopefully we have more than 2000 bytes of plain data in flag.png.part.

First we get the 2000 bytes of the keystream we need by xoring the plain data with the begining of the enc data. I did so in the solve.py with the function get_key:

```py
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
```
I write the result in a file named key.bin, this file will be used by solve_random.py which is a copy of my_random.py where i replaced the initialisation of the Generator seed by the "key" we recovered.
```py
class Generator:
    def __init__(self):
        with open('key.bin', 'rb') as f:
            #Getting the recovered key from key.bin
            self.feed = [int.from_bytes(f.read(1), 'big') for i in range(2000)]
```
Finally, back to solve.py we just call Generator() in the **decrypt** function (which is just a copy of the encrypt function) it will use our key to decrypt the flag file.
```py
f = open("flag.png.enc",'rb')
f.read(2000)
flag = f.read()

g = open('flag.png', 'w+b')
g.write(flagpart[:2000])
g.write(decrypt(flag,BLOCK_SIZE))
```
