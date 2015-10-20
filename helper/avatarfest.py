import re
import cPickle

class AvatarFestHelper(object):
    dictionary = {
        'Digiworldz; Club La Ola' : 'login.digiworldz.com:8002:Sirens Grotto',
        'Club La Ola\'S 2Nd Avatar Fest Tie-In' : 'login.digiworldz.com:8002:Sirens Grotto',
    }

    def customizeEvent(self, event):
        if event.hgurl in AvatarFestHelper.dictionary.keys():
            event.hgurl = AvatarFestHelper.dictionary[event.hgurl]
        return event


if __name__=='__main__':
    pass
