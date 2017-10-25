# -*- coding: utf-8 -*-

import ParserCACM as pars
import TextRepresenter as txtrep
import Index
import pickle as pkl

pars = pars.ParserCACM()
trep = txtrep.PorterStemmer()
data = "../cacm/cacm.txt"
ind = Index.IndexOnFile("test", pars, trep, data)
path = "../test"

ind.indexation(path)
with open(path+"/index.pkl","wb") as f:
    pkl.dump(ind, f)
#print(pkl.dumps(ind, protocol=0))
