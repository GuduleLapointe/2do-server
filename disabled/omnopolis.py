import re
import pickle
from datetime import timedelta
from helper import Helper

class OmnopolisHelper(Helper):
    hgre = re.compile("^[^:]+:[0-9]+:[^:]+$")

    def findRegion(self, data):
        if data==None or data=='' or data=='-':
            return 'omnopolis.com:8002'
        return None

    def customizeEvent(self, event):
        event = super(OmnopolisHelper, self).customizeEvent(event)

        hgurl = self.findRegion(event.hgurl)

        if hgurl != None:
            event.hgurl = hgurl

        return event
