# lambda functions
impar = lambda n: n % 2 != 0
positive = lambda n: n > 0
maior = lambda x,y: x > y

import math
polar = lambda x,y: (math.sqrt(x*x + y*y), math.atan2(y, x))

def ex4_5(f,g,h):
    return lambda x,y,z: h(f(x,y), g(y,z))        
    


print(impar(2))
print(positive(3))
print(maior(3,4))
print(polar(2,4))
print(ex4_5(lambda a,b : a+b, lambda a,b: a*b, lambda a,b: a > b)(1,2,3))