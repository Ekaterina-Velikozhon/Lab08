import copy

from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._clientiMaxBest = 0
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()

        #Aggiunto da me
        self.totHours = 0


    def worstCase(self, nerc, maxY, maxH):
        self.loadEvents(nerc)
        eventi = self._listEvents
        self._solBest = []
        self._totalHours = 0
        self._clientiMaxBest = 0 # perchè quando richiamo questo metodo per altro nerc e Y,H -> devo azzerare tutti i valori precedenti!!
        self._ricorsione([], maxY, maxH, 0, eventi)

        return self._solBest, self._clientiMaxBest, self.totHours

    def _ricorsione(self, parziale, maxY, maxH, pos, eventi):
        ore = self.getOreMax(parziale)
        if ore <= maxH:
            n_customers = self.countCostomers(parziale)
            if n_customers > self._clientiMaxBest:
                self._solBest = copy.deepcopy(parziale)
                self._clientiMaxBest = n_customers
                self.totHours = ore

        for i in range(pos, len(eventi)):
            evento = eventi[i]
            if self._is_admisible(parziale, evento, maxY):
                parziale.append(evento)
                self._ricorsione(parziale, maxY, maxH, i + 1, eventi)
                parziale.pop()

    def _is_admisible(self, parziale, evento, maxY):
        if len(parziale) < 2:
            return True

        parziale_n = parziale + [evento]
        if self.getAnniMax(parziale_n) > maxY:
            return False

        return True

    def countCostomers(self, parziale):
        if len(parziale) == 0:
            return 0

        num_customers = 0
        for evento in parziale:
            num_customers += evento.customers_affected
        return num_customers

    def getAnniMax(self, parziale):
        if len(parziale) < 2:
            return 0

        evento_last = parziale[-1].date_event_finished
        evento_first = parziale[0].date_event_began
        anni_tot = int(evento_last.year - evento_first.year)
        return anni_tot

    def getOreMax(self, parziale):
        if len(parziale) == 0: #non ci sono eventi selezionati
            return 0

        ore_tot = 0
        for evento in parziale:
            durata_ore = ((evento.date_event_finished - evento.date_event_began).total_seconds()) / 3600
            ore_tot += durata_ore
        return ore_tot

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()

    @property
    def listNerc(self):
        return self._listNerc