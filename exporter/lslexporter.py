import json
from exporter import Exporter
import pytz
from lib.hgurl import HgUrl

class LslExporter(Exporter):
    def __str__(self):
        lslevents = ""

        nevents = 0

        for event in self.events:
            lslevents += event.title.encode('utf-8') + "\n"
            lslevents += event.start.astimezone(pytz.utc).strftime("%s") + "\n"
            lslevents += HgUrl.normalize(event.hgurl.encode('utf-8')) + "\n"

            nevents = nevents + 1

            if nevents==10:
                break
            
        return lslevents
