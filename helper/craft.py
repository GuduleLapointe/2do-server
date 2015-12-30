import re
import pickle
from regionhelper import RegionHelper
import requests

class CraftHelper(RegionHelper):

    def customizeEvent(self, event):
        event = super(CraftHelper, self).customizeEvent(event)

        hgurl = self.findRegion(event.hgurl)
        if hgurl!=None:
            event.hgurl = 'craft-world.org:8002:' + hgurl
        return event

    @classmethod
    def fetchRegions(cls):
        page = requests.get("http://webapp.craft-world.org/moodle/blocks/modlos/helper/world_map.php")

        if page.status_code==200:
            matches = map(lambda m: m.group(1), re.finditer('new MapWindow\("Region Name: (.*?)<br', page.text))
            return matches
        else:
            raise Exception("Unable to retrieve region list, status "+str(page.status_code))

if __name__=='__main__':
    helper = CraftHelper()

