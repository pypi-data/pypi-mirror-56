import sys
import json

from testwizard.commands_core import CommandBase
from .WaitForAudioResult import WaitForAudioResult

class WaitForAudioPeakCommand(CommandBase):
    def __init__(self, session, testObjectName):
        CommandBase.__init__(self, session, testObjectName, "WaitForAudioPeak")
    
    def execute(self, level, timeout):
        if(level == None):
            raise Exception("level is required")
        if(timeout == None):
            raise Exception("timeout is required")

        requestObj = [level, timeout]
        requestObj = json.dumps(requestObj)

        response = self.robot.post(self.url, requestObj, "Could not execute command")

        return WaitForAudioResult(response.read(), "WaitForAudioPeak was successful", "WaitForAudioPeak failed")