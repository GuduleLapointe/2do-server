import requests
from lib.event import Event
from dateutil import parser
from lxml import html
import re
import sys
import pytz
from lib.category import Category

try:
    from helper import Helper
except ImportError:
    try:
        from helper.helper import Helper
    except ImportError:
        raise ImportError("Failed to import Helper from both 'helper' and 'helper.helper' modules")

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
            r = self.webcache.fetch(url,36000,72000)

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

    def __init__(self, eventlist, webcache):
        self.webcache = webcache
        self.eventlist = eventlist
        self.helper = ThirdRockHelper()

    def fetch(self, limit=0):
        print "ThirdRockFetcher: fetch overview.."

        r = self.webcache.fetch(self.eventurl,300,600)

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

                e = self.helper.customizeEvent(e)

                if e!=None:
                    self.eventlist.add(e)

                if limit>0 and ievent>=limit:
                    break
            print ""

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    webcache = WebCache("data/test_thirdrock.cache")

    f = ThirdRockFetcher(eventlist, webcache)

    f.fetch()

    webcache.flush()

    for event in eventlist:
        print str(event)

class ThirdRockHelper(Helper):
    dictionary = {
        re.compile('Enerdhil', flags=re.I)              : 'grid.3rdrockgrid.com:8002:Enerdhil',
        re.compile('ROB\'s Rock Island', flags=re.I)    : 'grid.3rdrockgrid.com:8002:ROBs Rock Island',
        re.compile('ROBs Rock Island', flags=re.I)      : 'grid.3rdrockgrid.com:8002:ROBs Rock Island',
        re.compile('Eldoland 1', flags=re.I)            : 'grid.3rdrockgrid.com:8002:Eldoland 1',
        re.compile('ROB\'s One World', flags=re.I)      : 'grid.3rdrockgrid.com:8002:ROBs Rock Island',
        re.compile('Roll Over Beethovens', flags=re.I)  : 'grid.3rdrockgrid.com:8002:ROBs Rock Island',
        re.compile('Peapodyne', flags=re.I)             : 'grid.3rdrockgrid.com:8002:Peapodyne',
        re.compile('UF Starfleet Astraios', re.I)       : 'grid.3rdrockgrid.com:8002:Starfleet Astraios',
    }

    hgexp = re.compile('([^:]+:[0-9]+:([^:/]*)?).*?$')
    hgexp2 = re.compile('([^:]+:[0-9]+)/(([^:/]*)?).*?$')

    def customizeEvent(self, event):
        # event has moved, but calendar not updated (yet?)
        if event.title=='Starfleet Boogie-Majel':
            return None

        event = super(ThirdRockHelper, self).customizeEvent(event)

        if event.title == 'UF Starfleet Astraios Mission':
            event.hgurl = 'grid.3rdrockgrid.com:8002:Starfleet Astraios'
        elif event.hgurl != None:
            hgurl = None
            for exp in ThirdRockHelper.dictionary:
                if exp.search(event.hgurl)!=None:
                    hgurl = ThirdRockHelper.dictionary[exp]
            if hgurl!=None:
            	event.hgurl = hgurl

        if event.hgurl!=None:
            m = ThirdRockHelper.hgexp.search(event.hgurl)
            if m!=None:
                event.hgurl = m.group(1)
                return event
            m = ThirdRockHelper.hgexp2.search(event.hgurl)
            if m!=None:
                event.hgurl = m.group(1) + ":" + m.group(2)
                return event

        event.hgurl = None

        return event


if __name__=='__main__':
    pass
