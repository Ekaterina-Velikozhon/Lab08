import flet as ft

from UI.view import View
from model.model import Model
from model.nerc import Nerc


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()


    def handleWorstCase(self, e):
        self._view._txtOut.controls.clear()

        nerc = self._idMap.get(self._view._ddNerc.value)

        if  nerc is None or self._view._txtYears.value == "" or self._view._txtHours.value == "":
            self._view.create_alert("Manca qualche dato!")
            return

        years = int(self._view._txtYears.value)
        hours = int(self._view._txtHours.value)
        sol_best, num_customer_max, ore = self._model.worstCase(nerc, years, hours)
        self._view._txtOut.controls.append(ft.Text(f"Tot people affected: {num_customer_max}"))
        self._view._txtOut.controls.append(ft.Text(f"Tor hours of outage: {ore}"))
        for evento in sol_best:
            self._view._txtOut.controls.append(ft.Text(evento))
        self._view.update_page()

    def fillDD(self):
        nercList = self._model.listNerc #getter!!

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(text=n.value,
                                                                 data=n, #associa l'oggetto all'opzione
                                                                 on_click=self.readDD))
            self._view.update_page()

    def readDD(self,e):
        print(e.control.data)

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
