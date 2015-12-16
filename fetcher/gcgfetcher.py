import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from fetcher.icalfetcher import IcalFetcher
from helper.gcg import GcgHelper
from datetime import timedelta

class GcgFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(GcgFetcher,self).__init__(
            "http://www.brownbearsw.com/cal/gcgevents?Op=iCalSubscribe",
            [ Category("grid-gcg") ],
            eventlist,
            webcache, 
            GcgHelper()
        )
        self.webcache = webcache
        self.minexpiry = 3000
        self.maxexpiry = 5000

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache('data/test_gcgfetcher.pck')

    f = GcgFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
