import re
import pickle
from datetime import timedelta
from helper import Helper

class SpeculoosWorldHelper(Helper):
    hgre = re.compile("^[^:]+:[0-9]+:[^:]+$")

    def findRegion(self, data):
        if data==None or data=='' or data=='-':
            return 'speculoos.world:8002:Speculoos World'
        return None

    def customizeEvent(self, event):
        event = super(SpeculoosWorldHelper, self).customizeEvent(event)

        hgurl = self.findRegion(event.hgurl)

        if hgurl != None:
            event.hgurl = hgurl

        return event
