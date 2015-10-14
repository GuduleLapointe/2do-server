class HgUrl(object):

    dictionary = {
        'grid.3rdrockgrid.com:8002 Enerdhil (113, 116, 38)' : 'grid.3rdrockgrid.com:8002:Enerdhil',
        'grid.3rdrockgrid.com:8002 Enerdhil Enerdhil (113, 116, 38)' : 'grid.3rdrockgrid.com:8002:Enerdhil',
        'Seanchai Library ~ Grid.Kitely.Com:8002:Seanchai' : 'grid.kitely.com:8002:Seanchai',
        'Seanchai Library - Spaceworld (Grid.Kitely.Com:8002/Spaceworld)' : 'grid.kitely.com:8002:Spaceworld',`
        'ROB\'s Rock Island(HG enabled) >grid.3rdrockgrid.com:8002:ROBs Rock Island' : 'grid.3rdrockgrid.com:8002:ROBs Rock Island',
        'Eldoland 1 (128,15,30)' : 'grid.3rdrockgrid.com:8002:Eldoland 1',
        'grid.3rdrockgrid.com:8002:ROBs Rock Island ,ROB\'s One World' : 'grid.3rdrockgrid.com:8002:ROBs Rock Island',
    }

    @staticmethod
    def normalize(url):
        if url in HgUrl.dictionary.keys():
            return HgUrl.dictionary[url]
        return url
        
