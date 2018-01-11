# -*- coding: utf-8 -*-

import ParserCACM as pars
import TextRepresenter as txtrep
import Index
import pickle as pkl
from pathlib import Path
import numpy as np
import Weighter as we
import IRmodel as ir
from modelLang import LanguageModel, Okapi
from EvalCACM import QueryParserCACM
from Mesures import APMesure, EvalIRModel, RecallMesure
from sklearn.model_selection import train_test_split as tts

path = "../test"
trep = txtrep.PorterStemmer()
indexFilePkl = "/index.pkl"
data = "../cacm/cacm.txt"


if Path(path+"/index.pkl").is_file() :
    with open(path+indexFilePkl,"rb") as f:
        ind = pkl.load(f)
else :
    pars = pars.ParserCACM()
    ind = Index.IndexOnFile("test", pars, trep)
    pars.initFile(data)
    ind.indexation(path, 1)
    with open(path+indexFilePkl,"wb") as f:
        pkl.dump(ind, f)

wei = we.Weighter(ind)

print("Création des modèles\n")
vec = ir.Vectoriel(wei, False)
lang = LanguageModel(wei)
oka = Okapi(wei)

#testQ = ' '.join(np.random.choice(list(ind.stems),5))
#print(testQ)
#print("vec")
#print(vec.getRanking(testQ))
#print("lang")
#print(lang.getRanking(testQ))
#print("okapi")
#print(oka.getRanking(testQ))

print("Mise en place des tests\n")
qp = QueryParserCACM("../cacm/cacm.qry", "../cacm/cacm.rel")
e = EvalIRModel(qp, [APMesure()])
eva = e.eval([vec, lang, oka])
print((np.mean(eva, axis=2), np.std(eva, axis=2)))
print(eva)


# Train Test
queries = [q for q in qp]
train, test = tts(queries)

llamb = np.arange(0.1, 1, 0.1)
lk1   = np.arange(1.1, 2, 0.1)
lb    = np.arange(0.1, 1, 0.1)

lml = [LanguageModel(wei, lamb) for lamb in llamb]
oml = [Okapi(wei) for k1 in lk1 for b in lb]

eva = e.eval([vec] + lml + oml)
print((np.mean(eva, axis=2), np.std(eva, axis=2)))
print(eva)
