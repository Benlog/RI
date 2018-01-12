# coding: utf-8

import logging  as log
import networkx as nx
import numpy    as np


class RandomWalker(object):
    """
        Random Walker

        Classe abstraite de marche aléatoire dans un graphe.
    """

    def __init__(self, max_iters=100, hyperlinks=None):
    	"""
			Initie un marcheur aléatoire sur graphe

			:param max_iters:  Nombre maximal de pas de la marche aléatoire
			:param hyperlinks: Fichier d'index des hyperliens
    	"""
    	self.max_iters = max_iters
    	self.g = nx.DiGraph()
    	if hyperlinks:
    		load(hyperlinks)

    	log.info("%s instancié", self.__class__.__name__)

    def load(self, hyperlinks):
    	"""
			Charge un fichier d'index d'hyperliens
    	"""
    	if Path(hyperlinks).is_file():
    		self.g = nx.DiGraph()
	    	with open(hyperlinks, "rb") as ifile:
	    		for line in ifile.readlines():
	    			doc, links = line.split(":")
	    			doc = int(doc)
	    			for link in links.split(";"):
	    				self.g.add_edge(doc, int(link))
	    	log.debug("%d documents et %d hyperliens chargés", len(self.g), self.g.size())
	    else:
	    	log.error("Erreur lors de l'ouverture du fichier %s", hyperlinks)



    def score(self, graph):
    	"""
			Calcule le score des documents

			Applique un algorithme de marche aléatoire sur un graphe de
			documents (le graphe entier par défaut, ou un sous-graphe spécifié)
			et retourne la liste des documents associés à leurs scores.

			:param graph: Graphe à parcourir

			:return: Dictionnaire associant à chaque document son score
			:rtype:  dict
    	"""
    	raise NotImplementedError()



    def getScores(self, subset=None):
    	"""
			Retourne le score des documents

			Utilise la fonction score() pour calculer le score des documents.

			.. seealso:: score()

			:param subset: Documents à parcourir (graphe entier par défaut)
			:type  subset: list
    	"""
		if subset:
			g = self.g.subgraph(subset)
		else:
			g = self.g

		return score(iterations, g)


class PageRank(RandomWalker):
	"""
		PageRank Random Walker
	"""

	def score(self, graph):
		return nx.pagerank(graph, max_iter=self.max_iter)


class HITS(RandomWalker):
	"""
		HITS Random Walker
	"""

	def score(self, graph):
		return nx.hits(graph, max_iter=self.max_iter)


class RandomWalkerModel(IRmodel):
	"""
		Modèle de recherche utilisant l'algorithme PageRank

		Utilise un autre modèle de recherche afin de produire des résultats
		préliminaires, avant d'appliquer l'algorithme PageRank sur un
		sous-graphe des documents basé sur les résultats du premier modèle.
	"""

	def __init__(self, model, rwalk, ndocs, kdocs):
		"""
			Initialise le modèle PageRank

			:param model: Modèle de recherche de base
			:param rwalk: Marcheur aléatoire
			:param ndocs: Nombre de résultats du modèle de base à retenir
			:param kdocs: Nombre d'antécédants à retenir
		"""
		self.model = model
		self.rwalk = rwalk
		self.ndocs = ndocs
		self.kdocs = kdocs


	def getScores(self, query, normalized=True):

		# Sélection des n premiers résultats du modèle de base
		results = [r for (r, s) in self.model.getRanking(query)[:self.ndocs]]

		# Ajouts documents accessibles et antécédents
		successors   = []
		predecessors = []
		for d in docs:
			successors   += self.rwalk.g.sucessors(d)
			predecessors += self.rwalk.g.predecessors(d)

		# Choix des documents à explorer
		np.random.shuffle(predecessors)
		subset = results + successors + predecessors[:kdocs]

		# Marche aléatoire
		return self.rwalk.getScores(subset)

