# Zack Adeaux

- **Category** : Crypto
- **Difficulty** : Medium
- **Description** : "Vous et votre ami Zack partez ensemble pour votre cours de natation habituel. Vers la moitié du trajet, votre ami décide de vous montrer sa toute nouvelle paire de lunettes de natation, cependant impossible de remettre la main dessus ! Vous décidez de l'aider mais vous vous rendez vite compte que son sac de piscine est un vrai bazar ! Étant un peu maniaque, vous décidez d'y mettre un peu d'ordre."
- **Files provided** : challenge.py
- **A remote server was providing the ciphertext and the public key, I stored one in secrets.py under the name ENCFLAG**

## Solution : 
### **TL;DR**
It's a Merkle-Hellman trapdoor knapsack cipher, so we just need : 
# LLL

### Source
I just implemented the attack I found at https://shrek.unideb.hu/~tengely/crypto/section-10.html with sage :

```py
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
        #Looking for binary array
        if B_LLL[i, 0] == 0 or B_LLL[i, 0] == 1:
            message = list(B_LLL[i])[:-3]
            print(int(''.join(map(str, message)), 2).to_bytes((len(message) + 7) // 8, byteorder='big'))
```


