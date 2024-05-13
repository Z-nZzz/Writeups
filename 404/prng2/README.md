# Poor Random Number Generator [2/2]

- **Category** : Crypto
- **Difficulty** : Medium
- **Description** : "Félicitations ! C'est vrai que mon PRNG précédent n'était pas terrible, on aurait pu voler mes affaires...
Je l'ai donc patché pour pouvoir rentrer habillé ! J'ai chiffré un nouveau fichier PNG et, cette fois-ci, j'ai essayé de limiter les données en clair qui ont fuité. Essayez de casser celui-là."
- **Files provided** : encrypt.py, generator.py, LFSR.py, flag.png.enc and flag.png.part

## Solution : 
### **TL;DR** 
 It's a **Combined LFSR** random generator used to encrypt the flag file like a one time pad, we can notice high correlations between the output of each LFSR and the output of the combining function f (see below) so a correlation attack let us recover the 3 initial states with arround 3 * 2^19 operations instead of 2^(3 * 19). Running brute.py print the recovered initial state and decrypt.py use them to decrypt the flag.

### Finding the attack
The cipher is a LFSR based stream cipher in the combiner model with 3 LFSRs of length 19 and a combining function **f(x1, x2, x3) = x1x2 + x1x3 + x2x3** when x1-3 are the output of each LFSR.

When we saw an LFSR based cipher, specifically in the combiner model there is two types of the most common attacks we need to try : 
- Algebraic attack which consist of finding a function g such that f(x)g(x) = 0 for every x, with g not null and the degree of g is less than the degree of f(2 in our case). So I checked every possible g of degree 1 (there is only 16 possiblity : 1, x1, 1 + x1, x1 + x2, x1 + x3, x1 + x2 + x3 ...) and none are annihilating f so let's check the other type of attack.
- Correlation attack for the combiner model we need to assess the correlation of the output bit of the LFSRs to the output of f *i.e* P($f(x)$ = $\alpha$ | $x_i$ = $\alpha$), for that we check the truth table of f:

|x1 |x2 |x3 |f(x) |
|-|-|-|-|
|0 |0 |0 |0 |
|0 |0 |1 |0 |
|0 |1 |0 |0 |
|0 |1 |1 |1 |
|1 |0 |0 |0 |
|1 |0 |1 |1 |
|1 |1 |0 |1 |
|1 |1 |1 |1 |

So we can see that 75% of the time f(x) is equal x1 and we have the same correlation to x2 and x3.
75 % it's high enough to allow us to distinguish the correct initial state of each LFSR from a random initial state whose generated keystream correlation with our part of the real keystream recovered with the plaintext will be arround 50% (every generated bit will have a 50% chance to be the same than the random one).  

This allow us to bruteforce every initial state independently of the others and so we need 3 times 2^19 operation instead of 2^(3 * 19)
To do that I'll just try every initial state and for each one count the differences between the generated sequence and the 280 output bits of f that we have, and store the initial states that have arround 70 errors.

```py
#Polynomial representation
poly = [[19,5,2,1], [19,6,2,1], [19,9,8,5]] 

n = pow(2, 19)
m = pow(2, 18)

#combine function
combine = lambda x1,x2,x3 : (x1 and x2)^(x1 and x3)^(x2 and x3)

#List of candidate for the 3 initial states
llstate = [[], [], []]

for j in range(3):
    #To prove that the correlation of random state is 50% I'm calculating the mean of errors with the moy variable
    moy = 0
    #Checking all the possible states from 2^18 to 2^19, i start with 2^18 to go 2 times faster now that I know the state :) 
    for k in range(m,n):
        error = 0
        x = bin(k)[2:]
        state =[0]*(19 - len(x)) + [int(xi) for xi in x ]

#Create LFSR
        L = LFSR(fpoly=poly[j],state=state)
#The key.bin have the keystream part we get from xoring the enc flag and plain part we have
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
    #Print the mean of errors to be sure it's close to 280/2
    print(moy/(n-m))
```

Then we can check if the 3 recovered state match together and have no errors with our keystream when combined :
```py
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
```
It prints :
```
state1 : [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1]
state2 : [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0]
state3 : [1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1]
```
Then we just need to use the three initial states that have been printed on the screen to decrypt the flag file as I do in decrypt.py

