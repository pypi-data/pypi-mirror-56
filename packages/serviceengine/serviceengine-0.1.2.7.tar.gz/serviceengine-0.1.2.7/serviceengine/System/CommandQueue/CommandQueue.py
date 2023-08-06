#!/usr/bin/python3
import queue
import shlex
from serviceengine.System.EndpointMap.EndpointMapper import CommandMapping


class CommandQueue:
    def __init__(self):
        self.commandQueue = queue.Queue()
        self.tempQueue = queue.Queue()
        self.context = None

    def SetContext(self, context):
        self.context = context

    def CommandQueueNotEmpty(self):
        return not self.commandQueue.empty()

    def EnqueueCommands(self, commands):
        for command in commands:
            commandClass = self.GetCommandClass(command)
            if commandClass:
                self.commandQueue.put(commandClass)
        self.context.Logger.System(f"Enqueued {len(commands)} commands last")

    def EnqueueCommandsNext(self, commands):
        while not self.commandQueue.empty():
            self.tempQueue.put(self.commandQueue.get())
        for command in commands:
            commandClass = self.GetCommandClass(command)
            if commandClass:
                self.commandQueue.put(commandClass)
        while not self.tempQueue.empty():
            self.commandQueue.put(self.tempQueue.get())
        self.context.Logger.System(f"Enqueued {len(commands)} commands next")

    def DeQueueCommand(self):
        return self.commandQueue.get() if self.CommandQueueNotEmpty() else None

    def EmptyCommandQueue(self):
        while not self.commandQueue.empty():
            self.commandQueue.get()

    def GetCommandClass(self, request):
        if not request:
            return None
        request = shlex.split(request)
        if len(request) < 1:
            return None

        requestedCommand = str.lower(request[0])
        if requestedCommand not in CommandMapping:
            self.context.Logger.WARN(f"No such api found '{requestedCommand}'")
            return None

        requestArgs = request[1:] if len(request) > 1 else None
        return CommandMapping[requestedCommand](requestArgs, self.context)

    def RunCommands(self):
        while self.CommandQueueNotEmpty():
            command = self.DeQueueCommand()
            try:
                command.Execute()
            except Exception as ex:
                self.context.Logger.ERROR(f"Encountered error executing command:\n{ex}\nEmptying command queue")
                self.EmptyCommandQueue()
                return

