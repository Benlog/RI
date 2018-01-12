# coding: utf-8

import pandas as pd


class QueryParser(object):
    """
        QueryParser

        Permet de charger des requêtes de recherche d'informations pré-définies.
    """

    def __init__(self, parser, req, jug):
        """
            Crée un objet QueryParser

            :param parser: Parseur
            :param req: Fichier de requêtes
            :param jug: Fichier de jugements
        """
        self.pars = parser
        self.pars.initFile(req)
        self.jug = pd.read_csv(jug, delim_whitespace=True, header=None, index_col=False, names=['queryId', 'docId', 'sub-theme', 'score'], dtype={'queryId' : str, 'docId' : str}, converters={'queryId' : lambda x : str(int(x))})


    def nextQuery(self):
        '''
            Renvoie la requête (query) suivante.

            Une requête est présentée sous la forme d'un dictionnaire contenant les trops champs suivants :
            - id : identifiant de la requête
            - text : contenu de la requête (termes recherchés)
            - relevant : dictionnaire contenant une liste de documents associés à un sous-thème et un score

            :return: Requête suivante
            :rtype:  dict
        '''
        q = self.pars.nextDocument()
        if q:
            return {
                'id' : q.identifier,
                'text' : q.text,
                'revelent' : self.jug[self.jug.queryId==q.getId()].drop('queryId', axis=1).set_index('docId').to_dict('index')}
        raise StopIteration()


    def __next__(self):
        self.nextQuery()


    def __iter__(self):
        return self
