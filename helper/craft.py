import re
import cPickle

class CraftHelper(object):
    def __init__(self):
        self.regions = cPickle.loads(file('data/craftregions.pck').read())

    def findRegion(self, data):
        for region in self.regions:
            if re.search(region, data, flags=re.I):
                return region
        return None


if __name__=='__main__':
    import requests
    
    page = requests.get("http://webapp.craft-world.org/moodle/blocks/modlos/helper/world_map.php")

    if page.status_code==200:
        matches = map(lambda m: m.group(1), re.finditer('new MapWindow\("Region Name: (.*?)<br', page.text))
        file('data/craftregions.pck','w+').write(cPickle.dumps(matches))
