import requests
from lib.event import Event
from dateutil import parser
import datetime
from lxml import html
import re
import sys
import pytz
from lib.category import Category
from lib.webcache import WebCache
from helper.craft import CraftHelper

class CraftFetcher:
    eventurl="http://www.craft-world.org/page/en/living-in-craft/events.php"
    tz_rome = pytz.timezone('Europe/Rome')

    def __init__(self,webcache):
        self.webcache = webcache
        self.helper = CraftHelper()

    def fetch(self, limit=0):
        print "CraftFetcher: fetch event page"

        rv = []

        r = requests.get(self.eventurl)

        if r.status_code==200:
            tree = html.fromstring(r.text)

            events = tree.xpath('//td[@class="allevent"]/ul/li')

            for event in events:
                print "\rCraftFetcher: processing event "+str(len(rv)+1),
                sys.stdout.flush()

                datestr = event.text.strip()
                date = parser.parse(datestr)

                e = Event()

                e.title = event.xpath('./a')[0].text

                e.description = event.xpath('./div')[0].text_content()

                e.start = self.tz_rome.localize(date)
                e.end = e.start + datetime.timedelta(days=1)

                region = self.helper.findRegion(e.description)

                if region!=None:
                    e.hgurl = "craft-world.org:8002:"+region

                rv += [e]

            print ""

        return rv



if __name__=='__main__':
    webcache = WebCache("data/test_craft.cache")

    f = CraftFetcher(webcache)

    e = f.fetch(12)

    webcache.flush()

    for event in e:
        print str(event)
