import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.kitely import KitelyHelper

class KitelyFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(KitelyFetcher,self).__init__(
            "https://www.google.com/calendar/ical/857iq9v0nfqrg3qmt4e00n53rc%40group.calendar.google.com/public/basic.ics",
            [Category("grid-kitely")],
            eventlist,
            webcache,
            KitelyHelper()
        )
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_kitely.cache")

    f = KitelyFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
