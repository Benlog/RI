# -*- coding: utf-8 -*-
from IRmodel import IRmodel

import numpy as np


class LanguageModel(IRmodel):
    def __init__(self, weighter, lamb = 0.5):
        super().__init__(weighter)
        self.lamb = lamb
        self.corpusLen = sum([sum(self.weighter.getDocWeightsForDoc(d).values()) for d in self.weighter.index.docs])

    def getScores(self, query):
        wq = self.weighter.getWeightsForQuery(query)
        r = {}
        l = {}
        for k,v in wq.items():
            tfCorpus = 0
            for k2,v2 in self.weighter.getDocWeightsForStem(k).items():
                    r[k2] = 0
                    if k2 not in l :
                        l[k2] = sum(self.weighter.getDocWeightsForDoc(k2).values())
                    tfCorpus += v2
            for k2,v2 in self.weighter.getDocWeightsForStem(k).items():
                r[k2] += v * np.log(self.lamb * (v/l[k2]) + (1-self.lamb) * (tfCorpus/self.corpusLen))
        return r