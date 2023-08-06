#!/usr/bin/python3
from serviceengine.System.Configurations.SystemConfig import SystemConfig
import json


def GetConfig(name="SystemConfig"):
    return json.loads(json.dumps(SystemConfig))
