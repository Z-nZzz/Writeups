# Zack à dos 

- **Category** : Crypto
- **Difficulty** : Medium
- **Description** : "Vous vous avancez sur le plongeoir, la foule est tellement en liesse que la planche en tremble. C'est le dernier saut avant d'avoir votre note finale et donc votre classement pour ce sport. Vous sautez, le monde se ralentit et, comme à l'entrainement, vous effectuez l'enchaînement de figures que vous avez travaillées. Une fois la tête sortie de l'eau, personne du jury ne montre de note ! Un flash vous frappe, c'est vrai que la note est transmise par chiffrement RSA ! Mais après vos multiples figures aériennes, vous ne vous souvenez que de votre clef publique, et de la trajectoire que vous avez empruntée..."
- **Files provided** : PlongeonRapideSuperArtistique.py

## Solution : 
### **TL;DR**
It's easier to factor polynomial than integer, so we can just factor N and retrieve r by finding the roots of N-n with the built-in functions of sagemath.

### Source

```py
from sage.all import *
from Cryptodome.Util.number import long_to_bytes

N = 9621137267597279445*x^14 + 18586175928444648302*x^13 + 32676401831531099971*x^12 + 42027592883389639924*x^11 + 51798494845427766041*x^10 + 63869556820398134000*x^9 + 74077517072964271516*x^8 + 79648012933926385783*x^7 + 69354747135812903055*x^6 + 59839859116273822972*x^5 + 48120985784611588945*x^4 + 36521316280908315838*x^3 + 26262107762070282460*x^2 + 16005081865177344119*x + 5810204145325142255 

n = 60130547801168751450983574194169752606596547774564695794919298973251203587128237799602582911050022571941793197314565314876508860461087209144687558341117955877761335067848122512358149929745084363835027292307961660634453113069168408298081720503728087287329906197832876696742245078666352861209105027134133927

c = 15129303695051503318505193172155921684909431243538868778377472653134183034984012506799855760917107279844275732327557949646134247015031503441468669978820652020054856908495646419146697920950182671202962511480958513703999302195279666734261744679837757391212026023983284529606062512100507387854428089714836938

#P obtained by using factor(N) with sage cli, i had trouble with the format of the output
P = 3378269265*x^7 + 2605358264*x^6 + 3892229888*x^5 + 2653862544*x^4 + 3893610093*x^3 + 2932575439*x^2 + 2322600571*x + 2442728695
r  = (N-n).roots()[0][0]
p = int(P(x=r))

#classic rsa decryption
q = n//p
phi = (p-1)*(q-1)
d = inverse_mod(65537, phi)
print(long_to_bytes(int(pow(c, d, n))))
```


