import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.helper import Helper

class DiscoveryGridFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(DiscoveryGridFetcher,self).__init__(
            "https://calendar.google.com/calendar/ical/041oe6elmn1n61bb5rk5rn6v1o%40group.calendar.google.com/public/basic.ics",
            [Category("grid-discovery")],
            eventlist,
            webcache,
            Helper()
        )
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_discoverygrid.cache")

    f = DiscoveryGridFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
