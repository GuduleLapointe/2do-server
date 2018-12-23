import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.helper import Helper

class InfiniteMetaverseAllianceFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        url="https://calendar.google.com/calendar/ical/2e73vfmkgbi7op4o7j9aplt4rk%40import.calendar.google.com/public/basic.ics"
        super(InfiniteMetaverseAllianceFetcher,self).__init__(
            url,
            [Category("grid-ima")],
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

    cache = WebCache("data/test_ima.cache")

    f = InfiniteMetaverseAllianceFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
