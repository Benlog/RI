# -*- coding: utf-8 -*-

class QueryParser(object):
    def __init__(self, req, jug):
        pass
    
    def nextQuery(self):
        '''
            :return: return a dictionary {'id' : id of the query, 'text' : text of the querry, 'relevant' : {docId : (sub-theme, score)}}
        '''
        pass
    
    def __next__(self):
        super().next()