import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from lib.webcache import WebCache
from helper.kalasiddhi import KalasiddhiHelper

class KalasiddhiFetcher(IcalFetcher):
    def __init__(self,webcache=None):
        super(KalasiddhiFetcher,self).__init__("https://calendar.google.com/calendar/ical/kalasiddhigrid@gmail.com/public/basic.ics", [Category("grid-kalasiddhi")], webcache, KalasiddhiHelper())
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    cache = WebCache("data/test_kalasiddhi.cache")

    f = KalasiddhiFetcher(cache)

    e = f.fetch()

    cache.flush()

    for ev in e:
        print str(ev)
