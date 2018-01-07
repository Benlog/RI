# -*- coding: utf-8 -*-

import ParserCACM as pars
import TextRepresenter as txtrep
import Index
import pickle as pkl
from pathlib import Path
import numpy as np
import Weighter as we
import IRmodel as ir
from modelLang import LanguageModel
from EvalCACM import QueryParserCACM
from Mesures import *

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
    ind.indexation(path)
    with open(path+indexFilePkl,"wb") as f:
        pkl.dump(ind, f)

wei = we.Weighter(ind)

vec = ir.Vectoriel(wei, False)
lang = LanguageModel(wei)

testQ = ' '.join(np.random.choice(list(ind.stems),5))
print(testQ)
print("vec")
print(vec.getScores(testQ))
print(vec.getRanking(testQ))
print("lang")
print(lang.getScores(testQ))
print(lang.getRanking(testQ))

qp = QueryParserCACM("../cacm/cacm.qry", "../cacm/cacm.rel")
e = EvalIRModel(qp, [RecallMesure(), APMesure(), PrecisionMesure(), ClusterRecallMesure()])
print(e.eval([vec, lang]))

