#!/usr/bin/python3
from serviceengine.System.EndpointMap.EndpointMapper import CreatePublicEndpointMap
from serviceengine.System.Models.Context.ContextFactory import GetContext


def InitAndGetContext():
    CreatePublicEndpointMap()
    context = GetContext()
    return context


def EnqueueAndRun(request):
    context = InitAndGetContext()
    context.Logger.System(f"user input: {request}")
    context.CommandQueue.EnqueueCommands([request])
    context.CommandQueue.RunCommands()


def Start(sysargs=None):
    context = InitAndGetContext()
    if sysargs and len(sysargs) > 1:
        EnqueueAndRun(" ".join(sysargs[1:]))
    while True:
        context.Logger.System("Please enter your next command")
        EnqueueAndRun(input(""))
