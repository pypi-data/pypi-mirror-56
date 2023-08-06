#!/usr/bin/python3
from serviceengine.System.FileSystem.FileSystem import ReadJsonFile
from os.path import dirname
from os import walk

root = f"{dirname(__file__)}/"

configMemory = {}


def GetConfig(name):
    if not name:
        return {}
    if name in configMemory:
        return configMemory[name]
    path = f"{root}{name}.json"
    config = ReadJsonFile(path)
    print(config)
    printit(path)
    configMemory[name] = config
    return config


def printit(mypath):
    print(mypath)
    result = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        result.extend(filenames)
        break
    print(result)
