# -*- coding: utf-8 -*-

import ParserCACM as pars
import TextRepresenter as txtrep
import Index
import pickle as pkl
from pathlib import Path
import numpy as np
import Weighter as we
import IRmodel as ir
from EvalCACM import QueryParserCACM
from Mesures import PrecisionMesure, ClusterRecallMesure, EvalIRModel
from diversity import DiversityCluster
from sklearn.cluster import KMeans
#from sklearn.model_selection import train_test_split as tts

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
data = "../easyCLEF08/easyCLEF08_text.txt"


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
print("Création des modèles\n")
wei = we.TfWeighter(ind)
vec = ir.Vectoriel(wei, False)
clu = [DiversityCluster(wei, vec, KMeans(), 100, "rank"),
DiversityCluster(wei, vec, KMeans(), 100, "asc"),
DiversityCluster(wei, vec, KMeans(), 100, "desc"),
DiversityCluster(wei, vec, KMeans(), 400, "rank"),
DiversityCluster(wei, vec, KMeans(), 400, "asc"),
DiversityCluster(wei, vec, KMeans(), 400, "desc")]


#lang = LanguageModel(wei)
#oka = Okapi(wei)

testQ = ' '.join(np.random.choice(list(ind.stems),5))
print(testQ)
print("glou")
print(clu[0].getRanking(testQ))

#testQ = ' '.join(np.random.choice(list(ind.stems),5))
#print(testQ)
#print("vec")
#print(vec.getRanking(testQ))
#print("lang")
#print(lang.getRanking(testQ))
#print("okapi")
#print(oka.getRanking(testQ))

print("Mise en place des tests\n")
qp = QueryParserCACM("../easyCLEF08/easyCLEF08_query.txt", "../easyCLEF08/easyCLEF08_gt.txt")
queries = list(qp)
np.random.shuffle(queries)

e = EvalIRModel(trep, queries[:20], [PrecisionMesure(), ClusterRecallMesure()], [vec] + clu)
eva = e.eval()
print((np.mean(eva, axis=2), np.std(eva, axis=2)))
print(eva)
