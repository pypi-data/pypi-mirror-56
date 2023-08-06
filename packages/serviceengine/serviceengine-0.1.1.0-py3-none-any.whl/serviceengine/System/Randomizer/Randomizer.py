#!/usr/bin/python3
import random
import string


def GetRandomString(size, includeDigits=True):
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(size)]) if includeDigits else\
        ''.join([random.choice(string.ascii_letters) for n in range(size)])


def GetRandomInt(size):
    minNum = 10**(size - 1)
    maxNum = (10**size) - 1
    return random.randint(minNum, maxNum)
