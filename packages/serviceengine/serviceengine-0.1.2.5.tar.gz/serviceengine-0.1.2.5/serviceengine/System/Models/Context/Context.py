#!/usr/bin/python3


class Context:
    def __init__(self, commandQueue, osModel, logger, config):
        self.CommandQueue = commandQueue
        self.OsModel = osModel
        self.Logger = logger
        self.Config = config
