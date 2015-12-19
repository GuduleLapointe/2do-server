import re
import pickle
from datetime import timedelta
from helper import Helper

class JapanOpenHelper(Helper):
    hgre = re.compile("^[^:]+:[0-9]+:[^:]+$")

    hgexpr = {
    }

    def __init__(self):
        self.regions = pickle.loads(file('data/jogregions.pck').read())
        pass

    def findRegion(self, data):
        if data==None:
            return None

        for exp in JapanOpenHelper.hgexpr:
            if exp.search(data)!=None:
                return JapanOpenHelper.hgexpr[exp]

        longest = 0
        region_match = None

        for region in self.regions:
            if re.search(region, data, flags=re.I):
                if len(region) > longest:
                    longest = len(region)
                    region_match = region

        return region_match

    def customizeEvent(self, event):
        event = super(JapanOpenHelper, self).customizeEvent(event)

        if event.hgurl!=None and JapanOpenHelper.hgre.match(event.hgurl)==None:
            hgurl = self.findRegion(event.hgurl)

        if event.hgurl==None:
            hgurl = self.findRegion(event.description)
            if hgurl!=None:
                event.hgurl = 'jogrid.net:8002:' + hgurl

        return event


if __name__=='__main__':
    import requests
    
    page = requests.get("https://www.jogrid.net/wi/blocks/modlos/helper/world_map.php")

    # Name: <a style=\"cursor:pointer\" onClick=\"regionwin('061ad504-53a4-4f8b-9a9c-4d933ae96557')\"><b><u>Shibuya</u></b></a><br />
    if page.status_code==200:
        matches = map(
            lambda m: m.group(1).replace('*','\*').replace('.','\.').replace('?','\?'),
            re.finditer('Name: <a[^>]+><b><u>([^<]+)</u>', page.text)
        )
        file('data/jogregions.pck','w+').write(pickle.dumps(matches))
