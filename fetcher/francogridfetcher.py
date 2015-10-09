import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar

class FrancoGridFetcher(IcalFetcher):
    def __init__(self):
        super(FrancoGridFetcher,self).__init__("http://francogrid.org/evenements/ical")

    def fetch(self, limit=0):
        events = super(FrancoGridFetcher,self).fetch(limit)

        for e in events:
            e.grid='FrancoGrid'

        return events

if __name__=='__main__':
    f = FrancoGridFetcher()

    e = f.fetch()

    for ev in e:
        print str(ev)
