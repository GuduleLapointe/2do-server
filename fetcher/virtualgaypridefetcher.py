import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.virtualgaypride import VirtualGayPrideHelper

class VirtualGayPrideFetcher(IcalFetcher):
    def __init__(self,eventlist,webcache=None):
        super(VirtualGayPrideFetcher,self).__init__(
            "https://calendar.google.com/calendar/ical/virtualgaypride%40gmail.com/public/basic.ics",
            [Category("grid-virtualgaypride")],
            eventlist,
            webcache,
            VirtualGayPrideHelper()
        )
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_virtualgaypride.cache")

    f = VirtualGayPrideFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
