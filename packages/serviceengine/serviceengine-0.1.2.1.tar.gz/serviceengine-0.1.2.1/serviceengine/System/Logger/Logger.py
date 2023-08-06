#!/usr/bin/python3
import datetime

from serviceengine.System.FileSystem.FileSystem import CreateDirIfNone, AppendToFile
from serviceengine.System.Logger.Colors import Color_Blue, Color_Default, Color_Green, Color_Orange, Color_Red
from serviceengine.System.Randomizer.Randomizer import GetRandomString


class Logger:
    def __init__(self, config, osType):
        self.Config = config
        self.LogFolderPath = self.Config["Logger"]["LogFilePath"][osType]
        self.LogFileName = self.GetLogFileName()
        CreateDirIfNone(self.LogFolderPath)
        return

    def LogDecorator(messageType, messageColor):
        def InnerDecorator(func):
            def LogLogic(self, message, unencryptedParams={}, encryptedParams={}):
                self.LogMessage(message, messageType, unencryptedParams, encryptedParams)
                self.DisplayMessage(message, messageColor, messageType)
            return LogLogic
        return InnerDecorator

    @LogDecorator("System", Color_Green)
    def System(self, message, unencryptedParams={}, encryptedParams={}):
        pass

    @LogDecorator("Info", Color_Default)
    def INFO(self, message, unencryptedParams={}, encryptedParams={}):
        pass

    @LogDecorator("Debug", Color_Blue)
    def DEBUG(self, message, unencryptedParams={}, encryptedParams={}):
        pass

    @LogDecorator("Warn", Color_Orange)
    def WARN(self, message, unencryptedParams={}, encryptedParams={}):
        pass

    @LogDecorator("Error", Color_Red)
    def ERROR(self, message, unencryptedParams={}, encryptedParams={}):
        pass
    
    def CreateLogMessage(self, message, messageType, unencryptedParams={}, encryptedParams={}):
        message = f"{self.GetLogTime()}({messageType}): {message}\n"
        if bool(unencryptedParams):
            message = f"{message}\n{self.GetStringFromParamsDictionary(unencryptedParams, False)}"
        if bool(encryptedParams):
            message = f"{message}\n{self.GetStringFromParamsDictionary(encryptedParams, True)}"
        return message

    def GetStringFromParamsDictionary(self, dictionary, encrypt):
        message = f"unencryptedParams:\n" if not encrypt else f"encryptedParams:\n"
        for key in dictionary:
            message = f"{message}\n         {key}: {dictionary[key]}" if not encrypt \
                else f"{message}\n         {key}: {hash(dictionary[key])}"

    def LogMessage(self, message, messageType, unencryptedParams={}, encryptedParams={}):
        if self.LoggingPermitted("Display", messageType):
            parsedMessage = self.CreateLogMessage(message, messageType, unencryptedParams, encryptedParams)
            AppendToFile(self.LogFileName, parsedMessage)

    def DisplayMessage(self, message, color, messageType):
        if self.LoggingPermitted("Display", messageType):
            print(f"{color}{message}{Color_Default}")

    def LoggingPermitted(self, ActionType, messageType):
        logToFileAllPermitted = bool(self.Config["Logger"][ActionType]["all"])
        logToFileSpecificPermitted = bool(self.Config["Logger"][ActionType][messageType])
        return logToFileAllPermitted and logToFileSpecificPermitted

    def GetLogTime(self):
        now = datetime.datetime.now()
        parsedTime = f"{now.day}.{now.month}.{now.year}/{now.hour}:{now.minute}:{now.second}"
        return parsedTime

    def GetLogFileName(self):
        now = datetime.datetime.now()
        path = f"{self.LogFolderPath}/Log_{now.day}{now.month}{now.year}"
        if bool(self.Config["Logger"]["LogFileForEachContext"]):
            random = GetRandomString(5)
            path = f"{path}_{random}"
        path = f"{path}.txt"
        return path
