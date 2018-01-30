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
from Mesures import PrecisionMesure, ClusterRecallMesure, EvalIRModel
from gloutonDiversity import DiversityGlouton
#from sklearn.model_selection import train_test_split as tts

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

wei = we.TfWeighter(ind)

print("Création des modèles\n")
vec = ir.Vectoriel(wei, False)
#lang = LanguageModel(wei)
#oka = Okapi(wei)
glou = DiversityGlouton(wei, vec, ndocsSortie = 5)
testQ = ' '.join(np.random.choice(list(ind.stems), 5))
print(testQ)
print("glou")
print(glou.getRanking(testQ))
#print("lang")
#print(lang.getRanking(testQ))
#print("okapi")
#print(oka.getRanking(testQ))

#print("Mise en place des tests\n")
#qp = QueryParserCACM("../easyCLEF08/easyCLEF08_query.txt", "../easyCLEF08/easyCLEF08_gt.txt")
#e = EvalIRModel(qp, [PrecisionMesure(), ClusterRecallMesure()])
#eva = e.eval([vec, lang, oka])
#print((np.mean(eva, axis=2), np.std(eva, axis=2)))
#print(eva)