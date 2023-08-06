#!/usr/bin/python3
import os


def GetEnvironmentVariableWindows(variableName):
    return os.getenv(variableName)


def GetEnvironmentVariableLinux(variableName):
    return os.environ[variableName]
