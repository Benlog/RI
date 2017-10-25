# -*- coding: utf-8 -*-

class Weighter(Object):

    def __init__(self, index, textRepresenter):
        self.index = index
        self.textRepresenter = textRepresenter

    def getDocWeightsForDoc(self, idDoc):
        return self.index.getTfsForDoc(idDoc)

    def getDocWeightsForStem(self, stem):
        return self.index.getTfsForStem(stem)

    def getWeightsForQuery(self, query):
        return self.textRepresenter.getTextRepresentation(query)