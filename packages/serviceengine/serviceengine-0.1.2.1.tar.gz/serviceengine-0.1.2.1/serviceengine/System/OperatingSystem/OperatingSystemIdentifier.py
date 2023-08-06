#!/usr/bin/python3
import platform


def GetOperatingSystemName():
    return platform.system()


def GetOperatingSystemRelease():
    return platform.release()


def GetOperatingSystemVersion():
    return platform.version()
