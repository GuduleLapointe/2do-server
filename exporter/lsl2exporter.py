import json
from exporter import Exporter
import pytz
import datetime
from unidecode import unidecode

class Lsl2Exporter(Exporter):
    def __str__(self):
        lslevents = "1.4.0 Recommended update\n"

        nevents = 0

        tz_slt = pytz.timezone("US/Pacific")

        epoch = datetime.datetime.utcfromtimestamp(0)
        epoch = epoch.replace(tzinfo=pytz.UTC)

        for event in self.events:
            if len(event.title)!=0 and len(event.hgurl)!=0:
                start = tz_slt.normalize(event.start.astimezone(tz_slt))
                end = tz_slt.normalize(event.end.astimezone(tz_slt))

                utc_start = pytz.utc.normalize(event.start.astimezone(pytz.utc))
                ts_start = (utc_start-epoch).total_seconds()

                utc_end = pytz.utc.normalize(event.end.astimezone(pytz.utc))
                ts_end = (utc_end-epoch).total_seconds()

                title = event.title
                title = title.replace("\n", " ")
                title = title.replace("\r", " ")
                title = unidecode(title.encode('utf-8'))
                # title = title.encode('ascii', 'ignore').decode('ascii')

                lslevents.append(title)
                lslevents.append(start.strftime("%I:%M%p~%Y-%m-%d~") + str(int(round(ts_start))))
                lslevents.append(end.strftime("%I:%M%p~%Y-%m-%d~") + str(int(round(ts_end))))
                lslevents.append(event.hgurl.encode('utf-8'))

                nevents += 1

            if nevents==25:
                break

        return "\n".join(lslevents)
