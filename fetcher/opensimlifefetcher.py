import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.helper import Helper

class OpenSimLifeFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        #url="https://calendar.google.com/calendar/ical/4q1c0qvrlteuja2dgn95qt2gj9r1hgbl%40import.calendar.google.com/public/basic.ics"
        url="http://events.time.ly/oz6nl2n/export?format=ics&no_html=true"
        super(OpenSimLifeFetcher,self).__init__(
            url,
            [Category("grid-opensimlife")],
            eventlist,
            webcache,
            Helper()
        )
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_opensimlife.cache")

    f = OpenSimLifeFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
