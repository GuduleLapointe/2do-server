import re
import pickle
from datetime import timedelta
from helper import Helper

class TangleHelper(Helper):
    hgre = re.compile("EXPO", re.I)

    def customizeEvent(self, event):
        if TangleHelper.hgre.search(event.title)==None:
            return None

        event = super(TangleHelper, self).customizeEvent(event)

        if event.hgurl=='' or event.hgurl=='-':
            if TangleHelper.hgre.search(event.title)!=None:
                event.hgurl='tanglegrid.net:8032:EXPO Isle'
            else:
                event.hgrul='tanglegrid.net:8032:Welcome Island'

        return event

