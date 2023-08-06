#!/usr/bin/python3
from serviceengine.System.CommandQueue.CommandQueueFactory import GetCommandQueue
from serviceengine.System.Configurations.ConfigArchivist import GetConfig
from serviceengine.System.Logger.LoggerFactory import GetLogger
from serviceengine.System.Models.Context.Context import Context
from serviceengine.System.Models.OperatingSystemModel.OsModelFactory import GetOsModel


def GetContext():
    commandQueue = GetCommandQueue()
    osModel = GetOsModel()
    config = GetConfig("SystemConfig")
    logger = GetLogger(config, osModel.OperatingSystemName)
    context = Context(commandQueue, osModel, logger, config)
    commandQueue.SetContext(context)
    return context
