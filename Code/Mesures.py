# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 11:43:40 2017

@author: 3200403
"""
from Evaluation import EvalMesure
import numpy as np


class RecallMesure(EvalMesure):
    def __init__(self, n=11):
        self.n = n
    def eval(self, q, l):
        r = {}
        for k in np.linspace(0,1,self.n):
            r[k] = max([len(l[:i] & q['revelent'].keys()) / i for i in range(1, len(l))\
             if (len(l[:i] & q['revelent'].keys()) / len(q['revelent'])) > k] + [0])
        return r



class APMesure(EvalMesure):
    def eval(self, q, l):
        return (1/len(q['revelent'])) * sum([len(l[:i] & q['revelent'].keys()) / len(l[:i]) for i in range(1, len(l))  \
        if l[i] in q['revelent']])


class PrecisionMesure(EvalMesure):
    def __init__(self, n=20):
        self.n = n
    def eval(self, q, l):
        return len(l[:self.n] & q['revelent'].keys()) / self.n


class ClusterRecallMesure(EvalMesure):
    def __init__(self, n=20):
        self.n = n
    def eval(self, q, l):
        return len({d[0] for d in l[:self.n]} & q['revelent'].keys()) / len(q['revelent'].keys())


class EvalIRModel(object):
    def __init__(self, queries, mesures):
        self.queries = queries
        self.mesures = mesures

    def eval(self, models):
        evals_q = []
        for q in self.queries:
            eva = np.empty((len(models),len(self.mesures),1))
            for i,m in enumerate(models):
                l = m.getRanking(q['text'])
                for j,e in enumerate(self.mesures):
                    eva[i][j] = e.eval(q, l)
            evals_q.append(eva)

        return np.concatenate(evals_q, 2)
#        evals_q = np.concatenate(evals_q, 2)
#
#        return (np.mean(evals_q, axis=2), np.std(evals_q, axis=2))
