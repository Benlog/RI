# coding: utf-8

import time
import logging as log


class Index(object):
    """
        Index

        Objet construisant et conservant les index et index inversé d'un corpus textuel.
    """

    def __init__(self, name, parser, textRepresenter, source, keep_alive=False):
        """
            Initialise un objet Index

            :param name: Nom de l'index
            :param parser: Parseur à utiliser
            :param textRepresenter: Représentation du corpus
            :param source: Corpus à indexer
            :param keep_alive: Indique s'il faut conserver l'index en mémoire vive
            :type name: str
            :type parser: Parser
            :type textRep: TextRepresenter
            :type source: str
            :type keep_alive: bool
        """

        self.name = name
        self.docs = {}
        self.stems = {}
        self.docFrom = {}
        self.parser = parser
        self.textRepresenterresenter = textRepresenter
        self.source = source
        self.keep_alive = keep_alive

        if self.keep_alive:
            self.index = {}

    def writeDict(self, dic):
        """
            Convertit un dictionnaire en une chaîne de caractères

            Cette fonction est utilisée lors de la sauvegarde sur disque d'un
            dictionnaire. Il est aussi possible d'écrire le dictionnaire
            directement, et de le lire ensuite à l'aide de la fonction native
            eval, de sa version sécurisée ast.literal_eval, ou en parsant
            le dictionnaire à l'aide du paquet json, ou encore en utilisant
            la sérialisation pickle.

            L'intér¤t de cette fonction est de proposer une sérialisation des
            dictionnaires la moins verbeuse possible, et dans un seul et m¤me
            fichier, ce qui sert l'objectif principal de performance visé ici.

            :param dic: Un dictionnaire à sérialiser
            :type dic: dict
            :return: Représentation en cha→ne de caractères du dictionnaire
            :rtype: str
        """

        return ';'.join([w + ":" + str(n) for w, n in dic.items()]).encode()

    def readDict(self, b):
        """
            Convertit une cha→ne de caractères en dictionnaire

            Convertit en dictionnaire python une cha→ne de caractères produite
            par la fonction Index.writeDict()

            .. seealso:: writeDict()

            :param b: Cha→ne à convertir
            :type b: str
            :return: Dictionnaire lu
            :rtype: dict
        """

        return {w: int(n) for w, n in [s.split(':') for s in b.decode().split(';')]}


    def indexation(self):
        """
            Effectue l'indexation du corpus
        """

        log.info("Création de l'index " + self.name + "\n\n")
        log_start = time.time()

        self.indexDirect()
        self.indexInversed()
        self.indexHyperLinks()

        log.info("\nIndex créé en " + str(time.time() - log_start) + " secondes.\n")
        log.info(str(len(self.docFrom)) + " documents et " + str(len(self.stems)) + " mots ont été indexés.\n")


    def indexDirect(self):
        """
            Effectue l'indexation normale du corpus
        """

        with open("./" + self.name + "_index", "wb") as ifile:
            ifcur = 0

            # Pour chaque document
            self.parser.initFile(self.source)
            d = self.parser.nextDocument()

            # Logging
            log_size = self.parser.countDocument()
            log_accu = 0

            while (d):

                # Lecture document
                id = d.getId()
                st = self.textRepresenter.getTextRepresentation(d.getText())

                # Écriture table DocFrom
                dfp, dfb, dfl = d.get("from").split(";")
                self.docFrom[id] = (dfp, int(dfb), int(dfl))

                # Initialisation stems
                for s, v in st.items():
                    log.debug("Stem : " + s)
                    spv = self.stems.get(s, (0, 0))[1]
                    self.stems[s] = (-1, spv + len(id + str(v)) + 2)

                # Écriture index
                ifile.write(self.writeDict(st))
                ifile.write("\n".encode())
                nfcur = ifile.tell()
                self.docs[id] = (ifcur, nfcur - ifcur)

                # Écriture hyperliens
                links = document.get('links').split(';')[:-1]
                if links:
                    lfile.write(docid + ":" + ";".join(links) + "\n")

                # Itération
                ifcur = nfcur
                d = self.parser.nextDocument()

                # Live version (deprecated)
                if self.keep_alive:
                    self.index[id] = st

                # Logging
                log_accu += 1
                log_perc = log_accu/log_size
                log.info("\rIndexation normale [" + "█"*int(50*log_perc) + " "*(50-int(50*log_perc)) + "] " + str(int(100*log_perc)) + "%")
                log.debug("Document : " + id)

            log.info("\b" * 4 + "\033[1;32mTerminé\033[0m\n")


    def indexInversed(self):
        """
            Indexation inversée
        """

        with open("./" + self.name + "_index", "rb") as wfile:
            with open("./" + self.name + "_inverted", "wb") as ifile:

                # Préparation
                offset = 0
                for s, (o, l) in self.stems.items():
                    self.stems[s] = (offset, l)
                    offset += l

                curs = dict.fromkeys(self.stems, 0)

                # Logging
                log_size = len(self.docs)
                log_accu = 0

                for s, (o, l) in self.docs.items():

                    # Logging
                    log_accu+= 1
                    per = log_accu/log_size
                    log.info("\rIndexation inverse [" + "█"*int(50*per) + " "*(50-int(50*per)) + "] " + str(int(100*per)) + "%")

                    # Lecture index
                    if self.keep_alive:
                        st = self.index[s]
                    else:
                        wfile.seek(o)
                        st = self.readDict(wfile.read(l))

                    # Ecriture doc-tf
                    for ss, (sd, sl) in self.stems.items():
                        if st.get(ss):
                            w = sd + ':' + st[ss] + ';'
                            ifile.seek(sd + curs[ss])
                            curs[ss] += len(w)
                            ifile.write(w.encode())

                # Finalisation index (rempalce dernier ; par \name)
                for ss, (sd, sl) in self.stems.items():
                    ifile.seek(sd + sl - 1)
                    ifile.write("\n".encode())

                log.info("\b" * 4 + "\033[1;32mTerminé\033[0m\n")


    def indexHyperLinks(self, document, file):
        """
            Indexation des hyperliens
        """
        with open("./" + self.name + "_links", "wb") as lfile:
            for document in self.docs.keys():
                docid = document.getId()
                links = document.get('links').split(';')[:-1]
                if links:
                    lfile.write(docid + ":" + ";".join(links) + "\n")


    def getTfsForDoc(self, doc):
        """
            Retourne la représentation stem-tf d'un document depuis l'index

            Retrouve un document déjà indexé par son identifiant, et renvoie un
            dictionnaire contenant tous les stems du document respectivement
            associés à leurs nombres d'apparition dans celui-ci.

            :param doc: Identifiant du document
            :type doc: str
            :return: Représentation stem-tf
            :rtype: dict
        """
        ifile = open("./" + self.name + "_index", "rb")
        ifile.seek(self.docs[doc][0])
        return self.readDict(ifile.read1(self.docs[doc][1]))


    def getTfsForStem(self, stem):
        """
            Retourne la représentation doc-tf d'un stem depuis l'index

            Pour un stem déjà indexé donné, retourne un dictionnaire contenant
            l'identifiant de tous les documents dans lequel il apparait,
            associés au nombre d'apparition du stem dans chacun de ces
            documents.

            :param stem: Stem recherché
            :type stem: str
            :return: Représentation doc-tf
            :rtype: dict
        """
        ifile = open("./" + self.name + "_inverted", "rb")
        try:
            ifile.seek(self.stems[stem][0])
            dic = self.readDict(ifile.read1(self.stems[stem][1]))
        except KeyError:
            dic = dict()
        return dic


    def getStrDoc(self, doc):
        """
            Retourne le texte brut d'un document

            Retourne le texte brut d'un document tel qu'il existe dans les
            fichiers sources indexés.

            :param doc: Document recherché
            :type doc: str
            :return: Texte brut du document
            :rtype: str
        """
        f = open(self.docFrom[0], "rb")
        f.seek(self.docFrom[1])
        return f.read1(self.docFrom[2])
