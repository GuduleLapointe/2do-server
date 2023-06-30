import re
import pickle
from datetime import timedelta
from helper import Helper

class FrancoGridHelper(Helper):
    hgre = re.compile("^[^:]+:[0-9]+:[^:]+$")

    def findRegion(self, data):
        if data=='None' or data=='-' or data==' ':
            return 'francogrid.org:8002:'
        return None

    def customizeEvent(self, event):
        event = super(FrancoGridHelper, self).customizeEvent(event)

        hgurl = self.findRegion(event.hgurl)
        if hgurl!=None:
            event.hgurl = hgurl

        return event

