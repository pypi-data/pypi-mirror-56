def add(param1, param2):
    return (param1+param2)


def centuryFromYear(year):
    x = year / 100
    y = year % 100
    if y == 0:
        return int(x)
    else:
        return int(x) + 1

def checkPalindrome(inputstring):
    return inputstring==inputstring[::-1]

def adjacentElementsProduct(input):
    return max([input[i]*input[i+1]for i in range(len(input)-1)])

def shapeArea(n):
    n = (n**2)+((n-1)**2)
    return n



