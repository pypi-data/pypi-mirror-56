#!/usr/bin/python3
import multiprocessing
from multiprocessing import Process
from System.Configurations.ConfigArchivist import GetConfig
from System.EnqueueAndRun.EnqueueAndRun import EnqueueAndRun


def RunCommandAsync(command):
    Process(target=EnqueueAndRun, args=(command,)).start()


def RunCommandsAsync(commands):
    p = multiprocessing.Pool(int(GetConfig("SystemConfig")["Async"]["threadPoolSize"]))
    p.map(EnqueueAndRun, commands)


