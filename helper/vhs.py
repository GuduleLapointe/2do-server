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
    ]

    def customizeEvent(self, event):
        event = super(VHSHelper, self).customizeEvent(event)

        for exp in VHSHelper.removeexp:
            event.title = exp.sub('', event.title)

        return event


if __name__=='__main__':
    pass
