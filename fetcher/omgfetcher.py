import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.helper import Helper

class OneMoreGridFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(OneMoreGridFetcher,self).__init__(
            "https://www.google.com/calendar/ical/8re6r0l486d4fu08s1os96r9o8%40group.calendar.google.com/public/basic.ics",
            [Category("grid-onemoregrid")],
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

    cache = WebCache("data/test_omg.cache")

    f = OneMoreGridFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
