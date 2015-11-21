import requests
import re
from lib.event import Event
import icalendar
import pytz
import datetime
from dateutil import rrule
from copy import copy,deepcopy
from lib.rrule import RRULEExpander

class IcalFetcher(object):
    tz_pacific = pytz.timezone('US/Pacific')

    def __init__(self,url=None,categories=None,webcache=None,helper=None):
        self.url = url
        self.categories = categories
        self.helper = helper
        self.cache = webcache
        self.minexpiry = 1800
        self.maxexpiry = 3600

    def customizeEvent(self, event):
        if self.helper!=None:
            return self.helper.customizeEvent(event)
        return event

    def fetch(self, limit=0, tz=pytz.utc):
        print "IcalFetcher: get url "+str(self.url)
        print "IcalFetcher: timezone " + str(tz)

        #r = requests.get(self.url, headers={"user-agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0"})
        r = self.cache.fetch(self.url, self.minexpiry, self.maxexpiry)

        events = []

        if r.status_code==200:
            cal = icalendar.Calendar.from_ical(r.text)
            cal_events = cal.walk(name="VEVENT")

            for event in cal_events:
                e = Event()

                if self.categories!=None:
                    e.categories += self.categories

                e.title = event.get('summary')

                e.description = "No description provided by event organizer."
                if 'DESCRIPTION' in event.keys():
                    e.description = event.get('description')

                e.start = event['DTSTART'].dt

                if 'DTEND' in event.keys():
                    e.end = event['DTEND'].dt
                else:
                    e.end = e.start

                if type(e.start)==datetime.date:
                    e.start = datetime.datetime.combine(e.start, datetime.time())

                if type(e.end)==datetime.date:
                    e.end = datetime.datetime.combine(e.end, datetime.time())

                if e.start.tzinfo==None or e.start.tzinfo.utcoffset(e.start)==None:
                    e.start = self.tz_pacific.localize(e.start)

                if e.end.tzinfo==None or e.end.tzinfo.utcoffset(e.end)==None:
                    e.end = self.tz_pacific.localize(e.end)

                try:
                    e.hgurl = event.get('LOCATION')
                except KeyError:
                    pass

                # TODO: log event w/o location and ignore
                if e.hgurl == None:
                    e.hgurl = "-"

                if not "RRULE" in event.keys():
                    customized = self.helper.customizeEvent(e)
                    if customized!=None:
                        events = events + [customized]
                else:
                    rule = event.get('RRULE')

                    expander = RRULEExpander(event.get('RRULE'), e.start, event.get('EXDATE'))


                        # calc event length
                    eventlen = e.end - e.start

                    for instance in expander:
                        revent = deepcopy(e)
                        revent.start = instance
                        revent.end = instance + eventlen
                        customized = self.customizeEvent(revent)
                        if customized != None:
                            events = events + [customized]
                        if limit>0 and len(events)>=limit:
                            break
        
                if limit>0 and len(events)>=limit:
                    break

        return events

if __name__=='__main__':
    f = IcalFetcher("https://www.google.com/calendar/ical/857iq9v0nfqrg3qmt4e00n53rc%40group.calendar.google.com/public/basic.ics")

    e = f.fetch()

    for ev in e:
        print str(ev)
