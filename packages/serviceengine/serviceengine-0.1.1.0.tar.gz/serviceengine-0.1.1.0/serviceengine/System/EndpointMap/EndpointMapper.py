#!/usr/bin/python3
import os
from os.path import dirname
from System.Reflection.Reflection import GetPublicFacingFunctionsFromPath

root = f"{dirname(dirname(dirname(dirname(__file__))))}/"
CommandMapping = {}


def GetProjectPythonFiles(fileList, directory):
    return [file for file in fileList
            if not file[0] == '.'
            and not file[0] == "_"
            and file.endswith(".py")
            and not directory.startswith("venv")
            and not directory.startswith(".")]


def GetParsedRelativeFilePath(fileName, directory):
    relativeFilePath = os.path.join(directory, fileName)
    relativeFilePath = relativeFilePath.replace("\\", ".")
    relativeFilePath = relativeFilePath.replace("/", ".")
    relativeFilePath = relativeFilePath.replace(".py", "")
    return relativeFilePath


def GetProjectFilesPaths():
    result = []
    for dir_, _, files in os.walk(root):
        directory = os.path.relpath(dir_, root)
        result.extend([GetParsedRelativeFilePath(fileName, directory)
                       for fileName
                       in GetProjectPythonFiles(files, directory)])
    return result


def CreatePublicEndpointMap():
    commandTypes = GetProjectFilesPaths()
    for commandPath in commandTypes:
        for command in GetPublicFacingFunctionsFromPath(commandPath):
            CommandMapping[str.lower(command[1].PublicFacing)] = command[1]
