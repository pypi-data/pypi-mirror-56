#!/usr/bin/python3
from System.Logger.Logger import Logger


def GetLogger(config, osType):
    return Logger(config, osType)
