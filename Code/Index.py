# -*- coding: utf-8 -*-

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

    def createFiles(self, path):
        #path = "../Data"
        open(path + "/" + self.name + "_index", "x").close()
        open(path + "/" + self.name + "_inverted", "x").close()

    def indexation(self, path):
        self.parser.initFile(path)
        fi = open(path + "/" + self.name + "_index", "w+b")
        fs = open(path + "/" + self.name + "_inverted", "w+b")
        cur = 0
        doc = self.parser.nextDocument()
        while(doc):
            stems = self.textRepresenter(doc.getText())
            fi.write((doc.getid() + " : " + str(stems)).encode())
            self.docs{doc.getid()} = (cur,fi.tell())
            cur = fi.tell()
            doc = self.parser.nextDocument()


