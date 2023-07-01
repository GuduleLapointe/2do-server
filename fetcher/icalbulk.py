import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
import re
import codecs

try:
    from helper import Helper
except ImportError:
    try:
        from helper.helper import Helper
    except ImportError:
        raise ImportError("Failed to import Helper from both 'helper' and 'helper.helper' modules")

class IcalBulk(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        config = self.read_config()
        exclusions = self.load_exclusions()
        for grid in config:
            fetcher = IcalFetcher(
                grid['calendar_url'],
                [Category(grid['grid_name'])],
                eventlist,
                webcache,
                GenericHelper(grid['default_region'], exclusions.get(grid['grid_name'], set()))
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

    def load_exclusions(self):
        exclusion_file = 'exclusions.txt'
        exclusions = {}
        try:
            with codecs.open(exclusion_file, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        grid_name, event_title = line.split(None, 1)  # Split by tab or space
                        exclusions.setdefault(grid_name, set()).add(event_title)
        except IOError:
            pass  # If exclusion file is not found, no exclusions will be applied
        return exclusions

    def customizeEvent(self, event):
        event = super(IcalBulk, self).customizeEvent(event)
        return event

class GenericHelper(Helper):
    hgre = re.compile("^[^:]+:[0-9]+:[^:]+$")

    def __init__(self, default_region, exclusions=None):
        super(GenericHelper, self).__init__()
        self.default_region = default_region
        self.exclusions = exclusions or set()

    def findRegion(self, data):
        if data == None or data == '' or data == '-':
            region = self.default_region
        else:
            region = None

        return region

    def customizeEvent(self, event):
        event = super(GenericHelper, self).customizeEvent(event)

        if isinstance(event.title, unicode):
            event_title = event.title
        else:
            event_title = event.title.decode('utf-8')

        if event_title in self.exclusions:
            return None

        hgurl = self.findRegion(event.hgurl)
        if hgurl is not None:
            hgurl = re.sub(r'^.*:\/\/', '', hgurl)
            event.hgurl = hgurl

        return event
