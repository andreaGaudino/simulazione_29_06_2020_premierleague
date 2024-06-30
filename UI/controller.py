import warnings

import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.mese = None



    def handleCreaGrafo(self, e):
        minuti = self._view.txtMinuti.value
        if minuti == "":
            self._view.create_alert("Minuti non inseriti")
            return
        try:
            minutiInt = int(minuti)
        except ValueError:
            self._view.create_alert("Minuti inseriti non numerici")
            return

        if self.mese is None:
            self._view.create_alert("Mese non inserito")
            return
        self._model.buildGraph(self.mese, minutiInt)
        n,e = self._model.graphDetails()
        self._view.txtGrafo.clean()
        self._view.txtGrafo.controls.append(ft.Text(f"Grafo creato con {n} nodi e {e} archi"))
        self._view.btnConnessioneMax.disabled = False
        self.fillDDMatches(list(self._model.graph.nodes))
        self._view.update_page()




    def handleConnessioneMax(self, e):
        result = self._model.getConnessioneMax()
        self._view.txtConnessione.clean()
        self._view.txtConnessione.controls.append(ft.Text(f"Coppie con connesione massima"))
        for i in result:
            self._view.txtConnessione.controls.append(ft.Text(f"{i[0]} -- {i[1]}  ({i[2]["weight"]})"))
        self._view.update_page()



    def handleCollegamento(self, e):
        self.m1 = int(self._view.ddM1.value)
        self.m2 = int(self._view.ddM2.value)
        if self.m1 is None or self.m2 is None:
            self._view.create_alert("Partite non inserite")
            return
        peso, lista = self._model.cammino(self.m1, self.m2)
        self._view.txtCollegamento.clean()
        self._view.txtCollegamento.controls.append(ft.Text(f"Cammino con peso {peso} di lunghezza {len(lista)-1}"))
        for i in lista:
            self._view.txtCollegamento.controls.append(ft.Text(f"{i}"))
        self._view.update_page()


    def fillDDMese(self):
        mesi = []
        for i in range(1, 13):
            mesi.append(i)
        mesiDD = list(map(lambda x: ft.dropdown.Option(key=x, on_click=self.getMese), mesi))
        self._view.ddMese.options = mesiDD
        self._view.update_page()

    def fillDDMatches(self, nodi):
        nodiDD = list(map(lambda x:ft.dropdown.Option(text=x,key=x.id), nodi))
        self._view.ddM1.options = nodiDD
        self._view.ddM2.options = nodiDD
        self._view.update_page()

    def getMese(self,e):
        if e.control.key is None:
            pass
        else:
            self.mese = e.control.key


           