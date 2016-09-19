import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from fetcher.icalfetcher import IcalFetcher
from helper.thirdlife import ThirdLifeHelper
from datetime import timedelta

class ThirdLifeFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(ThirdLifeFetcher,self).__init__(
            "http://www.brownbearsw.com/cal/3rdLifeCalendar?Op=iCalSubscribe",
            [ Category("grid-thirdlife") ],
            eventlist,
            webcache, 
            ThirdLifeHelper()
        )
        self.webcache = webcache
        self.minexpiry = 3000
        self.maxexpiry = 5000

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache('data/test_thirdlifefetcher.pck')

    f = ThirdLifeFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
