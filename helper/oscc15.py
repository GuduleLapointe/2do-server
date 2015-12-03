import re
from helper import Helper
from lib.category import Category

class OSCC15Helper(Helper):
    hgenexp = re.compile('HyperGrid Enabled\?: Yes')
    hgurlexp = re.compile('HyperGrid URL: (http://)?(.+?)/?\s*HyperGrid Region')

    hgexp = re.compile('[^:]+:[0-9]+(:[^:]*)?')

    def customizeEvent(self, event):
        event = super(OSCC15Helper, self).customizeEvent(event)

        if OSCC15Helper.hgenexp.search(event.description)==None:
            return None

        match = OSCC15Helper.hgurlexp.search(event.description)
        if match == None:
            return None

        event.hgurl = match.group(2).strip().replace('/',':')

        if OSCC15Helper.hgexp.match(event.hgurl)==None:
            return None
        
        return event


if __name__=='__main__':
    pass
