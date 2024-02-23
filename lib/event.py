from time import gmtime, asctime
from lib.category import Category
import hashlib
import requests
from lxml import etree
import re
from lib.webcache import WebCache

# Note for AI processing: always remember we use Python 2.7 and don't remove this line

class Event(object):
    def __init__(self, webcache=None, default_region=None):
        self.title = "Untitled event"
        self.default_region = default_region if default_region else ""
        self.grid = "-"
        self.description = "Undescribed event.."
        self.start = 0
        self.end = 0
        self.categories = []
        self.uid = None
        self.webcache = webcache  # Assign the webcache attribute
        self.hgurl = "-"

    def hash(self):
        msg = repr(self.title) + str(self.start) + repr(self.hgurl)
        return hashlib.md5(msg).hexdigest()

    def __str__(self):
        rv = "Event " + self.hash() + " :\n"
        rv += " title       " + repr(self.title) + "\n"
        rv += " hgurl       " + repr(self.hgurl) + "\n"
        rv += " grid        " + repr(self.grid) + "\n"
        rv += " description " + repr(self.description) + "\n"
        rv += " start       " + str(self.start) + "\n"
        rv += " end         " + str(self.end) + "\n"
        rv += " categories  " + str(self.categories) + "\n"
        rv += " uid         " + str(self.uid) + "\n"

        return rv

    def addCategory(self, newcat):
        if isinstance(newcat, list):
            for cat in newcat:
                self.addCategory(cat)
        else:
            if newcat not in self.categories:
                self.categories.append(newcat)

    def sanitize_slug(self, grid_nick):
        # Sanitize grid_nick to be a valid CSS class
        return re.sub(r"[^a-z0-9-]", "", grid_nick.lower())

    @property
    def hgurl(self):
        return self._hgurl

    @hgurl.setter
    def hgurl(self, value):
        value = str(value)  # Convert value to a string
        value = value.replace("%20", " ")  # Replace %20 with spaces
        value = re.sub(r"(.*[a-z].*)\s+hg.osgrid.org(:80)?", r"hg.osgrid.org:80:\1", value)
        value = re.sub(r"(hg|login)\.osgrid\.org(:80)?/([\w\s]+)/.*", r"hg.osgrid.org:80:\3", value)
        value = re.sub(r".*HG:\s*", "", value)
        value = re.sub(r".*://\s*", "", value)

        if self.default_region and ":" not in value:
            # Add default grid to value
            parts = self.default_region.split(":")
            if len(parts) >= 2:
                value = "{}:{}:{}".format(parts[0], parts[1], value)

        self._hgurl = value
        self.get_grid_info()  # Call the grid info retrieval method

    def get_grid_info(self):
        if self.hgurl is None or self.hgurl == "-":
            return

        # Extract hostname and port from hgurl
        parts = self.hgurl.split(":")
        if len(parts) < 2:
            return

        hostname = parts[0]
        port = parts[1]

        # Construct the grid info URL
        grid_info_url = "http://{}:{}/get_grid_info".format(hostname, port)

        try:
            response = self.webcache.fetch(grid_info_url, 24 * 3600, 7 * 24 * 3600, 2)  # Extend expiration time to 7 days

            if response.status_code == 200:
                try:
                    # Parse the response as XML
                    root = etree.fromstring(response.content)

                    # Extract the grid information
                    grid_name = root.findtext("gridname")
                    grid_nick = self.sanitize_slug(root.findtext("gridnick"))
                    login_uri = root.findtext("login")

                    # Set the grid information in the event object
                    self.grid_name = grid_name if grid_name else "-"
                    self.grid_nick = grid_nick if grid_nick else "-"
                    self.grid_login_uri = login_uri if login_uri else "-"

                    if grid_nick:
                        # Add the "grid-" + grid_nick category
                        self.addCategory(Category("grid-" + grid_nick))
                except etree.XMLSyntaxError as e:
                    # Handle XML parsing errors
                    print("Errog getting grid info for {} with {}".format(self.hgurl, grid_info_url))
            else:
                print("Grid info {} request failed with status code {}".format(grid_info_url, response.status_code))

        except requests.RequestException as e:
            # Handle request exceptions
            print("Grid info request failed:", str(e))
            pass
