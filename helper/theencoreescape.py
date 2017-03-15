import re
from helper import Helper
from datetime import timedelta

class TheEncoreEscapeHelper(Helper):
    cancelled_re = re.compile("cancel", flags=re.I)

    def customizeEvent(self, event):
        event = super(TheEncoreEscapeHelper, self).customizeEvent(event)

        if len(event.title)==0:
            return None

        if self.__class__.cancelled_re.search(event.title):
            return None

        if event.end - event.start > timedelta(hours=6):
            return None
        
        return event
