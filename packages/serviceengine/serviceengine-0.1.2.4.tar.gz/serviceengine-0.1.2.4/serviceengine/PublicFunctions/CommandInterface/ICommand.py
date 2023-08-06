#!/usr/bin/python3
import abc

from serviceengine.PublicFunctions.ShellCommands.ShellCommandExecutor.ShellCommandExecutor import RunSubProcess


class ICommand(metaclass=abc.ABCMeta):
    def __init__(self, request, context):
        self.request = request
        self.context = context

    def Execute(self):
        self.context.Logger.DEBUG(f"Running command '{self.PublicFacing}' with parameters {str(self.request)}")
        if self.request and len(self.request) > 0 and "--help" in self.request:
            self.RunHelpCommand()
            return
        if not self.ValidateRequestContainsMinimumRequiredParameters(self.MinRequestParameters):
            self.context.Logger.WARN(f"Missing required parameters (min amount: {self.MinRequestParameters})")
            return
        self.RunCommandBasedOnOperatingSystem()

    def ValidateRequestContainsMinimumRequiredParameters(self, minParams=0):
        requestHasAtLeastMinRequiredParams = True if (minParams == 0) or (self.request and len(self.request) >= minParams) else False
        return requestHasAtLeastMinRequiredParams

    def RunCommandBasedOnOperatingSystem(self):
        if str.lower(self.context.OsModel.OperatingSystemName) == "windows":
            self.Execute_Windows()
        elif str.lower(self.context.OsModel.OperatingSystemName) == "linux":
            self.Execute_Linux()
        else:
            self.context.Logger.WARN("unsupported OS")
            return

    def RunHelpCommand(self):
        self.context.Logger.INFO('\t\t'.join(('\t\t' + self.Help.lstrip()).splitlines(True)))

    def RunShellCommand(self, command):
        RunSubProcess(command, self.context.Logger)

    @abc.abstractmethod
    def Execute_Windows(self):
        pass

    @abc.abstractmethod
    def Execute_Linux(self):
        pass