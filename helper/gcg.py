import re
import pickle
from datetime import timedelta
from regionhelper import RegionHelper
import requests

class GcgHelper(RegionHelper):
    hgre = re.compile("^[^:]+:[0-9]+:[^:]+$")

    hgexpr = {
        re.compile("marina bay", flags=re.I)          : "Marina Bay",
        re.compile("hot rod 50s diner", flags=re.I)   : "Dreamland",
        re.compile("Manitou market", flags=re.I)        : "West Manitoulin Island",
        re.compile("Starlight Ballroom", flags=re.I)  : "Alabo Falls",
        re.compile("Starlight Mall", flags=re.I)   : "Alabo Falls",
    }

    bad_title = [
        re.compile("Submission Deadline", flags=re.I),
    ]

    def findRegion(self, data):
        if data==None:
            return None

        for exp in GcgHelper.hgexpr:
            if exp.search(data)!=None:
                return GcgHelper.hgexpr[exp]

        return super(GcgHelper, self).findRegion(data)

    def customizeEvent(self, event):
        # these are not real events:
        if event.title == "GCG Marketplace":
            return None

        if event.title == "(open 24/7) Labyrinth Walk by Dragon Ronin":
            return None

        for exp in GcgHelper.bad_title:
            if exp.search(event.title)!=None:
                return None

        event = super(GcgHelper, self).customizeEvent(event)

        if event.hgurl!=None and GcgHelper.hgre.match(event.hgurl)==None:
            hgurl = self.findRegion(event.hgurl)
            if hgurl==None:
                hgurl = self.findRegion(event.description)

                if hgurl=='Light':
                    hgurl = None
        
            if hgurl!=None:
                event.hgurl = 'login.greatcanadiangrid.ca:8002:' + hgurl
            else:
                event.hgurl = None

        # todo: correct for DST dynamically (ugh)
        event.start = event.start + timedelta(hours=3)
        event.end = event.end + timedelta(hours=3)

        return event

    @classmethod
    def fetchRegions(cls):
        page = requests.get("http://map.greatcanadiangrid.ca/")

        if page.status_code==200:
            matches = map(lambda m: m.group(1), re.finditer('new MapWindow\("Region Name: (.*?)<br', page.text))
            return matches
        else:
            raise Exception("Unable to retrieve region list, status "+str(page.status_code))

if __name__=="__main__":
    # trigger region list update
    helper = GcgHelper()
