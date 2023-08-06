#!/usr/bin/python3
from serviceengine.PublicFunctions.CommandInterface.ICommand import ICommand
from serviceengine.System.Language.SystemLanguage import SLI


class RunScript(ICommand):
    def Execute_Windows(self):
        self.RunScriptFile()

    def Execute_Linux(self):
        self.RunScriptFile()

    def RunScriptFile(self):
        scriptPath = self.request[0]
        sli = SLI(self.context)
        sli.RunScript(scriptPath)


RunScript.PublicFacing = "run"
RunScript.MinRequestParameters = 1
RunScript.Help = "Runs a series of commands\n" \
                       "Run  [script file path]\n" \
                       "Runs the files commands line by line - each command needs to be separated by line down.\n" \
                       "Can be called recursively."
RunScript.ShortHelp = "Runs a script file"
