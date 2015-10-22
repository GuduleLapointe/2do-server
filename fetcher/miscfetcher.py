import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from lib.webcache import WebCache
from helper.helper import Helper

class MiscFetcher(IcalFetcher):
    def __init__(self,webcache=None):
        super(MiscFetcher,self).__init__("https://www.google.com/calendar/ical/rtq0u6gmq6lcrrqpjnub2b3q8k%40group.calendar.google.com/public/basic.ics", [], webcache, Helper());
        self.webcache = webcache

if __name__=='__main__':
    cache = WebCache('data/test_miscfetcher.pck')

    f = MiscFetcher(cache)

    e = f.fetch()

    cache.flush()

    for ev in e:
        print str(ev)
