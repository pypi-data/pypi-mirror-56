#!/usr/bin/python3
import os
from serviceengine.System.Reflection.Reflection import GetPublicFacingFunctionsFromPath

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


def GetProjectFilesPaths(functionsPackagePath):
    result = []
    for dir_, _, files in os.walk(functionsPackagePath):
        directory = os.path.relpath(dir_, functionsPackagePath)
        result.extend([GetParsedRelativeFilePath(fileName, directory)
                       for fileName
                       in GetProjectPythonFiles(files, directory)])
    return result


def GetProjectFilesPathFromList(functionsPackagePath):
    result = []
    for packageDirectories in functionsPackagePath:
        for dir_, _, files in os.walk(packageDirectories):
            directory = os.path.relpath(dir_, packageDirectories)
            result.extend([GetParsedRelativeFilePath(fileName, directory)
                           for fileName
                           in GetProjectPythonFiles(files, directory)])
    return result


def CreatePublicEndpointMap(root, functionsPackagePath=None):
    commandTypes = GetProjectFilesPaths(root)
    for commandPath in commandTypes:
        for command in GetPublicFacingFunctionsFromPath(f"serviceengine.{commandPath}"):
            CommandMapping[str.lower(command[1].PublicFacing)] = command[1]

    if functionsPackagePath and len(functionsPackagePath) > 0:
        commandTypes = GetProjectFilesPathFromList(functionsPackagePath)
        for commandPath in commandTypes:
            for command in GetPublicFacingFunctionsFromPath(commandPath):
                CommandMapping[str.lower(command[1].PublicFacing)] = command[1]
