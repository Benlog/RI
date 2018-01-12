# coding: utf-8

import numpy as np
import logging as log


class IRmodel(object):
    """
        IRmodel
    """

    def __init__(self, index, weighter):
        """
            Initialise un objet IRmodel

            :param index:    Objet Index
            :param weighter: Objet Weighter
        """
        self.index    = index
        self.weighter = weighter
        log.debug("%s est instancié.", self.__class__.__name__)


    def getScores(query):
        """
            Retourne les scores des documents pour une requête donnée

            :param query: Requête à traiter
            :type  query: str
        """
        log.error("%s est une classe abstraite.", self.__class__.__name__)
        raise NotImplementedError()


    def getRanking(self, query):
        """
            Retourne une liste de documents

            :param stem: Terme à traiter
            :type  stem: str
        """
        s = list(self.getScores(query).items())

        # Ex-equao aléatoires
        np.random.shuffle(s)

        # Tri des résultats
        k = lambda x : x[1]
        return sorted(s, key = k, reverse=True)


class Vectoriel(IRmodel):

    def __init__(self, index, weighter, normalized):
        super().__init__(index, weighter)
        self.normalized = normalized
        if self.normalized:
            self.norms = {doc : np.linalg.norm(self.weighter.getDocWeightsForDoc(doc)) for doc in self.index.docs}


    def getScores(self, query):

        scores = {}
        qw = self.weighter.getWeightsForQuery(query)

        if self.normalized:
            norm = np.linalg.norm(wq)

        for doc in self.index.docs:
            dw = self.weighter.getDocWeightsForStem(doc).items()
            scores[doc] = np.sum([qw[i] * dw[i] for i in qw if i in dw])

            if self.normalized:
                scores[doc] /= self.norms[doc] + norm

        return scores
