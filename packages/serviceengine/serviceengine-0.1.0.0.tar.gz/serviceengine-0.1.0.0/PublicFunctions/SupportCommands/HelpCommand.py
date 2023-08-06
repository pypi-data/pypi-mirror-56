#!/usr/bin/python3
from PublicFunctions.CommandInterface.ICommand import ICommand
from System.EndpointMap.EndpointMapper import CommandMapping


class HelpCommand(ICommand):
    def Execute_Windows(self):
        self.GlobalHelp()

    def Execute_Linux(self):
        self.GlobalHelp()

    def GlobalHelp(self):
        helpText = "\n".join(["\t\t{0:30}{1}".format(command, CommandMapping[command].ShortHelp)
                              for command in CommandMapping if command != "help"])
        helpText = f"Public functions available. for more information type " \
                   f"--help after the desired function\n{helpText}"
        self.context.Logger.INFO(helpText)


HelpCommand.PublicFacing = "help"
HelpCommand.MinRequestParameters = 0
HelpCommand.Help = "Help"
HelpCommand.ShortHelp = "help"
