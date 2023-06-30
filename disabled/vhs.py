import re
from helper import Helper
from lib.category import Category

class VHSHelper(Helper):

    removeexp = [
        re.compile('^OG:\s*', flags=re.I),
        re.compile('^MG:\s*', flags=re.I),
        re.compile('^SL\+MG:\s*', flags=re.I),
        re.compile('^SL\+OG:\s*', flags=re.I),
        re.compile('^OSGrid \+ Metropolis Grid:\s*', flags=re.I),
        re.compile('^OSGrid:\s*', flags=re.I),
    ]

    def customizeEvent(self, event):
        event = super(VHSHelper, self).customizeEvent(event)

        if event.title == 'Teleport-Gates zu vielen Freebie shopping und Entdeckerorten im Hypergrid':
            return None

        if event.hgurl == 'auf dem:Infopfad':
            return None

        for exp in VHSHelper.removeexp:
            event.title = exp.sub('', event.title)

        if event.title == u'TEMPELRITTERambiente bei der Teststrecke fuer Avatare in Deutsch':
            return None

        return event


if __name__=='__main__':
    pass
