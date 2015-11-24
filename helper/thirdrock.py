import re
from helper import Helper

class ThirdRockHelper(Helper):
    dictionary = {
        'grid.3rdrockgrid.com:8002 Enerdhil (113, 116, 38)' : 'grid.3rdrockgrid.com:8002:Enerdhil',
        'grid.3rdrockgrid.com:8002 Enerdhil Enerdhil (113, 116, 38)' : 'grid.3rdrockgrid.com:8002:Enerdhil',
        'ROB\'s Rock Island(HG enabled) >grid.3rdrockgrid.com:8002:ROBs Rock Island' : 'grid.3rdrockgrid.com:8002:ROBs Rock Island',
        'Eldoland 1 (128,15,30)' : 'grid.3rdrockgrid.com:8002:Eldoland 1',
        'grid.3rdrockgrid.com:8002:ROBs Rock Island ,ROB\'s One World' : 'grid.3rdrockgrid.com:8002:ROBs Rock Island',
        'Roll Over Beethovens ' : 'grid.3rdrockgrid.com:8002:ROBs Rock Island',
        'Peapodyne' : 'grid.3rdrockgrid.com:8002:Peapodyne',
    }

    expr = {
        re.compile('UF Starfleet Astraios', re.I) : 'grid.3rdrockgrid.com:8002:Starfleet Astraios',
    }

    def customizeEvent(self, event):
        # event has moved, but calendar not updated (yet?)
        if event.title=='Starfleet Boogie-Majel':
            return None

        event = super(ThirdRockHelper, self).customizeEvent(event)

        if event.hgurl != None:
            if event.hgurl in ThirdRockHelper.dictionary.keys():
                event.hgurl = ThirdRockHelper.dictionary[event.hgurl]
            else:
                for exp in self.expr:
                    if exp.search(event.hgurl):
                        event.hgurl = self.expr[exp]

        return event


if __name__=='__main__':
    pass
