#!/usr/bin/python3
import inspect
import sys
import importlib


def GetFunctionsFromPath(filePath):
    importlib.import_module(filePath)
    return inspect.getmembers(sys.modules[filePath], inspect.isclass)


def GetFunctionsWithAttributeFromPath(filePath, attribute):
    return [mem for mem in GetFunctionsFromPath(filePath) if hasattr(mem[1], attribute)]


def GetPublicFacingFunctionsFromPath(filePath):
    return GetFunctionsWithAttributeFromPath(filePath, "PublicFacing")
