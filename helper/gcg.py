import re
import cPickle

class GcgHelper(object):
    def __init__(self):
        self.regions = cPickle.loads(file('data/gcgregions.pck').read())

    def findRegion(self, data):
        if re.search("marina bay beach club", data, flags=re.I):
            return "Marina Bay"
        for region in self.regions:
            if re.search(region, data, flags=re.I):
                return region
        return None


if __name__=='__main__':
    import requests
    
    page = requests.get("http://map.greatcanadiangrid.ca/")

    if page.status_code==200:
        matches = map(lambda m: m.group(1), re.finditer('new MapWindow\("Region Name: (.*?)<br', page.text))
        file('data/gcgregions.pck','w+').write(cPickle.dumps(matches))