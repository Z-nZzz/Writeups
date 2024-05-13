# Le petit bain 

- **Category** : Crypto
- **Difficulty** : easy
- **Description** : "Malheureusement, votre revanche contre votre adversaire de toujours s'est soldée par une défaite. En toute bonne foi, vous suspectez de la triche. Vous décidez vivement de fouiller son casier et tombez sur un étrange mot. À vous de le déchiffrer."
- **Files provided** : challenge.py

## Solution : 
**TL;DR** : It's an **afine cipher** with a permutation to add confusion, where we got a part of the flag long enough to get the key, the composition of afine cipher is an affine cipher and note that every slice of size 6 of the permutation is stable and runnned 6 times the permutation is equal to identity so we can ignore it.
These properties allow use to deduce that every char are encrypted idenpendently by a single affine cipher with 6 int long key.

For two couple $(p_i, c_i)$ and $(p_{i+6}, c_{i+6})$ _plain char / encrypted char_, we can retrieve the int of the key used to encrypt the two char (i+6 because the key is of length 6 and pi is encrypted with the same int of the key than every $p_{i+k*6}$) by doing :

$c_i$ = A[i%6] * $p_i$ + B[i+6%6]

$c_{i+6}$ = A[i+6%6] * $p_{i+6}$ + B[i+6%6]

$c_{i+6}$ = A[i%6] * $p_{i+6}$ + B[i%6]

Hence A[i%6] = ($c_i$ - $c_{i+6}$) * inverse($p_{i}$ - $p_{i+6}$, n)
and  B[i%6] = $c_i$ - A[%6] * $p_i$

_We use the modular inverse function from PyCryptodome_

```py
plain = "404CTF{tHe_c"

out ="C_ef8K8rT83JC8I0fOPiN6P!liE03W2NXFh1viJCROAqXb6o"
A=[]
B=[]
for i in range(6):
        p1 = charset.index(plain[i])
        p2 = charset.index(plain[i+6])
        c1 = charset.index(out[i])
        c2 = charset.index(out[i+6])
        a = (c1-c2)*inverse(p1-p2, n)
        A.append(a)
        B.append(c2 - a*p2)
decrypted=""
for i in range(len(out)):
		x = charset.index(out[i])
		a = A[i%6]
		b = B[i%6]
		x = ((x-b) * inverse(a, n))%n
		decrypted += charset[x]

print(decrypted)
```
