import json
from exporter import Exporter
import pytz
import datetime

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

                lslevents += title.encode('utf-8') + "\n"
                lslevents += start.strftime("%I:%M%p~%Y-%m-%d~") + str(int(round(ts_start))) + "~"
                lslevents += end.strftime("%I:%M%p~%Y-%m-%d~") + str(int(round(ts_end)))

                lslevents += "\n"
                lslevents += event.hgurl.encode('utf-8') + "\n"

                nevents = nevents + 1

            if nevents==25:
                break

        return lslevents
