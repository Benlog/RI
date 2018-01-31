# -*- coding: utf-8 -*-

from IRmodel import IRmodel

import numpy as np

def scalairProd(doc1, doc2):
    if len(doc1) <= len(doc2):
        small = doc1
    else:
        small = doc2
    sca = 0
    for k in small.keys():
       sca += doc1.get(k,0) * doc2.get(k,0)
    return sca

def norm(doc):
    r = np.array(list(doc.values()))
    return np.sqrt(np.sum(r*r))

def simCos(doc1,doc2):
    sca = scalairProd(doc1,doc2)
    r = sca/(norm(doc1)*norm(doc2))
    return (r+1)/2

class DiversityGlouton(IRmodel):

    def __init__(self, weighter, model, alpha = 0.5, ndocsSortie = 50, ndocs = 100, mesure = simCos):
        super().__init__(weighter)
        self.model = model
        self.aplha = alpha
        self.mesure = mesure
        self.ndocs = ndocs
        self.ndocsSortie = ndocsSortie

    def getRanking(self, query):
        qw = self.weighter.getWeightsForQuery(query)

        s = list(zip(*self.model.getRanking(query)[:self.ndocs]))[0]

        def value(d, l):
            dw = self.weighter.getDocWeightsForDoc(d)
            psiMesure = lambda d, l : - sum( 1 - simCos(d,self.weighter.getDocWeightsForDoc(i[0])) for i in l)/len(l)
            return self.aplha * self.mesure(dw,qw) - (1- self.aplha) * psiMesure(dw, l)

        r = [(s[0],0)]

        for i in range(min(self.ndocsSortie, len(s)-1)):
            r.append((max(set(s) - set(list(zip(*r))[0]), key = lambda x : value(x,r)), 0))

        return r

#class DiversityGloutonScore(IRmodel):
#
#    def __init__(self, weighter, model, alpha = 0.5, ndocsSortie = 50, ndocs = 100):
#        super().__init__(weighter)
#        self.model = model
#        self.aplha = alpha
#        self.ndocs = ndocs
#        self.ndocsSortie = ndocsSortie
#
#    def getRanking(self, query):
#
#        s = self.model.getRanking(query)[:self.ndocs]
#
#        def value(d, l):
#            dw = self.weighter.getDocWeightsForDoc(d)
#            psiMesure = lambda d, l : - sum( 1 - simCos(d,self.weighter.getDocWeightsForDoc(i)) for i in l)/len(l)
#            return self.aplha * d[1] - (1- self.aplha) * psiMesure(dw, l)
#
#        r = [(s[0][0],0)]
#
#        for i in range(min(self.ndocsSortie, len(s-1))):
#            r.append((max(set(s) - set(r), key = lambda x : value(x,r)), 0))
#
#        return list(zip(*r))