# -*- coding: utf-8 -*-
import numpy as np

class IRmode(object):

    def __init__(self, weighter):
        self.weighter = weighter

    def getScores(self, query):
        '''
        :return: return the dictionnary of docs -> their score
        :rtype: dict of doc -> float
        '''
        pass

    def getRanking(self, query):
        s = self.getScores(query)
        s = [(x,y) for x,y in s.items()]
        np.random.shuffle(s)
        k = lambda x : x[1]
        return sorted(s, key = k, reverse=True)
    
class Vectoriel(IRmode):
    
    def __init__(self, weighter, normalized):
        super().__init__(weighter)
        self.normalized = normalized
        if self.normalized : self.norms = {}
    
    def getScores(self, query):
        wq = self.weighter.getWeightsForQuery(query)
        if self.normalized : norm = np.linalg.norm(wq)
        r = {}
        for k,v in wq.items():
            for k2,v2 in self.weighter.getDocWeightsForStem(k).items():
                r[k2] = v * v2 + r.get(k2, 0)
                if self.normalized :
                    self.norms[k2] = np.linalg.norm(self.weighter.getDocWeightsForDoc(k2))
                    r[k2] /= self.norms[k2] + norm
        return r
    
    
        