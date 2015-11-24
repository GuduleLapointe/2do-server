import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from lib.webcache import WebCache
from helper.exolife import ExoLifeHelper

class ExoLifeFetcher(IcalFetcher):
    def __init__(self,webcache=None):
        super(ExoLifeFetcher,self).__init__("https://www.google.com/calendar/ical/bsogk32qd7813mggecb1tgclmo%40group.calendar.google.com/public/basic.ics", [Category("grid-exolife")], webcache, ExoLifeHelper())
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    cache = WebCache("data/test_exolife.cache")

    f = ExoLifeFetcher(cache)

    e = f.fetch()

    cache.flush()

    for ev in e:
        print str(ev)
