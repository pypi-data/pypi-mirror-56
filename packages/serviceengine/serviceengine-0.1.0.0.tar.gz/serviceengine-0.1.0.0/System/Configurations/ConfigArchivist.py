#!/usr/bin/python3
from System.FileSystem.FileSystem import ReadJsonFile


configDictionary = {
    "SystemConfig": "System/Configurations/SystemConfig.json"
}
configMemory = {}


def GetConfig(name):
    if not name:
        return {}
    if name in configMemory:
        return configMemory[name]
    if name in configDictionary:
        path = configDictionary[name]
        config = ReadJsonFile(path)
        configMemory[name] = config
        return config
