import json
from exporter import Exporter
import pytz

class LslExporter(Exporter):
    def __str__(self):
        lslevents = ""

        nevents = 0

        for event in self.events:
            lslevents += event.title.encode('utf-8') + "\n"
            lslevents += event.start.astimezone(pytz.utc).strftime("%s") + "\n"
            lslevents += event.hgurl.encode('utf-8') + "\n"

            nevents = nevents + 1

            if nevents==10:
                break
            
        return lslevents
