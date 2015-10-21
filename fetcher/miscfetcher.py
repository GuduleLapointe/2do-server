import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category

class MiscFetcher(IcalFetcher):
    def __init__(self,webcache=None):
        super(MiscFetcher,self).__init__("https://www.google.com/calendar/ical/rtq0u6gmq6lcrrqpjnub2b3q8k%40group.calendar.google.com/public/basic.ics", [], webcache);
        self.webcache = webcache

if __name__=='__main__':
    f = MiscFetcher()

    e = f.fetch()

    for ev in e:
        print str(ev)
