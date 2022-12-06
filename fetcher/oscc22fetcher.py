import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.oscc22 import OSCC22Helper

class OSCC22Fetcher(IcalFetcher):
    def __init__(self,eventlist,webcache=None):
        super(OSCC22Fetcher,self).__init__(
            "https://conference.opensimulator.org/?mec-ical-feed=1",
            [Category("grid-oscc22")],
            eventlist,
            webcache,
            OSCC22Helper()
        )
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_oscc22.cache")

    f = OSCC22Fetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
