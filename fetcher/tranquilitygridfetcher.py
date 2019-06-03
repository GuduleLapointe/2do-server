import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.tranquilitygrid import TranquilityGridHelper

class TranquilityGridFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(TranquilityGridFetcher,self).__init__(
            "https://ics.teamup.com/feed/kssj1utsskdmsaa4uz/0.ics",
            [Category("grid-tranquility")],
            eventlist,
            webcache,
            TranquilityGridHelper()
        )
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_tranquilitygrid.cache")

    f = TranquilityGridFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
