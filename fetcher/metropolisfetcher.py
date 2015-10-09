import requests
from lib.event import Event
from dateutil import parser
from lxml import html
import re
import sys
import pytz
import datetime
from lib.category import Category

class MetropolisEvent(Event):
    tz_berlin = pytz.timezone('Europe/Berlin')
    hgexp = re.compile('secondlife://hypergrid.org:8002:([^/]+)/')

    def __init__(self,url=None):
        super(MetropolisEvent,self).__init__()
        self.url=url
        self.grid="Metropolis"

    def fetch(self):
        if self.url == None:
            raise Exception("fetching MetropolisEvent without url set")

        r = requests.get(self.url)

        if r.status_code == 200:
            tree = html.fromstring(r.text)

            self.title = tree.xpath('//h1[@class="entry-title"]')[0].text
            
            content = tree.xpath('//div[@class="entry-content"]')[0].text_content()

            datematch = re.search('Datum: ([0-9]+)\.([0-9]+)\.([0-9]+)', content)
            day = datematch.group(1)
            month = datematch.group(2)
            year = datematch.group(3)
            timestr = re.search('Uhrzeit: ([0-9]+:[0-9]+) Uhr', content).group(1)

            datematch = re.search('Datum: ([0-9]+)\.([0-9]+)\.([0-9]+)', content)

            self.start = self.tz_berlin.localize(parser.parse("%s-%s-%s %s" % (year,month,day,timestr)))
            self.end = self.start + datetime.timedelta(hours=3600)

            langmatch = re.search("Sprache: (.*?)\s*\r", content).group(1)
            self.categories = self.categories + [Category("lang-"+langmatch)]

            cats = tree.xpath('//ul[@class="event-categories"]/li/a')
            for cat in cats:
                # cat.pet()
                self.categories = self.categories + [ Category(cat.text) ]

            urls = tree.xpath('//div[@class="entry-content"]//a/@href')

            for url in urls:
                regionmatch = self.hgexp.match(url)
                if regionmatch != None:
                    self.hgurl="hypergrid.org:8002:" + regionmatch.group(1)
                    break

            self.description = tree.xpath('//div[@class="entry-content"]/font')[0].text_content()

    def __str__(self):
        rv = super(MetropolisEvent,self).__str__()

        return rv


class MetropolisFetcher:
    eventurl="https://events.hypergrid.org/?pno="

    def __init__(self):
        pass

    def fetch(self, limit=0):
        pagecount = 1

        rv = []

        while True:
            print "MetropolisFetcher: fetch overview page " + str(pagecount)

            r = requests.get(self.eventurl+str(pagecount))

            if r.status_code==200:
                tree = html.fromstring(r.text)

                event_urls = tree.xpath('//table[@class="events-table"]//tr//td[2]/font/strong/a/@href')

                nevents = len(event_urls)

                print "MetropolisFetcher: found "+str(nevents)+" events"

                if nevents == 0:
                    break

                ievent = 1

                for event_url in event_urls:
                    print "MetropolisFetcher: fetch event [" + str(ievent) + "/" + str(nevents) + "]\r",
                    sys.stdout.flush()

                    e = MetropolisEvent(event_url)

                    e.fetch()

                    rv = rv + [e]

                    ievent = ievent + 1

                print ""

            pagecount = pagecount + 1

            if limit > 0 and len(rv) > limit:
                break

        return rv



if __name__=='__main__':
    f = MetropolisFetcher()

    e = f.fetch(1)

    for event in e:
        print str(event)
