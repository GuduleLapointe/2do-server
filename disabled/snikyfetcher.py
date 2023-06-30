import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.sniky import SnikyHelper

class SnikyFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(SnikyFetcher,self).__init__(
            "https://calendar.google.com/calendar/ical/9g7m9bi8mjhgqclu15fbsta9gk%40group.calendar.google.com/public/basic.ics",
            [Category("grid-sniky")],
            eventlist,
            webcache,
            SnikyHelper()
        )
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_sniky.cache")

    f = SnikyFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)

