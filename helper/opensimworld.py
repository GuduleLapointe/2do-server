import re
import pickle
from datetime import timedelta
from helper import Helper

class OpensimworldHelper(Helper):
    hgre = re.compile("^[^:]+:[0-9]+:[^:]+$")

    def findRegion(self, data):
        if data==None:
            return None
        if re.search("marina bay", data, flags=re.I):
            return "login.greatcanadiangrid.ca:8002:Marina Bay"
        if re.search("Hot Rod 50s Diner", data, flags=re.I):
            return "login.greatcanadiangrid.ca:8002:Dreamland"
        return None

    def customizeEvent(self, event):
        event = super(OpensimworldHelper, self).customizeEvent(event)

        hgurl = self.findRegion(event.hgurl)

        if hgurl != None:
            event.hgurl = hgurl

        return event

