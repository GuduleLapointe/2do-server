import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.oscc15 import OSCC15Helper

class OSCC15Fetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(OSCC15Fetcher,self).__init__(
            "http://opensimulatorcommunity20151914.sched.org/all.ics",
            [Category("grid-oscc15")],
            eventlist,
            webcache,
            OSCC15Helper()
        )
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_oscc15.cache")

    f = OSCC15Fetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
