#!/usr/bin/python3
from serviceengine.PublicFunctions.CommandInterface.ICommand import ICommand


class UpgradeCommand(ICommand):
    def Execute_Windows(self):
        self.context.Logger.ERROR("Not Implemented")

    def Execute_Linux(self):
        self.context.Logger.ERROR("Not Implemented")


UpgradeCommand.MinRequestParameters = 0
UpgradeCommand.Help = "Upgrades the application to latest stable version\n" \
                      "upgrade\n" \
                      "This command does not support any additional arguments"
UpgradeCommand.ShortHelp = "Upgrades the application to latest stable version"
