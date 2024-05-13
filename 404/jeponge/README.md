# J'éponge donc j'essuie 

- **Category** : Crypto
- **Difficulty** : Medium
- **Description** : "En faisant de la plongée sous-marine avec un ami gorfou, je suis tombé sur un animal plutôt réservé mais fort sympathique ! J'ai donc décidé de faire mon propre algorithme de hash. Je vous mets au défi de le casser."
- **Files provided** : challenge.py

## Solution : 
### **TL;DR** 
Just sent the following hex string "0" * (512 - 2 * len(str) - 4) + len(str) + str + len(str), with len(srt) = 16 = 0x10, for instance : 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001080f4491e946399d2dd02feca4b8c09d410

### Why ?
We add zeros because it is neutral for the xor operation used in the absorb function to update the state vector.
```py
self.state[0] = self.xor(self.state[0],input_data)
```

The total length of our payload is 512 so 256 bytes, hence the two bytes added at the beginning in the __init__ function will add zeros before and after our string.
```py
data = long_to_bytes(len(data)%256)+data+long_to_bytes(len(data)%256)
```

I add the two "len(str)" in my payload because thats what the init function did to hash the legit string initially and we want the result to be exactly the same, they are also the reason of the "-4" in the number of zeros I'm adding.


