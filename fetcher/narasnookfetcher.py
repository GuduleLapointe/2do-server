import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.narasnook import NarasNookHelper

class NarasNookFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(NarasNookFetcher,self).__init__(
            "https://calendar.google.com/calendar/ical/author.nara.malone@gmail.com/public/basic.ics",
            [],
            eventlist,
            webcache,
            NarasNookHelper()
        )
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_narasnook.cache")

    f = NarasNookFetcher(eventlist, cache)

    e = f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
