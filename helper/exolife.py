import re
from helper import Helper

class ExoLifeHelper(Helper):
    hgexp = re.compile('(.*)\s+hop://hg\.exo-life\.onl:8032')

    def customizeEvent(self, event):
        event = super(ExoLifeHelper, self).customizeEvent(event)

        if event.hgurl!=None:
            match = ExoLifeHelper.hgexp.search(event.hgurl)
            if match!=None:
                event.hgurl = 'hg.exo-life.onl:8032:'+match.group(1)
            else:
                # no hgurl -> no listing (exo has non-hg enabled regions as well)
                return None

        return event

if __name__=='__main__':
    pass
