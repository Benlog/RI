# -*- coding: utf-8 -*-

import Evaluation as eva
import ParserCACM as pars
import pandas as pd

class QueryParserCACM(eva.QueryParser):
    def __init__(self, req, jug):
        self.pars = pars.ParserCACM()
        self.pars.initFile(req)
        self.jug = pd.read_csv(jug, delim_whitespace=True, header=None, index_col=False, names=['queryId', 'docId', 'sub-theme', 'score'])


    def nextQuery(self):
        '''
            :return: return a dictionary {'id' : id of the query, 'text' : text of the querry, 'revelent' : {docId : (sub-theme, score)}}
        '''
        __next__()


    def __next__(self):
        q = self.pars.nextDocument()
        return {'id' : q.identifier, 'text' : q.text, 'revelent' : self.jug[self.jug.queryId==5].drop('queryId', axis=1).set_index('docId').to_dict('index')}

    def __iter__(self):
        return self
