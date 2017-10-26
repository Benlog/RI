# -*- coding: utf-8 -*-

import re
import ast
from pathlib import Path

class Index(object):

    def indexation(self, file):
        raise NotImplementedError()

    def getTfsForDoc(self, doc):
        raise NotImplementedError()

    def getTfsForStem(self, stem):
        raise NotImplementedError()

    def getStrDoc(self, doc):
        raise NotImplementedError()

class IndexOnFile(Index):

    def __init__(self, name, parser, textRepresenter):
        self.name = name
        self.docs = {}
        self.stems = {}
        self.docFrom = {}
        self.parser = parser
        self.textRepresenter = textRepresenter

    def indexation(self, path, verbose = True):
        if verbose : print("Début de l'indexation")
        self.path = path
        with open(self.path + "/" + self.name + "_index", "w+b") as fi :
            with open(self.path + "/" + self.name + "_inverted", "w+b") as fs :
                cur = 0
                doc = self.parser.nextDocument()
                if verbose : print("Création de l'index")
                while(doc):
                    if verbose : print("Indexation du doc :", doc.getId())
                    p, b, l = doc.get("from").split(";")
                    self.docFrom[doc.getId()] = (p, int(b), int(l))
                    stems = self.textRepresenter.getTextRepresentation(doc.getText())
                    if verbose == 2 : print("Stem :", stems):
                    for k,v in stems:
                        self.stems[k] = (0, len((doc.getId()+str(v)).encode()) + 5)
                    fi.write(str(stems).encode())
                    self.docs[doc.getId()] = (cur,fi.tell()-cur)
                    cur = fi.tell()
                    doc = self.parser.nextDocument()
                if verbose : print("Fin de l'index"):
                
                cur = 0
                for s,(d,l) in self.stems.items():
                    s = (cur, l+1)
                
                if verbose : print("Création de l'index inverse")
                if verbose == 2 : print("Stem à indexer :", self.stems)
                if verbose : print("Nombre :", len(self.stems))
                for k,(d,l) in self.docs:
                    fi.seek(d)
                    dic = fi.read(l)
                    d = ast.literal_eval(dic)
                    for s,(d,f) in self.stems:
                        fs.seek(d)
                        if d.get(s):
                            ds[doc] = d[s]
                if verbose == 2 : print("Docs :", ds)
                fs.write((s + ":" + str(ds) + "\n").encode())
                self.stems[s] = (cur,fi.tell())
                cur = fi.tell()
                if verbose : print("Fin de l'index inverse")
            if verbose : print("Fin de l'indexation")

    def getTfsForDoc(self, i):
        with open(self.path + "/" + self.name + "_index", "rb") as f :
            f.seek(self.docs[i][0])
            s = f.read(self.docs[i][1]).decode()
            return ast.literal_eval(re.match("(.*?):(.*)",s).group(2))

    def getTfsForStem(self, i):
        with open(self.path + "/" + self.name + "_inverted", "rb") as f:
            f.seek(self.stems[i][0])
            s = f.read(self.stems[i][1]).decode()
            return ast.literal_eval(re.match("(.*?):(.*)",s).group(2))

    def getStrDoc(self, i):
        with Path(self.docFrom[i][0]).open("rb") as f:
            f.seek(self.docFrom[i][1])
            return f.read(self.docFrom[i][2]).decode()

    def cheatIndexation(self, path, verbose = True):
        if verbose : print("Début de l'indexation")
        self.path = path
        with open(self.path + "/" + self.name + "_index", "w+b") as fi:
             with open(self.path + "/" + self.name + "_inverted", "w+b") as fs:
                 cur = 0
                 doc = self.parser.nextDocument()
                 tempStems = {}
                 if verbose : print("Création de l'index")
                 while(doc):
                     if verbose : print("Indexation du doc :", doc.getId())
                     p, b, l = doc.get("from").split(";")
                     self.docFrom[doc.getId()] = (p, int(b), int(l))
                     stems = self.textRepresenter.getTextRepresentation(doc.getText())
                     for s,i in stems.items() :
                         if tempStems.get(s):
                             tempStems[s][doc.getId()] = i
                         else:
                             tempStems[s] = {doc.getId() : i}
                     fi.write((doc.getId() + ":" + str(stems) + "\n").encode())
                     self.docs[doc.getId()] = (cur,fi.tell())
                     cur = fi.tell()
                     doc = self.parser.nextDocument()
                 if verbose : print("Fin de l'index")
                 if verbose : print("Création de l'index inverse")
                 if verbose == 2 : print("Stem à indexer :", tempStems)
                 if verbose : print("Nombre :", len(tempStems))
                 cur = 0
                 for n,(s,i) in enumerate(tempStems.items()):
                     if verbose : print("Indexation du stem :", s)
                     if verbose : print(n, "/", len(tempStems)-1)
                     fs.write((s + ":" + str(i) + "\n").encode())
                     self.stems[s] = (cur,fs.tell())
                     cur = fs.tell()
                 if verbose : print("Fin de l'index inverse")
             if verbose : print("Fin de l'indexation")
