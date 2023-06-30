import re
import pickle
from datetime import timedelta
from helper import Helper

class SnikyHelper(Helper):
    hgre = re.compile("^[^:]+:[0-9]+:[^:]+$")

    def customizeEvent(self, event):
        if event.hgurl is None or len(event.hgurl) is 0:
            return None

        event = super(SnikyHelper, self).customizeEvent(event)

        event.hgurl = event.hgurl.replace('http://', '')

        return event

