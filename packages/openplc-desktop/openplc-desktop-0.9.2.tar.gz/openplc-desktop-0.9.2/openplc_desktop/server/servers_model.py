# -*- coding: utf-8 -*-

from Qt import QtCore, QtWidgets, Qt, pyqtSignal

from img import Ico
import G

class C:
    name = 0
    address = 1
    login = 2
    autoconnect = 3

    _count = 4


class ServersModel(QtCore.QAbstractTableModel):

    sigLoaded = pyqtSignal()

    def data(self, midx, role):

        rec = self.recs[midx.row()]
        cidx = midx.column()

        if role == Qt.DisplayRole:
            if cidx == C.name:
                return rec["name"]

            elif cidx == C.address:
                return rec['address']

            elif cidx == C.login:
                return rec['login']

            elif cidx == C.autoconnect:
                return rec['auto_connect']

        if role == Qt.DecorationRole and  cidx == C.name:
            return Ico.icon(Ico.server)



    def __init__(self, parent=None):
        super(QtCore.QAbstractTableModel, self).__init__()

        self.recs = []


    def columnCount(self, pidx=None):
        return C._count

    def rowCount(self, pidx=None):
        return len(self.recs)

    def headerData(self, idx, orientation, role):
        if role == Qt.DisplayRole:
            return ["Name", "Address", "Login", "Auto Connect"][idx]


    def load(self):

        self.recs = G.settings.servers_list()
        self.modelReset.emit()