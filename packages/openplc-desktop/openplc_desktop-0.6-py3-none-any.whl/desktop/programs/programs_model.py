# -*- coding: utf-8 -*-

from Qt import QtCore, QtWidgets, Qt, pyqtSignal

from img import Ico
import G

class C:
    active = 0
    name = 1
    date_upload = 2
    description = 3
    prog_id = 4

    _count = 5


class ProgramsModel(QtCore.QAbstractTableModel):

    sigLoaded = pyqtSignal()

    def data(self, midx, role):

        rec = self.recs[midx.row()]
        cidx = midx.column()

        if role == Qt.DisplayRole:

            if cidx == C.active:
                return "Yes" if rec["active"] else "-"

            if cidx == C.name:
                return rec["name"]

            elif cidx == C.date_upload:
                return rec['date_upload']

            elif cidx == C.description:
                return rec['description']

            elif cidx == C.prog_id:
                return rec['prog_id']

        if role == Qt.DecorationRole and  cidx == C.name:
            return Ico.icon(Ico.program)



    def __init__(self, parent=None, serverConn=None):
        super(QtCore.QAbstractTableModel, self).__init__()

        assert serverConn != None
        self.serverConn = serverConn

        self.recs = []


    def columnCount(self, pidx=None):
        return C._count

    def rowCount(self, pidx=None):
        return len(self.recs)

    def headerData(self, idx, orientation, role):
        if role == Qt.DisplayRole:
            return ["Active", "Name", "Upload", "Description", "ProgID"][idx]


    def fetch(self):
        self.serverConn.get(self, "/programs")

    def on_server_reply(self, reply):

        if reply.busy:
            return


        self.recs = reply.data['programs']
        self.modelReset.emit()
        self.sigLoaded.emit()

    def upsert(self, rec):
        for idx, r in enumerate(self.recs):
            if r['prog_id'] == rec['prog_id']:
                self.recs[idx] = rec
                self.layoutChanged.emit()
                return
        self.recs.append(rec)
        self.layoutChanged.emit()

