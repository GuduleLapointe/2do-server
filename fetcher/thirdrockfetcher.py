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


class ThirdRockFetcher:
    eventurl="http://3rdrockgrid.com/new/wp-content/plugins/dwg-calendar/getevents.php"
    tz_pacific = pytz.timezone('US/Pacific')

    def __init__(self,webcache):
        self.webcache = webcache

    def fetch(self, limit=0):
        print "ThirdRockFetcher: fetch overview.."

        rv = []

        r = requests.get(self.eventurl)

        if r.status_code==200:
            nevents = len(r.json())
            if limit>0 and limit<nevents:
                nevents = limit

            ievent = 0
            print "ThirdRockFetcher: fetching "+str(nevents)+" events"
            print "ThirdRockFetcher: [0/"+str(nevents)+"]    ",
            sys.stdout.flush()
            for event in r.json():
                print "\rThirdRockFetcher: ["+str(ievent+1)+"/"+str(nevents)+"]        ",
                sys.stdout.flush()
                ievent = ievent + 1

                e = ThirdRockEvent(self.webcache)
                e.title = event['title']

                t_start = self.tz_pacific.localize(parser.parse(event['start']))
                t_end = self.tz_pacific.localize(parser.parse(event['end']))

                e.start = t_start
                e.end = t_end

                e.id = event['id']

                e.fetch()

                rv = rv + [e]

                if limit>0 and ievent>=limit:
                    break

        print ""

        return rv



if __name__=='__main__':
    webcache = WebCache("data/test_thirdrock.cache")

    f = ThirdRockFetcher(webcache)

    e = f.fetch(12)

    webcache.flush()

    for event in e:
        print str(event)
