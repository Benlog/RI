# -*- coding: utf-8 -*-

class IRmode(object):

    def __init__(self, weighter):
        self.weighter = weighter

    def getScores(self, query):
        pass

    def getRanking(self, query):
        pass
    
class Vectoriel(IRmode):
    
    def getScores(self, query):
        wq = self.weighter.getWeightsForQuery(query)
        r = {}
        for k,v in wq.items():
            for k2,v2 in self.weighter.getDocWeightsForStem(k):
                r[k2] = v * v2 + r.get(k2, 0)
        return r
    
    
        