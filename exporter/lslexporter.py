import json
from exporter import Exporter
import pytz
from unidecode import unidecode

class LslExporter(Exporter):
    def __str__(self):
        lslevents = ""

        nevents = 0

        tz_slt = pytz.timezone("US/Pacific")

        for event in self.events:
            if len(event.title)!=0 and len(event.hgurl)!=0:
                start = tz_slt.normalize(event.start.astimezone(tz_slt))

                title = event.title
                title = title.replace("\n", " ")
                title = title.replace("\r", " ")
                title = unidecode(title.encode('utf-8'))
                # title = title.encode('ascii', 'ignore').decode('ascii')

                lslevents.append(title)
                lslevents.append(start.strftime("%I:%M%p"))
                lslevents.append(event.hgurl.encode('utf-8'))

                nevents += 1

            if nevents==14:
                break

        return "\n".join(lslevents)
