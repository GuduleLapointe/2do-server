import requests
from lib.event import Event
from dateutil import parser
from lxml import html
import re
import sys
import pytz
from lib.category import Category
from lib.webcache import WebCache

class ThirdRockEvent(Event):
    detailurl = "http://3rdrockgrid.com/new/event-details/?id="
    hgre = re.compile(".+:.+:.+")

    def __init__(self, webcache=None):
        super(ThirdRockEvent,self).__init__()
        self.id = None
        self.categories += [ Category("grid-3rdrockgrid") ]
        self.webcache = webcache

    def fetch(self):
        if self.id==None:
            raise Exception("Fetch on unitialized ThirdRockEvent")
        url = self.detailurl + str(self.id)

        if self.webcache==None:
            r = requests.get(url)
        else:
            r = self.webcache.fetch(url)

        if r.status_code==200:
            tree = html.fromstring(r.text)
            self.description = ' '.join(tree.xpath('//div[@class="entry"]/div[5]/text()')).strip()

            region = ' '.join(tree.xpath('//div[@class="entry"]/div[6]/text()')).strip()
            location = ' '.join(tree.xpath('//div[@class="entry"]/div[7]/text()')).strip()

            if self.hgre.match(region):
                self.hgurl = region
            elif self.hgre.match(location):
                self.hgurl = location
            else:
                self.hgurl = region + " " + location

    def __str__(self):
        rv = super(ThirdRockEvent,self).__str__()

        return rv


class CraftFetcher:
    eventurl="http://www.craft-world.org/page/en/living-in-craft/events.php"
    tz_pacific = pytz.timezone('Europe/Rome')

    def __init__(self,webcache):
        self.webcache = webcache

    def fetch(self, limit=0):
        print "CraftFetcher: fetch event page"

        rv = []

        r = requests.get(self.eventurl)

        if r.status_code==200:
            tree = html.fromstring(r.text)

            events = tree.xpath('//td[@class="allevent"]/ul/li')

            for event in events:
                datestr = event.text.strip()
                date = parser.parse(datestr)

                e = Event()

                e.title = event.xpath('./a')[0].text

                e.description = event.xpath('./div')[0].text_content()

                e.start = date

                rv += [e]

        return rv



if __name__=='__main__':
    webcache = WebCache("data/test_craft.cache")

    f = CraftFetcher(webcache)

    e = f.fetch(12)

    webcache.flush()

    for event in e:
        print str(event)
