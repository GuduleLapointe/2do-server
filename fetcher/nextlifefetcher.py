import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from lib.webcache import WebCache
from helper.nextlife import NextLifeHelper

class NextLifeFetcher(IcalFetcher):
    def __init__(self,webcache=None):
        super(NextLifeFetcher,self).__init__("https://calendar.google.com/calendar/ical/atdiamant%40web.de/public/basic.ics", [], webcache, NextLifeHelper())
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    cache = WebCache("data/test_nextlife.cache")

    f = NextLifeFetcher(cache)

    e = f.fetch()

    cache.flush()

    for ev in e:
        print str(ev)
