import numpy as np
from IRmodel import IRmodel


class ClusterDiversityModel(IRmodel):
    def __init__(self, model, clustering, index, wei):  # arg ord ?
        super().__init__(wei)
        self.index = index
        self.model = model            # Baseline
        self.clustering = clustering  # Algo de clustering

    def getScores(self, query, n=100):

        result = self.model.getRanking(query)[:n]
        voc = {s for (r, _) in result for s in self.weighter.getDocWeightsForDoc(r)}
        dic = {r: [r[s] if s in r else 0 for s in self.index.stems]
               for (r, _) in result}

        clr = self.clustering(dic)

        r = []

        j = 0
        c = len(clr)

        while c:
            c = len(clr)
            for i in clr:
                if len(i) > j:
                    r.append(i[j])
                else:
                    c -= 1
            j += 1



class GreedyDiversityModel(ClusterDiversityModel):

    def getScores(self, query, n=100):

        result = self.model.getRanking(query)[:n]
        voc = {s for (r, _) in result for s in self.weighter.getDocWeightsForDoc(r)}
        dic = {r: [r[s] if s in r else 0 for s in self.index.stems]
               for (r, s) in result}

        self.clustering
