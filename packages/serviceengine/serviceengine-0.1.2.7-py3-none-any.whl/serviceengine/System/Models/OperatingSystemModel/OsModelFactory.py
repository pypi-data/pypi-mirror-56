#!/usr/bin/python3
from serviceengine.System.Models.OperatingSystemModel.OsModel import OsModel
from serviceengine.System.OperatingSystem.OperatingSystemIdentifier import GetOperatingSystemName, \
    GetOperatingSystemRelease, GetOperatingSystemVersion


def GetOsModel():
    operatingSystemName = GetOperatingSystemName()
    operatingSystemRelease = GetOperatingSystemRelease()
    operatingSystemVersion = GetOperatingSystemVersion()

    osModel = OsModel(operatingSystemName, operatingSystemRelease, operatingSystemVersion)

    return osModel
