from helper import Helper
from exceptions import IOError
import os.path
import re
import pickle
from time import time
import logging

class RegionHelper(Helper):
    REGION_LIST_EXPIRY  = 24*3600

    def __init__(self):
        super(RegionHelper, self).__init__()
        self.loadRegions()

    def refreshRegions(self, fname):
        logging.info('Reloading regionlist for '+self.__class__.__name__)
        regions = self.__class__.fetchRegions()
        file(fname,'w+').write(pickle.dumps({
            'expiry'  : time() + RegionHelper.REGION_LIST_EXPIRY,
            'regions' : regions
        }))
        return regions


    def loadRegions(self):
        fetchFile = False

        fname = 'data/' + self.__class__.__name__ + '.pck'

        if not os.path.isfile(fname):
            self.regions = self.refreshRegions(fname)
        else:
            raw = pickle.loads(file(fname).read())
            if raw['expiry'] <= time():
                self.regions = self.refreshRegions(fname)
            else:
                self.regions = raw['regions']

    def fetchRegions(self):
        raise Exception("fetchRegions not overridden in " + self.__class__.__name__)

    def findRegion(self, data):
        longest = 0
        region_match = None

        if data==None:
            return None

        for region in self.regions:
            if re.search(region, data, flags=re.I):
                if len(region) > longest:
                    longest = len(region)
                    region_match = region

        return region_match

