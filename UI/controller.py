import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaOggetti(self, e):
        self._model.creaGrafo()
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato", color="green"))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumNodes()} nodi"))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumEdges()} edges"))
        self._view._btnCompConnessa.disabled = False
        self._view.update_page()

    def handleCompConnessa(self, e):
        idAdded = self._view._txtIdOggetto.value
        try:
            intId = int(idAdded)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Il valore inserito non è un intero!", color="red"))
            self._view.update_page()
            return

        if self._model.checkExistence(intId):
            self._view._txt_result.controls.append(ft.Text(f"L'oggetto con id {intId} è presente nel grafo"))
        else:
            self._view._txt_result.controls.append(ft.Text(f"L'oggetto non è presente nel grafo!", color="red"))

        sizeConnessa = self._model.getConnessa(intId)
        self._view._txt_result.controls.append(
            ft.Text(f"La componente connessa che contiene {intId} ha dimensione {sizeConnessa}"))

        # Fill dd
        self._view._ddLun.disabled = False
        self._view._btnCercaPercorso.disabled = False
        myOptsNum = list(range(2, sizeConnessa))
        myOptsDD = list(map(lambda x: ft.dropdown.Option(x), myOptsNum))
        self._view._ddLun.options = myOptsDD
        # for numero in myOptsNum:
        #     self._view._ddLun.options.append(ft.dropdown.Option(numero))

        self._view.update_page()

    def handleCercaPercorso(self, e):
        path, peso = self._model.getBestPath(int(self._view._ddLun.value), self._model.getObjFromId(int(self._view._txtIdOggetto.value)))
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Percorso trovato con peso uguale a {peso}"))
        self._view._txt_result.controls.append(ft.Text(f"Percorso: "))
        for p in path:
            self._view._txt_result.controls.append(ft.Text(f"{p}"))
        self._view.update_page()


