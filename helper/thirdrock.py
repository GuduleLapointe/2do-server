import re
from helper import Helper

class ThirdRockHelper(Helper):
    dictionary = {
        re.compile('Enerdhil', flags=re.I)              : 'grid.3rdrockgrid.com:8002:Enerdhil',
        re.compile('ROB\'s Rock Island', flags=re.I)    : 'grid.3rdrockgrid.com:8002:ROBs Rock Island',
        re.compile('ROBs Rock Island', flags=re.I)      : 'grid.3rdrockgrid.com:8002:ROBs Rock Island',
        re.compile('Eldoland 1', flags=re.I)            : 'grid.3rdrockgrid.com:8002:Eldoland 1',
        re.compile('ROB\'s One World', flags=re.I)      : 'grid.3rdrockgrid.com:8002:ROBs Rock Island',
        re.compile('Roll Over Beethovens', flags=re.I)  : 'grid.3rdrockgrid.com:8002:ROBs Rock Island',
        re.compile('Peapodyne', flags=re.I)             : 'grid.3rdrockgrid.com:8002:Peapodyne',
        re.compile('UF Starfleet Astraios', re.I)       : 'grid.3rdrockgrid.com:8002:Starfleet Astraios',
    }

    hgexp = re.compile('([^:]+:[0-9]+:([^:/]*)?).*?$')
    hgexp2 = re.compile('([^:]+:[0-9]+)/(([^:/]*)?).*?$')

    def customizeEvent(self, event):
        # event has moved, but calendar not updated (yet?)
        if event.title=='Starfleet Boogie-Majel':
            return None

        event = super(ThirdRockHelper, self).customizeEvent(event)

        if event.title == 'UF Starfleet Astraios Mission':
            event.hgurl = 'grid.3rdrockgrid.com:8002:Starfleet Astraios'
        elif event.hgurl != None:
            hgurl = None
            for exp in ThirdRockHelper.dictionary:
                if exp.search(event.hgurl)!=None:
                    hgurl = ThirdRockHelper.dictionary[exp]
            if hgurl!=None:
            	event.hgurl = hgurl

        if event.hgurl!=None:
            print "===="
            print event.hgurl
            m = ThirdRockHelper.hgexp.search(event.hgurl)
            print m
            if m!=None:
                event.hgurl = m.group(1)
                return event
            m = ThirdRockHelper.hgexp2.search(event.hgurl)
            print m
            if m!=None:
                event.hgurl = m.group(1) + ":" + m.group(2)
                return event

        event.hgurl = None

        return event


if __name__=='__main__':
    pass
