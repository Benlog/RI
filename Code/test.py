# -*- coding: utf-8 -*-

import ParserCACM as pars
import TextRepresenter as txtrep
import Index
import pickle as pkl
from pathlib import Path
import numpy as np
import Weighter as we
import IRmode as ir

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

testQ = ' '.join(np.random.choice(list(ind.stems),5))
print(testQ)
print(vec.getScores(testQ))
print(vec.getRanking(testQ))