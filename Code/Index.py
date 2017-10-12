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
        #self.parser.initFile(path)
        self.path = path
        fi = open(self.path + "/" + self.name + "_index", "w+b")
        fs = open(self.path + "/" + self.name + "_inverted", "w+b")
        cur = 0
        doc = self.parser.nextDocument()
        while(doc):
            p, b, l = doc.other["from"].split(";")
            self.docFrom[doc.id] = (p, int(b), int(l))
            stems = self.textRepresenter(doc.getText())
            for s in stems:
                self.stems[s] = None
            fi.write((doc.getid() + " : " + str(stems)).encode() + "\n")
            self.docs{doc.getid()} = (cur,fi.tell())
            cur = fi.tell()
            doc = self.parser.nextDocument()
        for s in self.stems:
            ds = 
            for i,(b,l) in self.docs.items():
                f.seek(b)
                s = f.read(self.docs[i][1]).splitlines()
                s = map(lambda x : str.split(x, ":"), s)
                d = dict(s)
                
            fs.write()

    def getTfsForDoc(self, i):
        f = open(self.path + "/" + self.name + "_index", "rb")
        f.seek(self.docs[i][0])
        s = f.read(self.docs[i][1])
        s = re.find()
        return dict(s)