# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 11:43:40 2017

@author: 3200403
"""
from Evaluation import EvalMesure
import numpy as np


class RecallMesure(EvalMesure):
    def eval(l, nbLevels = 11):
        r = {}
        for k in numpy.linspace(0,1,nbLevels):
            r[k] = max([len(l[1][:i] & l[0]['revelent'].keys()) / i  for i in range(1, len(l[1]))\
             if (len(l[1][:i] & l[0]['revelent'].keys()) / len(l[0]['revelent'])) > k])
        return r



class APMesure(EvalMesure):
    def eval(l):
        return (1/len(l[0]['revelent'])) * sum([len(l[1][:i] & l[0]['revelent'].keys()) / len(l[1][:i]) for i in range(1, len(l[1]))  \
        if l[1][i] in l[0]['revelent']])


class PrecisionMesure(EvalMesure):
    def eval(l, n=20):
        return len(l[1][:n] & l[0]['revelent'].keys()) / n


class ClusterRecallMesure(EvalMesure):
    def eval(l, n=20):
        return len({d[0] for d in l[1][:n] & l[0]['revelent'].values()}) / len({d[0] for d in l[0]['revelent'].values()})


class EvalIRModel(object):
    def __init__(self, query, mesures):
        self.query = query
        self.mesures = mesures

    def eval(self, models):
        r = []
        for m in models:
            evals_q = []
            for q in self.query:
                l = m.getRanking(q)
                evals = []
                for e in self.mesures:
                    evals.append(e.eval(l))
                evals_q.append(evals)
            evals_q = np.array(evals_q)

            r.append((np.mean(evals, axis=1), np.std(evals, axis=1)))

        return r