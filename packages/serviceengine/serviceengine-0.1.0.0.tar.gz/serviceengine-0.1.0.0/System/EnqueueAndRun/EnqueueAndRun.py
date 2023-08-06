#!/usr/bin/python3
from System.Models.Context.ContextFactory import GetContext


def EnqueueAndRun(request):
    context = GetContext()
    context.CommandQueue.EnqueueCommands([request])
    context.CommandQueue.RunCommands()
