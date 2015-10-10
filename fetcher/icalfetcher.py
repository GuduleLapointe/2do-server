import requests
from lib.event import Event
import icalendar
import pytz
import datetime

class IcalFetcher(object):
    tz_pacific = pytz.timezone('US/Pacific')

    def __init__(self,url=None):
        if url!=None:
            self.url = url

    def fetch(self, limit=0, tz=pytz.utc):
        print "IcalFetcher: get url "+str(self.url)
        print "IcalFetcher: timezone " + str(tz)

        r = requests.get(self.url)

        events = []

        if r.status_code==200:
            cal = icalendar.Calendar.from_ical(r.text)
            cal_events = cal.walk(name="VEVENT")

            for event in cal_events:
                e = Event()
                e.title = event['SUMMARY'].title()
                e.description = event['DESCRIPTION'].title()


                e.start = event['DTSTART'].dt
                e.end = event['DTEND'].dt

                if type(e.start)==datetime.date:
                    e.start = datetime.datetime.combine(e.start, datetime.time())

                if type(e.end)==datetime.date:
                    e.end = datetime.datetime.combine(e.end, datetime.time())

                if e.start.tzinfo==None or e.start.tzinfo.utcoffset(e.start)==None:
                    print "start time is naive"
                    e.start = self.tz_pacific.localize(e.start)

                if e.end.tzinfo==None or e.end.tzinfo.utcoffset(e.end)==None:
                    print "end time is naive"
                    e.end = self.tz_pacific.localize(e.end)

                try:
                    e.hgurl = event['LOCATION'].title()
                except KeyError:
                    pass

                events = events + [e]

                if limit>0 and len(events)>=limit:
                    break

        return events

if __name__=='__main__':
    f = IcalFetcher("https://www.google.com/calendar/ical/857iq9v0nfqrg3qmt4e00n53rc%40group.calendar.google.com/public/basic.ics")

    e = f.fetch()

    for ev in e:
        print str(ev)
