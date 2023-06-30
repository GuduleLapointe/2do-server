import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.francogrid import FrancoGridHelper

class FrancoGridFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(FrancoGridFetcher,self).__init__(
            "http://francogrid.org/evenements/ical",
            [ Category("grid-francogrid") ],
            eventlist,
            webcache,
            FrancoGridHelper()
        )
        self.webcache = webcache

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache('data/test_francogridfetcher.pck')

    f = FrancoGridFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
