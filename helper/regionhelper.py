from helper import Helper
from exceptions import IOError
import os.path
import re
import pickle

class RegionHelper(Helper):
    def __init__(self):
        super(RegionHelper, self).__init__()
        self.loadRegions()

    def loadRegions(self):
        fetchFile = False

        fname = 'data/' + self.__class__.__name__ + '.pck'

        if not os.path.isfile(fname):
            self.__class__.fetchRegions()

        self.regions = pickle.loads(file(fname).read())

    def fetchRegions(self):
        raise Exception("fetchRegions not overridden in " + self.__class__.__name__)

    def findRegion(self, data):
        longest = 0
        region_match = None

        for region in self.regions:
            if re.search(region, data, flags=re.I):
                if len(region) > longest:
                    longest = len(region)
                    region_match = region

        return region_match

