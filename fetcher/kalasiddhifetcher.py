import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from lib.webcache import WebCache
from helper.helper import Helper

class KalasiddhiFetcher(IcalFetcher):
    def __init__(self,webcache=None):
        super(KalasiddhiFetcher,self).__init__("https://www.google.com/calendar/ical/kalasiddhigrid%40group.calendar.google.com/public/basic.ics", [Category("grid-kalasiddhi")], webcache, Helper())
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
