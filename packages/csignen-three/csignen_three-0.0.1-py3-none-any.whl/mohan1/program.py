def add(param1, param2):
   return param1+param2


def centuryFromYear(year):
    x = year // 100
    y = year % 100
    if y == 0:
        return x
    else:
        return (x + 1)




def checkPalindrome(inputString):
    return inputString==inputString[::-1]
