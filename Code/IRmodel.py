# -*- coding: utf-8 -*-
import numpy as np

class IRmodel(object):

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

class Vectoriel(IRmodel):

    def __init__(self, weighter, normalized):
        super().__init__(weighter)
        self.normalized = normalized
        if self.normalized : self.norms = {}

    def getScores(self, query):
        scores = {}
        qw = self.weighter.getWeightsForQuery(query)

        if self.normalized:
            norm = np.linalg.norm(qw)

        for doc in self.weighter.index.docs:
            dw = self.weighter.getDocWeightsForStem(doc).items()
            scores[doc] = np.sum([qw[i] * dw[i] for i in qw if i in dw])

            if self.normalized:
                scores[doc] /= self.norms[doc] + norm

        return scores
