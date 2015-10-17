class HgUrl(object):

    dictionary = {
        'grid.3rdrockgrid.com:8002 Enerdhil (113, 116, 38)' : 'grid.3rdrockgrid.com:8002:Enerdhil',
        'grid.3rdrockgrid.com:8002 Enerdhil Enerdhil (113, 116, 38)' : 'grid.3rdrockgrid.com:8002:Enerdhil',
        'Seanchai Library ~ Grid.Kitely.Com:8002:Seanchai' : 'grid.kitely.com:8002:Seanchai',
        'Seanchai Library - Spaceworld (Grid.Kitely.Com:8002/Spaceworld)' : 'grid.kitely.com:8002:Spaceworld',
        'ROB\'s Rock Island(HG enabled) >grid.3rdrockgrid.com:8002:ROBs Rock Island' : 'grid.3rdrockgrid.com:8002:ROBs Rock Island',
        'Eldoland 1 (128,15,30)' : 'grid.3rdrockgrid.com:8002:Eldoland 1',
        'grid.3rdrockgrid.com:8002:ROBs Rock Island ,ROB\'s One World' : 'grid.3rdrockgrid.com:8002:ROBs Rock Island',
        'Roll Over Beethovens ' : 'grid.3rdrockgrid.com:8002:ROBs Rock Island',
        'Peapodyne' : 'grid.3rdrockgrid.com:8002:Peapodyne',
        'One Day Ahead Of The Moon At The Seanchai Library' : 'grid.kitely.com:8002:Seanchai',
        'In The Shadows At The Seanchai Library' : 'grid.kitely.com:8002:Seanchai',
        'Digiworldz; Club La Ola' : 'login.digiworldz.com:8002:Sirens Grotto',
        'Club La Ola\'S 2Nd Avatar Fest Tie-In' : 'login.digiworldz.com:8002:Sirens Grotto',
    }

    @staticmethod
    def normalize(url):
        #print "["+url + "]    ",
        if url in HgUrl.dictionary.keys():
            #print HgUrl.dictionary[url]
            return HgUrl.dictionary[url]
        #print url
        return url
        
