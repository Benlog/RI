# -*- coding: utf-8 -*-

import ParserCACM as pars
import TextRepresenter as txtrep

pars = pars.ParserCACM()
pars.initFile("../cacm/cacm.txt")

docs = []


while (True):
    d = pars.nextDocument()
    if d == None:
        break
    docs.append(d)