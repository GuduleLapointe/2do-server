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

    descexp = {
        re.compile('Der Krater', re.I) : 'phaandoria.de:8002:Der Krater',
    }

    def customizeEvent(self, event):
        event = super(PhaandoriaHelper, self).customizeEvent(event)

        if event.title=="Phaandoria Grid Friday Party":
            event.hgurl = "phaandoria.de:8002:Der Krater"
        else:
            for exp in PhaandoriaHelper.dictionary.keys():
                if event.hgurl!=None and exp.search(event.hgurl):
                    event.hgurl = PhaandoriaHelper.dictionary[exp]

        if event.hgurl == "" or event.hgurl == "-" or event.hgurl == None:
            matched = False
            for exp in PhaandoriaHelper.descexp:
                if exp.search(event.description):
                    event.hgurl = PhaandoriaHelper.descexp[exp]
                    matched = True
            if not matched:
                return None
        elif event.hgurl!=None:
            match = PhaandoriaHelper.hgexp.search(event.hgurl)
            if match == None:
                event.hgurl="phaandoria.de:8002:Phaandoria Welcome"
            

        return event


if __name__=='__main__':
    pass
