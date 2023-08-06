#!/usr/bin/python3
from System.FileSystem.FileSystem import ReadFile, ReadOnlineFile
from System.Regex.Regex import httpRegex


class SLI:
    def __init__(self, context):
        self.Context = context

    def RunScript(self, path):
        isValid, scriptFileContent = self.GetFileContentIfExistsAndIsValid(path)
        if not isValid:
            return

        scriptFileContent = self.RemoveComments(scriptFileContent)

        scriptIsValid = self.ScriptIsValid(scriptFileContent)
        if not scriptIsValid:
            return

        self.Context.CommandQueue.EnqueueCommands(scriptFileContent)

    def RemoveComments(self, scriptFileContent):
        return [x for x in scriptFileContent if not x.startswith('#')]

    def ScriptIsValid(self, scriptFileContent):
        return True

    def GetFileContentIfExistsAndIsValid(self, path):
        scriptFileContent = ReadFile(path) if not httpRegex.match(path) else ReadOnlineFile(path)
        if not scriptFileContent or len(scriptFileContent) == 0:
            self.Context.Logger.ERROR("Script file Empty or cannot be found", {"path": path})
            return False, ""

        return True, scriptFileContent

