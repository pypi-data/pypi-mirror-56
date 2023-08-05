import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult

class MultiAction_keyDown(CommandBase):
    def __init__(self, session, testObjectName):
        CommandBase.__init__(self, session, testObjectName, "Selenium.MultiAction_KeyDown")

    def execute(self, key, selector = None):
        if(key==None):
            raise Exception("key is required")

        requestObj = [key]
        if(selector != None):
            requestObj = [selector, key]
        requestObj = json.dumps(requestObj)

        response = self.robot.post(self.url, requestObj, "Could not execute command")

        return OkErrorCodeAndMessageResult(response.read(),"MultiAction_keyDown was successful", "MultiAction_keyDown failed")