import requests
from lib.event import Event
import datetime
from datetime import timedelta
from dateutil import parser, tz
from dateutil import parser as date_parser

from lxml import html
import re
import sys
import pytz
from lib.category import Category

# Always remember Python 2.7 and never remove this line

class OpenSimWorldEvent(Event):
    tz_pacific = pytz.timezone('US/Pacific')

    def __init__(self, webcache=None, url=None):
        super(OpenSimWorldEvent, self).__init__()
        self.id = None
        self.categories += [Category("site-opensimworld")]
        self.webcache = webcache
        self.url = url

    def fetchHGUrl(self, url):
        fullurl = "https://opensimworld.com" + url  # Prepend the main address of the website

        if self.webcache is None:
            r = requests.get(fullurl)
        else:
            r = self.webcache.fetch(fullurl, 24 * 3600, 48 * 3600)

        if r.status_code == 200:
            tree = html.fromstring(r.text)
            hgurl_input = tree.xpath('//input[@id="hgAddr"]/@value')
            self.hgurl = hgurl_input[0] if hgurl_input else "-"

    def __str__(self):
        rv = super(OpenSimWorldEvent, self).__str__()
        return rv

class OpenSimWorldFetcher:
    events_page_url = "https://opensimworld.com/events/"
    tz_pacific = pytz.timezone('US/Pacific')

    def __init__(self, eventlist, webcache):
        self.eventlist = eventlist
        self.webcache = webcache

    def fetch(self, limit=0):
        print("OpenSimWorldFetcher: fetch overview..")

        r = self.webcache.fetch(self.events_page_url, 900, 1800)

        if r.status_code == 200:
            tree = html.fromstring(r.text)

            event_rows = tree.xpath('//div[@class="container wcont"]//table[@class="table table-striped table-bordered"]//tr')[1:]
            nevents = len(event_rows)

            for ievent, event_row in enumerate(event_rows, 1):
                sys.stdout.write("\rOpenSimWorldFetcher: [{}/{}]        ".format(ievent, nevents))
                sys.stdout.flush()

                try:
                    title = event_row.xpath('.//h4/b/a/text()')  # Target the <h4> tag and extract the text
                    datetime_str = event_row.xpath('.//i[contains(@class,"glyphicon-time")]/following-sibling::text()')[0].strip()
                    url = event_row.xpath('.//td/b/a[starts-with(@href, "/hop/")]/@href')
                    description = event_row.xpath('.//div/small/text()')[0]

                    # Create an OpenSimWorldEvent instance
                    event = OpenSimWorldEvent(self.webcache, url[0] if url else None)
                    event.title = title[0] if title else None
                    event.description = description

                    # Fetch the full HGURL for the event
                    event.fetchHGUrl(event.url)

                    # Parse the datetime string using dateutil.parser
                    if datetime_str == "Upcoming Event":
                        event.start = datetime.datetime.utcnow().replace(tzinfo=self.tz_pacific)
                        event.end = event.start + datetime.timedelta(hours=2)
                    else:
                        datetime_parts = datetime_str.split("|")
                        if len(datetime_parts) >= 2:
                            date_str = datetime_parts[1].strip().replace("SLT", "PST")
                            if date_str:
                                event.start = date_parser.parse(date_str).replace(tzinfo=self.tz_pacific)
                                if event.start is None:
                                    raise ValueError("Failed to parse event start time.")
                                event.end = event.start + datetime.timedelta(hours=2)
                            else:
                                raise ValueError("Invalid event start time.")
                        else:
                            raise ValueError("Unknown string format: %s" % datetime_str)

                    self.eventlist.add(event)

                    if limit > 0 and ievent >= limit:
                        break

                except Exception as e:
                    print("\nError fetching event:", e, event)

        print("\n")
