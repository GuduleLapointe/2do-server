import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.nextlife import NextLifeHelper

class NextLifeFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(NextLifeFetcher,self).__init__(
            "https://calendar.google.com/calendar/ical/atdiamant%40web.de/public/basic.ics",
            [],
            eventlist,
            webcache,
            NextLifeHelper()
        )
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_nextlife.cache")

    f = NextLifeFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
