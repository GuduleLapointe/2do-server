import requests
from lib.event import Event
import icalendar
import pytz
import datetime
from fetcher.icalfetcher import IcalFetcher

class IcalHelpedFetcher(IcalFetcher):
    tz_pacific = pytz.timezone('US/Pacific')

    def __init__(self,url=None,categories=None,helper=None):
        if url!=None:
            self.url = url
        self.categories = categories
        self.helper = helper

if __name__=='__main__':
    f = IcalHelpedFetcher("https://www.google.com/calendar/ical/857iq9v0nfqrg3qmt4e00n53rc%40group.calendar.google.com/public/basic.ics")

    e = f.fetch()

    for ev in e:
        print str(ev)
