import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.francogrid import FrancoGridHelper
from lib.webcache import WebCache

class FrancoGridFetcher(IcalFetcher):
    def __init__(self,webcache=None):
        super(FrancoGridFetcher,self).__init__("http://francogrid.org/evenements/ical",[ Category("grid-francogrid") ],webcache, FrancoGridHelper())
        self.webcache = webcache

if __name__=='__main__':
    cache = WebCache('data/test_francogridfetcher.pck')

    f = FrancoGridFetcher(cache)

    e = f.fetch()

    cache.flush()

    for ev in e:
        print str(ev)
