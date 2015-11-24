import re
import pickle
from datetime import timedelta
from helper import Helper

class FrancoGridHelper(Helper):
    hgre = re.compile("^[^:]+:[0-9]+:[^:]+$")

    def __init__(self):
        self.regions = pickle.loads(file('data/gcgregions.pck').read())

    def findRegion(self, data):
        if data=='None' or data=='-' or data==' ':
            return 'francogrid.org:8002:'
        return None

    def customizeEvent(self, event):
        event = super(FrancoGridHelper, self).customizeEvent(event)

        hgurl = self.findRegion(event.hgurl)
        if hgurl!=None:
            event.hgurl = hgurl

        return event


if __name__=='__main__':
    import requests
    
    page = requests.get("http://map.greatcanadiangrid.ca/")

    if page.status_code==200:
        matches = map(lambda m: m.group(1), re.finditer('new MapWindow\("Region Name: (.*?)<br', page.text))
        file('data/gcgregions.pck','w+').write(pickle.dumps(matches))
