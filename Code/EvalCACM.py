# -*- coding: utf-8 -*-

from Evaluation import QueryParser
from ParserCACM import ParserCACM
import pandas as pd

class QueryParserCACM(QueryParser):
    def __init__(self, req, jug):
        self.pars = ParserCACM()
        self.pars.initFile(req)
        self.jug = pd.read_csv(jug, delim_whitespace=True, header=None, index_col=False, names=['queryId', 'docId', 'sub-theme', 'score'])


    def nextQuery(self):
        '''
            :return: return a dictionary {'id' : id of the query, 'text' : text of the querry, 'revelent' : {docId : (sub-theme, score)}}
        '''
        return self.__next__()


    def __next__(self):
        q = self.pars.nextDocument()
        if q:
            return {'id' : q.identifier, 'text' : q.text, 'revelent' : self.jug[self.jug.queryId==5].drop('queryId', axis=1).set_index('docId').to_dict('index')}
        raise StopIteration()

    def __iter__(self):
        return self
