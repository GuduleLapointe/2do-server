import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from lib.webcache import WebCache
from helper.zangrid import ZanGridHelper

class ZanGridFetcher(IcalFetcher):
    def __init__(self,webcache=None):
        super(ZanGridFetcher,self).__init__("https://calendar.google.com/calendar/ical/zangrid2015%40gmail.com/public/basic.ics", [Category("grid-zangrid")], webcache, ZanGridHelper())
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    cache = WebCache("data/test_zangrid.cache")

    f = ZanGridFetcher(cache)

    e = f.fetch()

    cache.flush()

    for ev in e:
        print str(ev)
