import re
import pickle
from datetime import timedelta
from helper import Helper

class GcgHelper(Helper):
    hgre = re.compile("^[^:]+:[0-9]+:[^:]+$")

    def __init__(self):
        self.regions = pickle.loads(file('data/gcgregions.pck').read())

    def findRegion(self, data):
        if re.search("marina bay", data, flags=re.I):
            return "Marina Bay"
        if re.search("Hot Rod 50s Diner"):
            return "Dreamland"
        for region in self.regions:
            if re.search(region, data, flags=re.I):
                return region
        return None

    def customizeEvent(self, event):
        event = super(GcgHelper, self).customizeEvent(event)

        if GcgHelper.hgre.match(event.hgurl)==None:
            hgurl = self.findRegion(event.hgurl)
            if hgurl!=None:
                event.hgurl = 'login.greatcanadiangrid.ca:8002:' + hgurl

        # todo: correct for DST dynamically (ugh)
        event.start = event.start + timedelta(hours=4)
        event.end = event.end + timedelta(hours=4)

        return event


if __name__=='__main__':
    import requests
    
    page = requests.get("http://map.greatcanadiangrid.ca/")

    if page.status_code==200:
        matches = map(lambda m: m.group(1), re.finditer('new MapWindow\("Region Name: (.*?)<br', page.text))
        file('data/gcgregions.pck','w+').write(pickle.dumps(matches))
