import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.helper import Helper

# hypevents.net calendar
#

class MiscFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(MiscFetcher,self).__init__(
            "https://www.google.com/calendar/ical/rtq0u6gmq6lcrrqpjnub2b3q8k%40group.calendar.google.com/public/basic.ics",
            [],
            eventlist,
            webcache,
            Helper()
        )
        self.webcache = webcache
        self.minexpiry = 600
        self.maxexpiry = 1000


if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache('data/test_miscfetcher.pck')

    f = MiscFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
