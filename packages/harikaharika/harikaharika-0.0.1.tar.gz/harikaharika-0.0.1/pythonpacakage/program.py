def add(param1, param2):
    c=param1+param2
    return(c)

def centuryFromYear(year):
    x=year/100
    y=year%100
    if y==0:
        return x
    else:
        return int(x+1)

def checkPalindrome(inputString):
    if inputString==inputString[::-1]:
        return True
    else:
        return False

def adjacentElementsProduct(inputArray):
    a=inputArray
    l=len(a)
    sum=[]
    for i in range(l-1):
        sum.append(a[i]*a[i+1])
    return max(sum)

def shapeArea(n):
    area = 1
    while n>1:
        area += (n-1)*4
        n -=1
    return area