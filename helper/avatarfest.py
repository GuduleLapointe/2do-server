import re
from helper import Helper

class AvatarFestHelper(Helper):
    dictionary = {
        'Digiworldz; Club La Ola' : 'login.digiworldz.com:8002:Sirens Grotto',
        'Club La Ola\'S 2Nd Avatar Fest Tie-In' : 'login.digiworldz.com:8002:Sirens Grotto',
    }

    def customizeEvent(self, event):
        event = super(AvatarFestHelper, self).customizeEvent(event)
        if event.hgurl in AvatarFestHelper.dictionary.keys():
            event.hgurl = AvatarFestHelper.dictionary[event.hgurl]
        return event


if __name__=='__main__':
    pass
