import re
import pickle
from datetime import timedelta
from helper import Helper

class TheFactoryHelper(Helper):
    hgre = re.compile("^[^:]+:[0-9]+:[^:]+$")

    def findRegion(self, data):
        if data==None or data=='' or data=='-':
            return 'hg.osgrid.org:80:The Factory'
        return None

    def customizeEvent(self, event):
        event = super(TheFactoryHelper, self).customizeEvent(event)

        hgurl = self.findRegion(event.hgurl)

        if hgurl != None:
            event.hgurl = hgurl

        return event
