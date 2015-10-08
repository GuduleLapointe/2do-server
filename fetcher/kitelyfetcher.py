import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar

class KitelyFetcher(IcalFetcher):
    def __init__(self):
        super(KitelyFetcher,self).__init__("https://www.google.com/calendar/ical/857iq9v0nfqrg3qmt4e00n53rc%40group.calendar.google.com/public/basic.ics")

    def fetch(self, limit=0):
        events = super(KitelyFetcher,self).fetch(limit)

        for e in events:
            e.grid='Kitely'

        return events

if __name__=='__main__':
    f = KitelyFetcher()

    e = f.fetch()

    for ev in e:
        print str(ev)
