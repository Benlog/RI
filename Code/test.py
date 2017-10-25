# -*- coding: utf-8 -*-

import ParserCACM as pars
import TextRepresenter as txtrep
import Index
import pickle as pkl
from pathlib import Path

path = "../test"


if Path(path+"/index.pkl").is_file() :
    with open(path+"/index.pkl","rb") as f:
        ind = pkl.load(f)
else :
    pars = pars.ParserCACM()
    trep = txtrep.PorterStemmer()
    data = "../cacm/cacm.txt"
    ind = Index.IndexOnFile("test", pars, trep)
    pars.initFile(data)
    ind.cheatIndexation(path)
    with open(path+"/index.pkl","wb") as f:
        pkl.dump(ind, f)



#print(pkl.dumps(ind, protocol=0))
