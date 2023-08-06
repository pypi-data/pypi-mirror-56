#!/usr/bin/python3
from serviceengine.System.FileSystem.FileSystem import ReadJsonFile
from os.path import dirname

root = f"{dirname(__file__)}/"

configMemory = {}


def GetConfig(name):
    if not name:
        return {}
    if name in configMemory:
        return configMemory[name]
    path = f"{root}{name}.json"
    print(path)
    config = ReadJsonFile(path)
    configMemory[name] = config
    return config
