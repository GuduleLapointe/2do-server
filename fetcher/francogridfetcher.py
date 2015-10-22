import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.helper import Helper

class FrancoGridFetcher(IcalFetcher):
    def __init__(self,webcache=None):
        super(FrancoGridFetcher,self).__init__("http://francogrid.org/evenements/ical",[ Category("grid-francogrid") ],webcache, Helper())
        self.webcache = webcache

if __name__=='__main__':
    f = FrancoGridFetcher()

    e = f.fetch()

    for ev in e:
        print str(ev)
