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
    
    def createFiles(path = "../Data"):
        open(path + "/" + self.name + "_index", "x").close()
        open(path + "/" + self.name + "_inverted", "x").close()
    
    def indexation(self, file):
        self.parser.initFile(file)
        fi = open(path + "/" + self.name + "_index", "w+b")
        fs = open(path + "/" + self.name + "_inverted", "w+b")
        curi = 0
        curs = 0
        doc = self.parser.nextDocument()
        while(doc):
            stems = self.textRepresenter(doc.getText())
            fi.write((doc.getid() + " : " + str(stems)).encode())
            doc = self.parser.nextDocument()
            
    
    