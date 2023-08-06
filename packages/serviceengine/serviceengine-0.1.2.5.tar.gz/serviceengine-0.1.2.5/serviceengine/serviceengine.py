#!/usr/bin/python3
from serviceengine.System.EndpointMap.EndpointMapper import CreatePublicEndpointMap
from serviceengine.System.Models.Context.ContextFactory import GetContext


def InitAndGetContext(functionsPackagePath=None):
    CreatePublicEndpointMap(functionsPackagePath)
    context = GetContext()
    return context


def EnqueueAndRun(context, request=""):
    context.Logger.System(f"user input: {request}")
    context.CommandQueue.EnqueueCommands([request])
    context.CommandQueue.RunCommands()


def Start(functionsPackagePath=None, sysargs=None):
    context = InitAndGetContext(functionsPackagePath)
    if sysargs and len(sysargs) > 1:
        EnqueueAndRun(context, " ".join(sysargs[1:]))
    while True:
        context.Logger.System("Please enter your next command")
        EnqueueAndRun(context, input(""))
