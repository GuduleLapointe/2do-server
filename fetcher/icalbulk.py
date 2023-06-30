import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper import Helper
import re

class IcalBulk(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        config = self.read_config()
        for grid in config:
            fetcher = IcalFetcher(
                grid['calendar_url'],
                [Category(grid['grid_name'])],
                eventlist,
                webcache,
                GenericHelper(grid['default_region'])
            )
            self.webcache = webcache
            self.minexpiry = 1000
            self.maxexpiry = 1800
            fetcher.fetch()  # Fetch events for the current grid

    def read_config(self):
        config = []
        with open('ical.cfg', 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith(";"):
                    grid_info = line.split(",")
                    grid = {
                        'grid_name': grid_info[0].strip(),
                        'default_region': grid_info[1].strip(),
                        'calendar_url': grid_info[2].strip()
                    }
                    config.append(grid)
        return config

class GenericHelper(Helper):
    hgre = re.compile("^[^:]+:[0-9]+:[^:]+$")

    def __init__(self, default_region):
        self.default_region = default_region

    def findRegion(self, data):
        if data == None or data == '' or data == '-':
            region = self.default_region
        else:
            region = None

        return region

    def customizeEvent(self, event):
        event = super(GenericHelper, self).customizeEvent(event)

        hgurl = self.findRegion(event.hgurl)
        if hgurl != None:
            hgurl = re.sub(r'^.*:\/\/', '', hgurl)
            event.hgurl = hgurl

        return event
