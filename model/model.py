import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._artObjectList = DAO.getAllObjects()
        self._idMap = {}
        for art in self._artObjectList:
            self._idMap[art.object_id] = art
        self._grafo = nx.Graph()
        self._grafo.add_nodes_from(self._artObjectList)
        self._solBest = []
        self._pesoBest = 0

    def creaGrafo(self):
        self.addEdges()

    def addEdges(self):
        self._grafo.clear_edges()

        # Soluzione1: ciclare sui nodi
        # for u in self._artObjectList:
        #     for v in self._artObjectList:
        #         peso = DAO.getPeso(u, v)
        #         self._grafo.add_edge(u, v, weight=peso)
        # metodo sconsigliato!

        # Soluzione2
        allEdges = DAO.getAllConnessioni(self._idMap)
        for e in allEdges:
            self._grafo.add_edge(e.v1, e.v2, weight=e.peso)

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

    def checkExistence(self, idOggetto):
        return idOggetto in self._idMap

    def getObjFromId(self, idOggetto):
        return self._idMap[idOggetto]

    def getConnessa(self, v0int):
        v0 = self._idMap[v0int]

        # Modo1: successori di v0 in DFS
        successors = nx.dfs_successors(self._grafo, v0)
        allSucc = []
        for v in successors.values():
            allSucc.extend(v)  # funziona come append, ma se aggiungo una lista aggiunge gli elementi della lista
            # singolarmente
        print(f"Metodo 1 (succ): {len(allSucc)}")

        # Modo2: predecessori di v0 in DFS
        predecessors = nx.dfs_predecessors(self._grafo, v0)
        print(f"Metodo 2 (pred): {len(predecessors.values())}")

        # Modo3: conto i nodi dell'albero di visita
        tree = nx.dfs_tree(self._grafo, v0)
        print(f"Metodo 3 (tree): {len(tree.nodes())}")

        # Modo4: node_connected_component
        connComp = nx.node_connected_component(self._grafo, v0)
        print(f"Metodo 4 (ncc): {len(connComp)}")

        return len(connComp)

    def getBestPath(self, lun, v0):
        self._solBest = []
        self._pesoBest = 0

        parziale = [v0]

        for v in self._grafo.neighbors(v0):
            if v.classification == v0.classification:
                parziale.append(v)
                self.ricorsione(parziale, lun)
                parziale.pop()

        return self._solBest, self._pesoBest

    def ricorsione(self, parziale, lun):
        # Controllo se parziale è una sol valida, e in caso se è migliore del best
        if len(parziale) == lun:
            if self.peso(parziale) > self._pesoBest:
                self._pesoBest = self.peso(parziale)
                self._solBest = copy.deepcopy(parziale)
            return

        # Se arrivo qui, allora len(parziale) < lun
        for v in self._grafo.neighbors(parziale[-1]):
            # v lo aggiungo se non è già in parziale e se ha stessa classification di v0
            if v.classification == parziale[-1].classification and v not in parziale:
                parziale.append(v)
                self.ricorsione(parziale, lun)
                parziale.pop()

    def peso(self, listObject):
        p = 0
        for i in range(0, len(listObject) - 1):
            p += self._grafo[listObject[i]][listObject[i + 1]]["weight"]
        return p


