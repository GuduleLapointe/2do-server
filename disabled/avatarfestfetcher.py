import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.avatarfest import AvatarFestHelper

class AvatarFestFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(AvatarFestFetcher,self).__init__(
            "https://calendar.google.com/calendar/ical/9g0idps421vmlfukadao93tiu8%40group.calendar.google.com/public/basic.ics",
            [ Category("fair"), Category("grid-avatarfest") ],
            eventlist,
            webcache,
            AvatarFestHelper()
        )
        self.minexpiry = 1000
        self.maxexpiry = 1800

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    webcache = WebCache('data/test_avatarfest.pck')

    f = AvatarFestFetcher(eventlist, webcache)

    f.fetch()

    webcache.flush()

    for ev in eventlist:
        print str(ev)
