import re
import pickle
from datetime import timedelta
from helper import Helper

class OSCC22Helper(Helper):
    hgre = re.compile("^[^:]+:[0-9]+:[^:]+$")

    def findRegion(self, data):
        return 'cc.opensimulator.org:8002'
        # if data==None or data=='' or data=='-':
        #     return 'cc.opensimulator.org:8002'
        # return None

    def customizeEvent(self, event):
        event = super(OSCC22Helper, self).customizeEvent(event)

        hgurl = self.findRegion(event.hgurl)

        if hgurl != None:
            event.hgurl = hgurl

        event.title = 'OSCC ' + event.title

        return event
