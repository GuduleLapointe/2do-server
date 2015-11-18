import re
from helper import Helper
from lib.category import Category

class PhaandoriaHelper(Helper):
    hgexp = re.compile('phaandoria.de:8002:([^/]+)')

    dictionary = {
        re.compile('Phaandoria Der Krater', re.I) : 'phaandoria.de:8002:Der Krater',
        re.compile('Carribean Beach', re.I) : 'phaandoria.de:8002:Carribean Beach',
        re.compile('Welcome', re.I) : 'phaandoria.de:8002:Phaandoria Welcome',
        re.compile('Mango', re.I) : 'phaandoria.de:8002:Mango',
    }

    def customizeEvent(self, event):
        event = super(PhaandoriaHelper, self).customizeEvent(event)

        if event.title=="Phaandoria Grid Friday Party":
            event.hgurl = "phaandoria.de:8002:Der Krater"
        else:
            for exp in PhaandoriaHelper.dictionary.keys():
                if exp.search(event.hgurl):
                    event.hgurl = PhaandoriaHelper.dictionary[exp]

        if event.hgurl == "" or event.hgurl == "-":
            return None
        else:
            match = PhaandoriaHelper.hgexp.search(event.hgurl)
            if match == None:
                event.hgurl="phaandoria.de:8002:Phaandoria Welcome"
            

        return event


if __name__=='__main__':
    pass
