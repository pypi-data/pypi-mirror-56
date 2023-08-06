#!/usr/bin/python3
from PublicFunctions.CommandInterface.ICommand import ICommand
from System.MultiProcessing.MultiProcessing import RunCommandsAsync, RunCommandAsync


class AsyncCommand(ICommand):
    def Execute_Windows(self):
        self.RunAsync()

    def Execute_Linux(self):
        self.RunAsync()

    def RunAsync(self):
        RunCommandsAsync(self.request)


AsyncCommand.PublicFacing = "async"
AsyncCommand.MinRequestParameters = 1
AsyncCommand.Help = "Receives a command or list of commands and runs them via thread pool concurrently\n" \
                    "async [command] [command]...\n" \
                    "command - a command that will be run async, all commands passed must be wrapped in parentheses"
AsyncCommand.ShortHelp = "Runs the added command(s) concurrently"
