import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from fetcher.icalfetcher import IcalFetcher
from helper.helper import Helper
from datetime import timedelta

class ArcanaFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(ArcanaFetcher,self).__init__(
            "http://www.brownbearsw.com/cal/Events.Calendar?Op=iCalSubscribe",
            [ Category("grid-arcana") ],
            eventlist,
            webcache, 
            Helper()
        )
        self.webcache = webcache
        self.minexpiry = 3000
        self.maxexpiry = 5000

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache('data/test_arcana.pck')

    f = ArcanaFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
