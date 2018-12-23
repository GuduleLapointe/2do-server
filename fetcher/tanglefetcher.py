import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.tangle import TangleHelper

class TangleFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(TangleFetcher,self).__init__(
            "https://calendar.google.com/calendar/ical/lesliespiritweaver%40gmail.com/public/basic.ics",
            [Category("grid-tangle")],
            eventlist,
            webcache,
            TangleHelper()
        )
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_tangle.cache")

    f = TangleFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
