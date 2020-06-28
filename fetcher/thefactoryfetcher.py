import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.thefactory import TheFactoryHelper

class TheFactoryFetcher(IcalFetcher):
    def __init__(self,eventlist,webcache=None):
        super(TheFactoryFetcher,self).__init__(
            "https://calendar.google.com/calendar/ical/ernestmoncrieff54%40gmail.com/private-57530a1e03a7fd303d8ef3ff7436cd00/basic.ics",
            [Category("grid-thefactory")],
            eventlist,
            webcache,
            TheFactoryHelper()
        )
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_thefactory.cache")

    f = TheFactoryFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
