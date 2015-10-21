import requests
from lib.event import Event
import icalendar
import pytz
import datetime
from dateutil import rrule
from copy import copy

def fixDateTime(dt):
    if type(dt)==datetime.date:
        return pytz.utc.localize(datetime.datetime.combine(dt, datetime.time()))
    return dt

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

                e.title = event['SUMMARY'].title()
                e.description = ""
                if 'DESCRIPTION' in event.keys():
                    e.description = event['DESCRIPTION'].title()

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
                    e.hgurl = event['LOCATION'].title()
                except KeyError:
                    pass

                if "RRULE" in event.keys():
                    rule = event.get('RRULE')

                        # calc event length
                    eventlen = e.end - e.start

                        # fix until
                    until = rule.get('UNTIL')
                    if until!=None:
                        newuntil = []
                        for entry in until:
                            if type(entry)==datetime.date:
                                entry = datetime.datetime.combine(entry, datetime.time())
                                entry = pytz.utc.localize(entry)
                            newuntil += [entry]
                        rule['UNTIL'] = newuntil

                    rrlimit = pytz.utc.localize(datetime.datetime.now()) + datetime.timedelta(days=30)

                    rrset = rrule.rruleset()
                    rrset.rrule( rrule.rrulestr( rule.to_ical(), dtstart = e.start ) )

                    exdate = event.get('EXDATE')

                    if type(exdate)==type([]):
                        if exdate!=None:
                            for date in exdate:
                                for dd in date.dts:
                                    rrset.exdate(fixDateTime(dd.dt))
                    elif type(exdate)==icalendar.prop.vDDDLists:
                                for dd in exdate.dts:
                                    rrset.exdate(fixDateTime(dd.dt))


                    for instance in rrset:
                        instance = instance.tzinfo.normalize(instance)
                        print "- " + str(instance)
                        if instance > rrlimit:
                            break
                        revent = copy(e)
                        revent.start = instance
                        revent.end = instance + eventlen
                        events = events + [self.customizeEvent(revent)]
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
