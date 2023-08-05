import json
import sys

from testwizard.commands_core.ResultBase import ResultBase

class FindAllPatternLocationsResult(ResultBase):
    def __init__(self, json1, successMessage, failMessage):
        jsonObj = json.loads(json1)
        ResultBase.__init__(self, jsonObj["errorCode"] == 0, successMessage, failMessage)

        self.matches = jsonObj["matches"]
        self.numberOfMatches = jsonObj["numberOfMatches"]

        if(self.success):
            return

        if("errorCode" in jsonObj):
            self.message = self.getMessageForErrorCode(self.message, jsonObj["errorCode"])