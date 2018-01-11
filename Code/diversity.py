# -*- coding: utf-8 -*-

from IRmodel import IRmodel
from sklearn.cluster import AgglomerativeClustering

import numpy as np

class DiversityCluster(IRmodel):

    def __init__(self, weighter, model, clustering):
        super().__init__(weighter)
        self.model = model
        self.clustering = clustering

    def getScores(self, query):
        s = self.model.getScores()
        
        return r
