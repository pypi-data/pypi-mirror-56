import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult

class RunAppInBackgroundCommand(CommandBase):
    def __init__(self, session, testObjectName):
        CommandBase.__init__(self, session, testObjectName, "Mobile.RunAppInBackground")

    def execute(self, seconds = None):
        if(seconds!=None):
            requestObj = [seconds]
        else:
            requestObj = []
        requestObj = json.dumps(requestObj)

        response = self.robot.post(self.url, requestObj, "Could not execute command")

        return SimpleResult(response.read(), "RunAppInBackground was successful", "RunAppInBackground failed")