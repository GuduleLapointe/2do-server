import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.omnopolis import OmnopolisHelper

class OmnopolisFetcher(IcalFetcher):
    def __init__(self,eventlist,webcache=None):
        super(OmnopolisFetcher,self).__init__(
            "https://calendar.google.com/calendar/ical/a35f7429de4c6d1ac940e73c48d4267c40c677e4543d38898d20e8e73b699b2f%40group.calendar.google.com/public/basic.ics",
            [Category("grid-omnopolis")],
            eventlist,
            webcache,
            OmnopolisHelper()
        )
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_omnopolis.cache")

    f = OmnopolisFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
