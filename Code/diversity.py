# -*- coding: utf-8 -*-

from IRmodel import IRmodel
from sklearn.cluster import AgglomerativeClustering, KMeans

import numpy as np


class DiversityCluster(IRmodel):

    def __init__(self, weighter, model, clustering, ndocs):
        super().__init__(weighter)
        self.model = model
        self.clustering = clustering
        self.ndocs = ndocs

    def getRanking(self, query):
        s = self.model.getRanking()[:self.ndocs]

        l = list(s.values())

        self.clustering.fit(l)
        c = self.clustering.labels_

        d = {s.keys()[i]: c[i] for i in range(len(c))}

        r = []
        a = np.array([])
        n = 0
        k = self.clustering.labels_

        for i in set(self.clustering.labels_):

            r.append()		# alterner sous-thèmes

            if i == k-1:
                n += 1

        return r


class KMeansDiversityCluster(DiversityCluster):

    def __init__(self, weighter, model, k):
        super().__init__(weighter, model, KMeans(k))
