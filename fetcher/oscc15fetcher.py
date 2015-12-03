import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from lib.webcache import WebCache
from helper.oscc15 import OSCC15Helper

class OSCC15Fetcher(IcalFetcher):
    def __init__(self,webcache=None):
        super(OSCC15Fetcher,self).__init__("http://opensimulatorcommunity20151914.sched.org/all.ics", [Category("grid-oscc15")], webcache, OSCC15Helper())
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    cache = WebCache("data/test_oscc15.cache")

    f = OSCC15Fetcher(cache)

    e = f.fetch()

    cache.flush()

    for ev in e:
        print str(ev)
