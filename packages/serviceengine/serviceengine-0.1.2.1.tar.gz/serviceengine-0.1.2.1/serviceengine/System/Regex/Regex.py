#!/usr/bin/python3
import re


subRegex = re.compile(r"sub\[(.+?)\]")
httpRegex = re.compile(r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$")
timeRegex = re.compile("^[1-9]([0-9]*)([s,m,h,d])$")
