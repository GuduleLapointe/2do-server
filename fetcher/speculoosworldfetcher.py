import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.speculoosworld import SpeculoosWorldHelper

class SpeculoosWorldFetcher(IcalFetcher):
    def __init__(self,eventlist,webcache=None):
        super(SpeculoosWorldFetcher,self).__init__(
            "https://speculoos.world/en/events/?ical=1",
            [Category("grid-speculoosworld")],
            eventlist,
            webcache,
            SpeculoosWorldHelper()
        )
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_speculoosworld.cache")

    f = SpeculoosWorldFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
