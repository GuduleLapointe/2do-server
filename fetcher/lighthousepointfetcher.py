import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from lib.webcache import WebCache
from helper.helper import Helper

class LightHousePointFetcher(IcalFetcher):
    def __init__(self,webcache=None):
        super(LightHousePointFetcher,self).__init__("http://lighthousepoint.co.uk/?plugin=all-in-one-event-calendar&controller=ai1ec_exporter_controller&action=export_events&no_html=true", [Category("grid-lhp")], webcache, Helper())
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    cache = WebCache("data/test_lhp.cache")

    f = LightHousePointFetcher(cache)

    e = f.fetch()

    cache.flush()

    for ev in e:
        print str(ev)
