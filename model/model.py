import copy
import random

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph = nx.Graph()
        self.idMap = {}

    def buildGraph(self, mese, minuti):
        self.graph.clear()
        nodi = DAO.getNodi(mese)
        for n in nodi:
            self.graph.add_node(n)
            self.idMap[n.id] = n
        archi = DAO.getArchi(mese, minuti)
        for a in archi:
            self.graph.add_edge(self.idMap[a[0]], self.idMap[a[1]], weight=a[2])

    def getConnessioneMax(self):
        archi = list(self.graph.edges(data=True))
        archi.sort(key=lambda x: x[2]["weight"], reverse=True)
        maxPlayers = archi[0][2]["weight"]
        result = []
        for a in archi:
            if a[2]["weight"] == maxPlayers:
                result.append(a)
        return result

    def cammino(self, m1, m2):
        self.solBest = []
        self.pesoMassimo = 0
        parziale = [self.idMap[m1]]
        self.ricorsione(parziale, self.idMap[m2])
        print(self.pesoMassimo, len(self.solBest))
        return self.pesoMassimo, self.solBest

    def ricorsione(self, parziale, m2):
        vicini = list(self.graph.neighbors(parziale[-1]))
        viciniAmmissibili = self.getAmmissibili(parziale, vicini)
        if parziale[-1] == m2:
            if len(parziale) == 1:
                return
            peso = self.calcolaPeso(parziale)
            if peso>self.pesoMassimo:
                self.pesoMassimo = peso
                self.solBest = copy.deepcopy(parziale)
        else:
            for v in viciniAmmissibili:
                parziale.append(v)
                self.ricorsione(parziale, m2)
                parziale.pop()

    def getAmmissibili(self, parziale, vicini):
        ammissibili = []
        if len(parziale)==1:
            ammissibili = vicini
        else:
            nodo = parziale[-1]
            for v in vicini:
                if v not in parziale and {nodo.home, nodo.away} != {v.home, v.away} :
                    ammissibili.append(v)


        return ammissibili

    def calcolaPeso(self, parziale):
        somma = 0
        for i in range(len(parziale) -1 ):
            somma += self.graph[parziale[i]][parziale[i+1]]["weight"]
        return somma

    def graphDetails(self):
        return len(self.graph.nodes), len(self.graph.edges)