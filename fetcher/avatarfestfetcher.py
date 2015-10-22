import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.avatarfest import AvatarFestHelper
from lib.webcache import WebCache

class AvatarFestFetcher(IcalFetcher):
    def __init__(self,webcache=None):
        super(AvatarFestFetcher,self).__init__(
            "https://www.google.com/calendar/ical/7qk2kkudtb4m864ljdmtsg308c%40group.calendar.google.com/public/basic.ics",
            [ Category("festival"), Category("grid-avatarfest") ],
            webcache,
            AvatarFestHelper()
        )
        self.minexpiry = 1000
        self.maxexpiry = 1800

if __name__=='__main__':
    webcache = WebCache('data/test_avatarfest.pck')

    f = AvatarFestFetcher(webcache)

    e = f.fetch()

    webcache.flush()

    for ev in e:
        print str(ev)
