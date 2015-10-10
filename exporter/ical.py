from exporter import Exporter
import icalendar
import datetime
import pytz

class IcalExporter(Exporter):

    def __str__(self):
        cal = icalendar.Calendar()

        cal.add('PRODID','-//Linkwater//Aggregator//EN')
        cal.add('VERSION','2.0')

        i=0

        start_after = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=1)
        end_before = start_after + datetime.timedelta(days=365)

        for e in self.events:
            if e.start > start_after and e.end < end_before:
                ie = icalendar.Event()
                ie.add('dtstart', e.start.astimezone(pytz.utc))
                ie.add('dtend', e.end.astimezone(pytz.utc))
                ie.add('dtstamp', pytz.utc.localize(datetime.datetime.utcnow()))
                #ie.add('uid', i)
                ie.add('summary', icalendar.vText(e.title))
                ie.add('description', icalendar.vText(e.description))
                ie.add('location', icalendar.vText(e.hgurl))
                ie.add('categories', ','.join(map(lambda c: c.normalize(),e.categories)))
                ie.add('status',icalendar.vText('confirmed'))

                cal.add_component(ie)

                i=i+1

        return cal.to_ical()

