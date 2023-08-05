def add(param1, param2):
    return param1+param2
x = add(1,2)
print(x)


import math
def centuryFromYear(x):
    if x%100==0:
        return int(x/100)
    else:
        return math.ceil(x/100)
x = centuryFromYear(1994)
print(x)


def checkPalindrome(x):
    return x == x[::-1]

def adjacentElementsProduct(x):
    z = -100
    for i in range(0,len(x)-1):
        y=x[i]*x[i+1]
        if z<y:
            z = y
    return z
x = [2,5,4,1,6,3,5]
x = adjacentElementsProduct(x)
print(x)


def shapeArea(x):
    x = (x**2)+((x-1)**2)
    return x
n = shapeArea(2)
print(n)