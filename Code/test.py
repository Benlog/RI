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

import logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)
log_format = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
stream_handler = logging.StreamHandler()
#stream_handler.terminator = ""
stream_handler.setLevel(logging.DEBUG)
log.addHandler(stream_handler)
log.info("\033[?25l")

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

wei = we.BinaryWeighter(ind)

print("Création des modèles\n")
vec = ir.Vectoriel(ind, wei, False)
lang = LanguageModel(ind, wei)
oka = Okapi(ind, wei)

#testQ = ' '.join(np.random.choice(list(ind.stems),5))
#print(testQ)
#print("vec")
#print(vec.getRanking(testQ))
#print("lang")
#print(lang.getRanking(testQ))
#print("okapi")
#print(oka.getRanking(testQ))

#print("Mise en place des tests\n")
qp = QueryParserCACM("../cacm/cacm.qry", "../cacm/cacm.rel")
#e = EvalIRModel(trep, list(qp)[:10], [APMesure()], [vec, lang, oka])
#eva = e.eval()
#print((np.mean(eva, axis=2), np.std(eva, axis=2)))
#print(eva)


# Train Test
queries = list(qp)
np.random.shuffle(queries)
train, test = tts(queries[:20])

llamb = np.arange(0.1, 1, 0.2)
lk1   = np.arange(1.1, 2, 0.4)
lb    = np.arange(0.1, 1, 0.4)

import copy
lm = LanguageModel(ind, wei)
lml = []
for i in range(len(llamb)):
	lml.append(copy.deepcopy(lm))
	lml[i].lamb = llamb[i]

om = Okapi(ind, wei)
oml = []
for i in range(len(lk1)):
	omlt = []
	for j in range(len(lb)):
		omlt.append(copy.deepcopy(om))
		omlt[j].k1 = lk1[i]
		omlt[j].b = lb[j]
	oml += omlt

e = EvalIRModel(trep, train, [APMesure()], [vec] + lml + oml)
eva = e.eval()
print((np.mean(eva, axis=2), np.std(eva, axis=2)))
print(eva)
