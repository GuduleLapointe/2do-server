import re

class ThirdRockHelper(object):
    dictionary = {
        'grid.3rdrockgrid.com:8002 Enerdhil (113, 116, 38)' : 'grid.3rdrockgrid.com:8002:Enerdhil',
        'grid.3rdrockgrid.com:8002 Enerdhil Enerdhil (113, 116, 38)' : 'grid.3rdrockgrid.com:8002:Enerdhil',
        'ROB\'s Rock Island(HG enabled) >grid.3rdrockgrid.com:8002:ROBs Rock Island' : 'grid.3rdrockgrid.com:8002:ROBs Rock Island',
        'Eldoland 1 (128,15,30)' : 'grid.3rdrockgrid.com:8002:Eldoland 1',
        'grid.3rdrockgrid.com:8002:ROBs Rock Island ,ROB\'s One World' : 'grid.3rdrockgrid.com:8002:ROBs Rock Island',
        'Roll Over Beethovens ' : 'grid.3rdrockgrid.com:8002:ROBs Rock Island',
        'Peapodyne' : 'grid.3rdrockgrid.com:8002:Peapodyne',
    }

    def customizeEvent(self, event):
        if event.hgurl in ThirdRockHelper.dictionary.keys():
            event.hgurl = ThirdRockHelper.dictionary[event.hgurl]
        return event


if __name__=='__main__':
    pass
