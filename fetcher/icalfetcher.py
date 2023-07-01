import requests
import re
from lib.event import Event
import icalendar
import pytz
import datetime
from dateutil import rrule
from copy import copy, deepcopy
from lib.rrule import RRULEExpander

class IcalFetcher(object):
    tz_pacific = pytz.timezone('US/Pacific')

    def __init__(self, url, categories, eventlist, webcache=None, helper=None):
        self.url = url
        self.categories = categories
        self.helper = helper
        self.eventlist = eventlist
        self.cache = webcache
        self.minexpiry = 1800
        self.maxexpiry = 3600

    def customizeEvent(self, event):
        if self.helper is not None:
            return self.helper.customizeEvent(event)
        return event

    def fetch(self, limit=0, tz=pytz.utc):
        print("IcalFetcher: get url", self.url)
        print("IcalFetcher: timezone", tz)

        r = self.cache.fetch(self.url, self.minexpiry, self.maxexpiry)

        events = []

        if r.status_code == 200:
            cal = icalendar.Calendar.from_ical(r.text)
            cal_events = cal.walk(name="VEVENT")

            for event in cal_events:
                e = Event(self.cache)

                if self.categories is not None:
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

                if type(e.start) == datetime.date:
                    e.start = datetime.datetime.combine(e.start, datetime.time())

                if type(e.end) == datetime.date:
                    e.end = datetime.datetime.combine(e.end, datetime.time())

                if e.start.tzinfo is None or e.start.tzinfo.utcoffset(e.start) is None:
                    e.start = self.tz_pacific.localize(e.start)

                if e.end.tzinfo is None or e.end.tzinfo.utcoffset(e.end) is None:
                    e.end = self.tz_pacific.localize(e.end)

                try:
                    e.hgurl = event.get('LOCATION')
                except KeyError:
                    pass

                try:
                    e.uid = event.get('UID')
                except KeyError:
                    pass

                # TODO: log event w/o location and ignore
                if e.hgurl is None:
                    e.hgurl = "-"

                if "RRULE" not in event.keys():
                    customized = self.customizeEvent(e)
                    if customized is not None:
                        self.eventlist.add(customized)
                else:
                    rule = event.get('RRULE')

                    expander = RRULEExpander(event.get('RRULE'), e.start, event.get('EXDATE'))

                    # Calculate event length
                    eventlen = e.end - e.start

                    for instance in expander:
                        revent = deepcopy(e)
                        revent.start = instance
                        revent.end = instance + eventlen
                        customized = self.customizeEvent(revent)
                        if customized is not None:
                            self.eventlist.add(customized)
                        if limit > 0 and len(events) >= limit:
                            break

                if limit>0 and len(events)>=limit:
                    break

if __name__=='__main__':
    from lib.eventlist import EventList
    from lib.webcache import WebCache

    eventlist = EventList()

    cache = WebCache("data/test_phaandoria.cache")

    f = IcalFetcher("https://www.google.com/calendar/ical/857iq9v0nfqrg3qmt4e00n53rc%40group.calendar.google.com/public/basic.ics", [], eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
