import re
import pickle
from datetime import timedelta
from helper import Helper

class OpensimworldHelper(Helper):
    hgre = re.compile("^[^:]+:[0-9]+:[^:]+$")

    hgexp = {
        re.compile("marina bay", flags=re.I)        : "login.greatcanadiangrid.ca:8002:Marina Bay",
        re.compile("Hot Rod 50s Diner", flags=re.I) : "login.greatcanadiangrid.ca:8002:Dreamland",
        re.compile("Cajun Country", flags=re.I)     : "login.greatcanadiangrid.ca:8002:Dreamland",
    }

    blacklist = [
        re.compile("zangrid.ch", flags=re.I),
    ]

    def findRegion(self, data):
        if data==None:
            return None
        for exp in OpensimworldHelper.hgexp:
            if exp.search(data):
                return OpensimworldHelper.hgexp[exp]
        return None

    def customizeEvent(self, event):
        event = super(OpensimworldHelper, self).customizeEvent(event)

        hgurl = self.findRegion(event.hgurl)

        if hgurl != None:
            event.hgurl = hgurl

        for exp in OpensimworldHelper.blacklist:
            if exp.search(event.hgurl):
                return None

        return event

