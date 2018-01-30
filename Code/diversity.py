# -*- coding: utf-8 -*-

from IRmodel import IRmodel
from sklearn.cluster import AgglomerativeClustering, KMeans

from collections import Counter
import numpy as np


class DiversityCluster(IRmodel):

    def __init__(self, weighter, model, clustering, ndocs, ordr="rank"):
        super().__init__(weighter)
        self.model = model
        self.clustering = clustering
        self.ndocs = ndocs
        self.ordr = ordr

    def getRanking(self, query):
        s = self.model.getRanking(query)[:self.ndocs]

        l = np.array([y for (_, y) in s]).reshape(-1, 1)

        self.clustering.fit(l)
        c = self.clustering.labels_

        nclu = len(set(c))
        r = []
        clu = []

        if self.ordr == "rank":

            for i in range(nclu):
                x = 0
                ld = True
                while ld:
                    if c[x] not in clu:
                        ld = False
                        clu.append(c[x])
                        c = np.delete(c, x)
                        r.append(s[x])
                        del(s[x])
                    x += 1

        elif self.ordr == "asc":
            clu = list(Counter(c).keys())

        elif self.ordr == "desc":
            clu = list(reversed(list(Counter(c).keys())))

        i = 0
        while s:
            x = 0
            ld = True
            while ld:
                if x == len(c):
                    del(clu[i%nclu])
                    nclu-=1
                    ld = False
                elif c[x] == clu[i%nclu]:
                    ld = False
                    r.append(s[x])
                    del(s[x])
                    c = np.delete(c, x)
                else:
                    x += 1
            i += 1

        return r


class KMeansDiversityCluster(DiversityCluster):

    def __init__(self, weighter, model, k):
        super().__init__(weighter, model, KMeans(k))
