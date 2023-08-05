def add(param1, param2):
    return param1 + param2


def centuryFromYear(year):
    import math
    if year / 100 <= 1:
        return 1
    else:
        return math.ceil(year / 100)


def checkPalindrome(inputString):
    lt = len(inputString)
    for i in range(0, int(lt / 2) + 1):
        if inputString[i] != inputString[lt - 1 - i]:
            return False
    return True


def adjacentElementsProduct(inputArray):
    high = -1000000
    for idx, i in enumerate(inputArray):
        if idx < len(inputArray) - 1:
            if (inputArray[idx] * inputArray[idx + 1]) > high:
                high = inputArray[idx] * inputArray[idx + 1]
    return high


def shapeArea(n):
    n = int(n)
    return (n ** 2) + ((n - 1) ** 2)
