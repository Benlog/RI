# -*- coding: utf-8 -*-

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

    indexPathName = "_index"
    invertedPathName = "_inverted"

    def __init__(self, name, parser, textRepresenter):
        self.name = name
        self.docs = {}
        self.stems = {}
        self.docFrom = {}
        self.parser = parser
        self.textRepresenter = textRepresenter

    def indexation(self, path, verbose = False):
        if verbose : print("Début de l'indexation")
        self.path = path
        with open(self.path + "/" + self.name + self.indexPathName, "w+b") as fi :
            with open(self.path + "/" + self.name + self.invertedPathName, "w+b") as fs :
                cur = 0
                doc = self.parser.nextDocument()
                if verbose : print("Création de l'index")
                while(doc):
                    if verbose == 2 : print("Indexation du doc :", doc.getId())
                    p, b, l = doc.get("from").split(";")
                    self.docFrom[doc.getId()] = (p, int(b), int(l))
                    stems = self.textRepresenter.getTextRepresentation(doc.getText())
                    if verbose == 2 : print("Stem :", stems)
                    for k,v in stems.items():
                        ls = self.stems.get(k, (0,0))[1]
                        self.stems[k] = (0, len((str(v)+str(doc.getId())).encode())+6+ls)
                    fi.write(str(stems).encode())
                    self.docs[doc.getId()] = (cur,fi.tell()-cur)
                    cur = fi.tell()
                    doc = self.parser.nextDocument()
                if verbose : print("Fin de l'index")

                if verbose : print("Création de l'index inverse")
                if verbose : print("Nombre de stem:", len(self.stems))
                cur = 0
                av = {}
                for s in self.stems:
                    l = self.stems[s][1]
                    self.stems[s] = (cur, l)
                    cur += l
                    av[s] = 0
                for k,(d,l) in self.docs.items():
                    if verbose == 2 : print("Indexation du doc :", k)
                    fi.seek(d)
                    dic = ast.literal_eval(fi.read(l).decode())
                    if verbose == 2 : print("Docs :", dic)
                    for s,(ds,ls) in self.stems.items():
                        if dic.get(s):
                            fs.seek(ds+av[s])
                            sW = "'" + str(k) + "'" + ": " + str(dic[s])
                            if av[s] == 0 : sW = '{' + sW
                            else : sW = ', ' + sW
                            if av[s] + len(sW.encode()) == ls - 1: sW = sW + '}'
                            fs.write(sW.encode())
                            if av[s] == ls :
                                print(fs.read(ls))
                            av[s] += len(sW.encode())

                if verbose : print("Fin de l'index inverse")
            if verbose : print("Fin de l'indexation")

    def getTfsForDoc(self, i):
        if i not in self.docs : return {}
        with open(self.path + "/" + self.name + "_index", "rb") as f :
            f.seek(self.docs[i][0])
            s = f.read(self.docs[i][1]).decode()
            #return ast.literal_eval(re.match("(.*?):(.*)",s).group(2))
            return ast.literal_eval(s)


    def getTfsForStem(self, i):
        if i not in self.stems : return {}
        with open(self.path + "/" + self.name + "_inverted", "rb") as f:
            f.seek(self.stems[i][0])
            s = f.read(self.stems[i][1]).decode()
            return ast.literal_eval(s)

    def getStrDoc(self, i):
        if i not in self.docFrom : return {}
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
                     fi.write(str(stems).encode())
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
                     fs.write(str(i).encode())
                     self.stems[s] = (cur,fs.tell())
                     cur = fs.tell()
                 if verbose : print("Fin de l'index inverse")
             if verbose : print("Fin de l'indexation")
