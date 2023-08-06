#!/usr/bin/python3
from PublicFunctions.CommandInterface.ICommand import ICommand


class LoopCommand(ICommand):
    def Execute_Windows(self):
        self.Loop()

    def Execute_Linux(self):
        self.Loop()

    def Loop(self):
        loopTimes = self.request[0]
        loopCommand = " ".join(self.request[1:])
        try:
            loopTimesInt = int(loopTimes)
        except ValueError:
            self.context.Logger.ERROR(f"Requested loop times '{loopTimes}' not valid integer")
            return

        newCommands = [loopCommand] * loopTimesInt
        self.context.CommandQueue.EnqueueCommandsNext(newCommands)


LoopCommand.PublicFacing = "loop"
LoopCommand.MinRequestParameters = 2
LoopCommand.Help = "Repeats the command a requested amount of times\n" \
                   "loop [count] [command]\n" \
                   "count- The amount of times the command will be repeated\n" \
                   "command- The command that will be run"
LoopCommand.ShortHelp = "Repeats the command a requested amount of times"
