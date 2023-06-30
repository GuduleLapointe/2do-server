import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.zangrid import ZanGridHelper

class ZanGridFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(ZanGridFetcher,self).__init__(
            "https://calendar.google.com/calendar/ical/zangrid2015%40gmail.com/public/basic.ics",
            [Category("grid-zangrid")],
            eventlist,
            webcache,
            ZanGridHelper()
        )
        self.webcache = webcache
        self.minexpiry = 600
        self.maxexpirty = 1000

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_zangrid.cache")

    f = ZanGridFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
