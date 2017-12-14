# -*- coding: utf-8 -*-

import Evaluation as eva
import ParserCACM as pars
import pandas as pd

class QueryParserCACM(eva.QueryParser):
    def __init__(self, req, jug):
        self.pars = pars.ParserCACM()
        pars.initFile(req)
        self.jug = pd.read_csv(jug, delim_whitespace=True, header=None, index_col=False, names=['querryId', 'docId', 'sub-theme', 'score'])
        
    
    def nextQuery(self):
        '''
            :return: return a dictionary {'id' : id of the query, 'text' : text of the querry, 'relevant' : {docId : (sub-theme, score)}}
        '''
        
    
    def __next__(self):
        super().next()