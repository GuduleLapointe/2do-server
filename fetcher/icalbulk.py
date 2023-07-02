import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
import re
import codecs
import requests
from lib.webcache import WebCache

try:
    from helper import Helper
except ImportError:
    try:
        from helper.helper import Helper
    except ImportError:
        raise ImportError("Failed to import Helper from both 'helper' and 'helper.helper' modules")

class IcalBulk(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        config = self.read_ical_config()
        exclusions = self.load_exclusions()

        for grid in config:
            fetcher = IcalFetcher(
                grid['calendar_url'],
                grid['source_name'],
                eventlist,
                webcache,
                GenericHelper(grid['default_region'], exclusions.get(grid['source_name'], set())),
                default_region=grid['default_region'],  # Pass the default region to IcalFetcher
            )
            self.webcache = webcache  # Set the webcache attribute of the IcalBulk instance
            fetcher.webcache = webcache  # Set the webcache attribute of the fetcher
            fetcher.fetch()  # Fetch events for the current grid

    def read_ical_config(self):
        config = []
        with open('ical.cfg', 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith(";"):
                    source_info = line.split(",")
                    source_name = source_info[0].strip()
                    default_region = source_info[1].strip()
                    calendar_url = source_info[2].strip()

                    hg_url_parts = default_region.split(":")
                    if len(hg_url_parts) < 2:
                        print("Error: Invalid default region '{}' for source {}".format(default_region, source_name))
                        continue  # Skip adding this grid to the list

                    hostname = hg_url_parts[0]
                    port = hg_url_parts[1]

                    # Check if the grid info URL is reachable
                    grid_info_url = "http://{}:{}/get_grid_info".format(hostname, port)
                    try:
                        response = requests.get(grid_info_url, timeout=10)
                        if response.status_code == 200:
                            source = {
                                'source_name': source_name,
                                'hostname': hostname,
                                'default_region': default_region,
                                'port': port,
                                'calendar_url': calendar_url
                            }
                            print("Adding source {} {} {}".format(source_name, default_region, calendar_url))
                            config.append(source)
                        else:
                            print("Skipping source {}: failed to fetch {}:{} grid info. Status code: {}".format(source_name, hostname, port, response.status_code))
                    except requests.RequestException as e:
                        print("Skipping source {}: failed to fetch {}:{} grid info. Exception: {}".format(source_name, hostname, port, str(e)))
                    except requests.exceptions.ConnectionError as ce:
                        print("Skipping source {}: connection error while fetching {}:{} grid info. Exception: {}".format(source_name, hostname, port, str(ce)))

        return config

    def load_exclusions(self):
        exclusion_file = 'exclusions.txt'
        exclusions = {}
        try:
            with codecs.open(exclusion_file, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        source_name, event_title = line.split(None, 1)  # Split by tab or space
                        exclusions.setdefault(source_name, set()).add(event_title)
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
