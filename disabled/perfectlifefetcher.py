import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category

from helper import Helper
import re
# import pickle
# from datetime import timedelta

class PerfectLifeFetcher(IcalFetcher):
    def __init__(self,eventlist,webcache=None):
        super(PerfectLifeFetcher,self).__init__(
            "https://calendar.google.com/calendar/ical/i3aadh9g4kds7tsissgo81rg1k%40group.calendar.google.com/public/basic.ics",
            [Category("grid-perfectlife")],
            eventlist,
            webcache,
            PerfectLifeHelper()
        )
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_perfectlife.cache")

    f = PerfectLifeFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)

class PerfectLifeHelper(Helper):
    hgre = re.compile("^[^:]+:[0-9]+:[^:]+$")

    def findRegion(self, data):
        if data == None or data == '' or data == '-':
            region = 'grid.perfect-life.ca:8002'
        else:
            region = None

        print("Data:", data)  # Debug output

        return region

    def customizeEvent(self, event):
        event = super(PerfectLifeHelper, self).customizeEvent(event)

        hgurl = self.findRegion(event.hgurl)
        if hgurl != None:
            hgurl = re.sub(r'^.*:\/\/', '', hgurl)
            event.hgurl = hgurl

        return event
