import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from fetcher.icalfetcher import IcalFetcher
from helper.gcg import GcgHelper
from datetime import timedelta

class GcgFetcher(IcalFetcher):
    def __init__(self,webcache=None):
        super(GcgFetcher,self).__init__("http://www.brownbearsw.com/cal/gcgevents?Op=iCalSubscribe",[ Category("grid-gcg") ],webcache)
        self.webcache = webcache
        self.helper = GcgHelper()
        self.minexpiry = 3000
        self.maxexpiry = 5000

if __name__=='__main__':
    f = GcgFetcher()

    e = f.fetch()

    for ev in e:
        print str(ev)
