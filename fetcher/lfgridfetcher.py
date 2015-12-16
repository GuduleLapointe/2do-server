import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.lf import LfHelper

class LfGridFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(LfGridFetcher,self).__init__(
            "http://www.localendar.com/public/lfgrid?style=X2",
            [Category("grid-littlefield")],
            eventlist,
            webcache,
            LfHelper()
        )
        self.webcache = webcache

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_littlefield.cache")

    f = LfGridFetcher(eventlist, cache)

    e = f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
