#!/usr/bin/python3
from serviceengine.PublicFunctions.CommandInterface.ICommand import ICommand
import time
import re
from serviceengine.System.Regex.Regex import timeRegex

TimeConversionsFromSeconds = {
    "s": 1,
    "m": 60,
    "h": 3600,
    "d": 86400
}


class WaitCommand(ICommand):
    def Execute_Windows(self):
        self.Wait()

    def Execute_Linux(self):
        self.Wait()

    def Wait(self):
        timeParam = self.request[0]
        if not re.match(timeRegex, timeParam):
            self.context.Logger.ERROR(f"Parameter passed '{timeParam}' not valid")
            return
        waitTimeRequested = timeParam[:-1]
        waitTimeType = timeParam[-1:]
        try:
            WaitTime = float(waitTimeRequested) * TimeConversionsFromSeconds[waitTimeType]
        except ValueError:
            self.context.Logger.ERROR("The Wait time entered is not a valid number")
            return
        time.sleep(WaitTime)


WaitCommand.PublicFacing = "wait"
WaitCommand.MinRequestParameters = 1
WaitCommand.Help = "Waits for an amount of time\n" \
                   "wait [time and timeType]\n" \
                   "time and timeType- an integer followed be a single character indicating the length of time that" \
                   "will be waited (there should be no spacing between the integer and the character.\n" \
                   "\t\ts: The integer will be in seconds\n" \
                   "\t\tm: The integer will be in minutes\n" \
                   "\t\th: The integer will be in hours\n" \
                   "\t\td: The integer will be in days\n" \
                   "i.e.:\n" \
                   "\t\twait 100s- will wait for 100 seconds\n" \
                   "\t\twait 2h- will wait for 2 hours\n"
WaitCommand.ShortHelp = "Waits for an amount of time"
