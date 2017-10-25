# -*- coding: utf-8 -*-

import re
import ast

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

    def __init__(self, name, parser, textRepresenter, docPath):
        self.name = name
        self.docs = {}
        self.stems = {}
        self.docFrom = {}
        self.parser = parser
        self.textRepresenter = textRepresenter
        self.docPath = docPath

    def indexation(self, path, verbose = True):
        #self.parser.initFile(path)
        self.parser.initFile(self.docPath)
        if verbose : print("Début de l'indexation")
        self.path = path
        with open(self.path + "/" + self.name + "_index", "w+b") as fi :
            with open(self.path + "/" + self.name + "_inverted", "w+b") as fs :
                cur = 0
                doc = self.parser.nextDocument()
                tempStems = set()
                if verbose : print("Création de l'index")
                while(doc):
                    if verbose : print("Indexation du doc :", doc.getId())
                    p, b, l = doc.get("from").split(";")
                    self.docFrom[doc.getId()] = (p, int(b), int(l))
                    stems = self.textRepresenter.getTextRepresentation(doc.getText())
                    if verbose == 2 : print("Stem :", stems)
                    tempStems = tempStems.union(stems)
                    fi.write((doc.getId() + ":" + str(stems) + "\n").encode())
                    self.docs[doc.getId()] = (cur,fi.tell())
                    cur = fi.tell()
                    doc = self.parser.nextDocument()
                if verbose : print("Fin de l'index")
                if verbose : print("Création de l'index inverse")
                if verbose == 2 : print("Stem à indexer :", tempStems)
                if verbose : print("Nombre :", len(tempStems))
                for n, s in enumerate(tempStems):
                    if verbose : print("Indexation du stem :", s)
                    if verbose : print(n, "/", len(tempStems)-1)
                    ds = {}
#                    for i,(b,l) in self.docs.items():
#                        fi.seek(b)
#                        buff = fi.read(l).decode()
#                        d = ast.literal_eval(re.match("(.*?):(.*)",buff)[2])
#                        if d.get(s):
#                            ds[i] = d[s]
                    fi.seek(0)
                    for l in fi:
                        match = re.match("(.*?):(.*)",l.decode())
                        doc, dic = match[1], match[2]
                        d = ast.literal_eval(dic)
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
            s = f.read(self.docs[i][1])
            return ast.literal_eval(re.match("(.*?):(.*)",s)[2])

    def getTfsForStem(self, i):
        with  open(self.path + "/" + self.name + "_inverted", "rb") as f:
            f.seek(self.stems[i][0])
            s = f.read(self.docs[i][1])
            return ast.literal_eval(re.match("(.*?):(.*)",s)[2])

    def getStrDoc(self, i):
        with open(self.docPath, "rb") as f:
            f.seek(self.docFrom[i][0])
            return f.read(self.docs[i][1])

	def cheatIndexation(self, path):
		self.path = path
        with open(self.path + "/" + self.name + "_index", "w+b") as fi:
		     with open(self.path + "/" + self.name + "_inverted", "w+b") as fs
		    cur = 0
		    doc = self.parser.nextDocument()
		    tempStems = {}
		    while(doc):
		        p, b, l = doc.other["from"].split(";")
		        self.docFrom[doc.id] = (p, int(b), int(l))
		        stems = self.textRepresenter(doc.getText())
		        for s,i in stems.items() :
		            tempStems[s][doc.id] = i
		        fi.write((doc.getid() + ":" + str(stems)).encode() + "\n")
		        self.docs{doc.getid()} = (cur,fi.tell())
		        cur = fi.tell()
		        doc = self.parser.nextDocument()
		    cur = 0
			for s,i in tempStems.items():
				fs.write((s + ":" + str(i)).encode() + "\n")
				self.stems[s] = (cur,fi.tell())
