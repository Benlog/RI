# -*- coding: utf-8 -*-

class Weighter(object):

    def __init__(self, index):
        self.index = index

    def getDocWeightsForDoc(self, idDoc):
        return self.index.getTfsForDoc(idDoc)

    def getDocWeightsForStem(self, stem):
        return self.index.getTfsForStem(stem)

    def getWeightsForQuery(self, query):
        return self.index.textRepresenter.getTextRepresentation(query)