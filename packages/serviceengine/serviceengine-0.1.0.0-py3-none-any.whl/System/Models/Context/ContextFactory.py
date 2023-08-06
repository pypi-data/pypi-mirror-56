#!/usr/bin/python3
from System.CommandQueue.CommandQueueFactory import GetCommandQueue
from System.Models.Context.Context import Context
from System.Models.OperatingSystemModel.OsModelFactory import GetOsModel
from System.Logger.LoggerFactory import GetLogger
from System.Configurations.ConfigArchivist import GetConfig


def GetContext():
    commandQueue = GetCommandQueue()
    osModel = GetOsModel()
    config = GetConfig("SystemConfig")
    logger = GetLogger(config, osModel.OperatingSystemName)
    context = Context(commandQueue, osModel, logger, config)
    commandQueue.SetContext(context)
    return context
