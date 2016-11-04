import re
from helper import Helper

class IslandOasisHelper(Helper):
    hgre = re.compile("^[^:]+:[0-9]+:[^:]+$")

    titlere = re.compile('^[a-zA-Z]*\s*[0-9]+[apAP]m\s+(.*)$', flags=re.I)

    hgexpr = {
    }

    def customizeEvent(self, event):
        event = super(IslandOasisHelper, self).customizeEvent(event)

        match = IslandOasisHelper.titlere.search(event.title)
        if match is not None:
            event.title = match.group(1)

        return event
