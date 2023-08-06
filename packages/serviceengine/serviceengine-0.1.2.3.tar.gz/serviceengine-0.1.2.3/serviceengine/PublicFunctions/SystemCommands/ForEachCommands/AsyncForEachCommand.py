#!/usr/bin/python3
from serviceengine.PublicFunctions.CommandInterface.ICommand import ICommand
from serviceengine.PublicFunctions.SystemCommands.ForEachCommands.ForEachLogic import ForEachLogic
from serviceengine.System.MultiProcessing.MultiProcessing import RunCommandsAsync


class AsyncForEachCommand(ICommand):
    def Execute_Windows(self):
        self.PopulateAsyncForEachCommands()

    def Execute_Linux(self):
        self.PopulateAsyncForEachCommands()

    def PopulateAsyncForEachCommands(self):
        newCommands = ForEachLogic().GetNewCommands(self.request)
        RunCommandsAsync(newCommands)


AsyncForEachCommand.PublicFacing = "aforeach"
AsyncForEachCommand.MinRequestParameters = 1
AsyncForEachCommand.Help = "Replaces any parameters wrapped in a special syntax indicating a path or list to a list.\n"\
                      "A list of new commands will be created from all possible replacements and these commands " \
                      "will be activated concurrently via a thread pool.\n" \
                      "Any number of substitutions can be inserted in a single foreach function, all combinations" \
                      "will be created.\n" \
                      "i.e.:\n" \
                      "\t\tforeach some text sub[\"path or list\"] additional text sub[\"path2 or list\"]\n" \
                      "\t\tIn this case the application will dynamically detect if the content of sub[\"xxx\"] " \
                           "(as shown: xxx) is a list of items, a path to a local file or a path to a remote url." \
                           "\n\t\tIf its a path to a file the file must contain only elements of the list either" \
                           " separated by line breaks " \
                      "or commas orboth. " \
                           "\n\t\tThe application will then create new commands for all combinations of the " \
                      "first and second sub parameters and runs all the commands via a process pool so they activate " \
                      "concurrently"
AsyncForEachCommand.ShortHelp = "Replaces parameters in a command with all possible combinations and adds the" \
                           "new commands to the event queue - runs like foreach but async"
