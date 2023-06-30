import re
import pickle
from datetime import timedelta
from helper import Helper

class ThirdLifeHelper(Helper):
    hgre = re.compile("^[^:]+:[0-9]+:[^:]+$")

    def findRegion(self, data):
        if data==None or data=='' or data=='-':
            return '3rdlifegrid.com:8002:'
        return None

    def customizeEvent(self, event):
        event = super(ThirdLifeHelper, self).customizeEvent(event)

        hgurl = self.findRegion(event.hgurl)

        if hgurl != None:
            event.hgurl = hgurl

        if event.hgurl is not None and self.hgre.search(event.hgurl) is None:
            event.hgurl = None
        
        return event

