# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 11:43:40 2017

@author: 3200403
"""

import numpy   as np
import logging as log
import time


class EvalMesure(object):
    """
        Mesure d'évaluation
    """

    def eval(self, q, l):
        """
            Évaluation d'une liste de résultats pour une requête

            :param q: Requête de recherche
            :param l: Liste de résultats de recherche
        """
        log.error("%s est une classe abstraite.", self.__class__.__name__)
        raise NotImplementedError();


class RecallMesure(EvalMesure):
    """
        Mesure de rappel
    """

    def __init__(self, n=11):
        """
            Initialise une mesure de rappel

            :param n: Nombre de résultats à évaluer
        """
        self.n = n


    def eval(self, q, l):
        if len(q['revelent']) == 0:
            return {k : 1 for k in np.linspace(0, 1, self.n)}
        r = {}
        l = list(zip(*l))[0]

        for k in np.linspace(0,1,self.n):
            r[k] = max([len(l[:i] & q['revelent'].keys()) / i for i in range(1, len(l))\
             if (len(l[:i] & q['revelent'].keys()) / len(q['revelent'])) > k] + [0])

        return r


class APMesure(EvalMesure):
    """
        Mesure de précision moyenne
    """

    def eval(self, q, l):
        if len(q['revelent']) == 0:
            return 1
        if len(l) == 0:
            return 0
        l = list(zip(*l))[0]

        return (1/len(q['revelent'])) * sum([len(l[:i] & q['revelent'].keys()) / len(l[:i]) for i in range(1, len(l))  \
        if l[i] in q['revelent']])


class PrecisionMesure(EvalMesure):
    """
        Mesure de précision
    """

    def __init__(self, n=20):
        """
            Initialise une mesure de précision

            :param n: Nombre de résultats à évaluer
        """
        self.n = n


    def eval(self, q, l):
        l = list(zip(*l))[0]
        return len(l[:self.n] & q['revelent'].keys()) / self.n


class ClusterRecallMesure(EvalMesure):

    def __init__(self, n=20):
        """
            Initialise une mesure de rappel catégorique

            :param n: Nombre de résultats à évaluer
        """
        self.n = n


    def eval(self, q, l):
        if len(q['revelent']) == 0:
            return 1

        l = list(zip(*l))[0]

        return len({d[0] for d in l[:self.n]} & q['revelent'].keys()) / len(q['revelent'].keys())


class EvalIRModel(object):
    """
        Évaluateur EvalIRModel
    """

    def __init__(self, stemmer, queries, mesures, models):
        """
            Initialise un évaluateur de modèles

            :param queries: Requêtes à tester
            :param mesures: Mesures à utiliser
            :param models: Liste de modèles à évaluer
        """

        self.stemmer = stemmer
        self.queries = queries
        self.mesures = mesures
        self.models  = models

        log.info("%s instancié, avec %d requêtes, %d mesures et %d modèles.",
            self.__class__.__name__,
            len(self.queries),
            len(self.mesures),
            len(self.models))


    def eval(self):
        """
            Évalue une liste de modèles
        """

        log.info("Début de l'évaluation")
        log_start = time.time()

        mesures_mean = np.zeros((len(self.models), len(self.mesures)))
        mesures_std = np.zeros((len(self.models), len(self.mesures)))
        scores = {}

        for i, m in enumerate(self.models):

            log.info("Évaluation du modèle (%d) %s", i, m.__class__.__name__)

            for k, q in enumerate(self.queries):
                log.debug("Pré-traitement de la requête (%d) [%s]", k, q['id'])
                scores[k] = m.getRanking(q['text'])

            for j, e in enumerate(self.mesures):
                log.debug("Mesure par évaluation (%d) %s", j, e.__class__.__name__)
                evaluation = []

                for k, q in enumerate(self.queries):
                    log.debug("Traitement de la requête (%d) [%s]", k, q['id'])
                    evaluation.append(e.eval(q, scores[k]))

                mesures_mean[i, j] = np.mean(evaluation)
                mesures_std[i, j]  = np.std(evaluation)

                log.debug("Mesure du modèle (%d) %s par (%d) %s : %f +/- %f",
                    i,
                    m.__class__.__name__,
                    j,
                    e.__class__.__name__,
                    mesures_mean[i, j],
                    mesures_std[i, j])

        return mesures_mean, mesures_std
