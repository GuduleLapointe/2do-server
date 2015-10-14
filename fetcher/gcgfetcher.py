import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category

class GcgFetcher(IcalFetcher):
    def __init__(self,webcache=None):
        super(GcgFetcher,self).__init__("http://www.brownbearsw.com/cal/gcgevents?Op=iCalSubscribe",[ Category("grid-gcg") ])
        self.webcache = webcache

if __name__=='__main__':
    f = GcgFetcher()

    e = f.fetch()

    for ev in e:
        print str(ev)
