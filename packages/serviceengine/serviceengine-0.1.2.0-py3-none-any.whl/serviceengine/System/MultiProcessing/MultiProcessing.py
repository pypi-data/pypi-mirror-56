#!/usr/bin/python3
import multiprocessing
from multiprocessing import Process
from serviceengine.System import EnqueueAndRun
from serviceengine.System.Configurations.ConfigArchivist import GetConfig


def RunCommandAsync(command):
    Process(target=EnqueueAndRun, args=(command,)).start()


def RunCommandsAsync(commands):
    p = multiprocessing.Pool(int(GetConfig("SystemConfig")["Async"]["threadPoolSize"]))
    p.map(EnqueueAndRun, commands)


