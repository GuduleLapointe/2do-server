import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from lib.webcache import WebCache
from helper.lf import LfHelper

class LfGridFetcher(IcalFetcher):
    def __init__(self,webcache=None):
        super(LfGridFetcher,self).__init__("http://www.localendar.com/public/lfgrid?style=X2", [Category("grid-littlefield")], webcache, LfHelper())
        self.webcache = webcache

if __name__=='__main__':
    cache = WebCache("data/test_littlefield.cache")

    f = LfGridFetcher(cache)

    e = f.fetch()

    cache.flush()

    for ev in e:
        print str(ev)
