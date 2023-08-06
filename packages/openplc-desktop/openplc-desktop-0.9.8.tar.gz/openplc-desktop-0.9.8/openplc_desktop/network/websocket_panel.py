

import datetime


from Qt import QtCore, QtGui, QtWidgets, Qt, pyqtSignal

import cwidgets
from img import Ico




class WebSocketPanel(QtWidgets.QWidget):



    def __init__(self, parent=None, serverConn=None):
        QtWidgets.QWidget.__init__(self, parent)


        self.serverConn = serverConn


        self.mainLayout = cwidgets.vlayout()
        self.setLayout(self.mainLayout)


        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.mainLayout.addWidget(self.toolbar)

        # # Actions
        self.tbActions = cwidgets.ToolBarGroup(self, title="Actions")
        self.toolbar.addWidget(self.tbActions)
        #
        # self.lblServerName = cwidgets.XLabel()
        # self.lblServerName.setFixedWidth(160)
        # self.tbServer.addWidget(self.lblServerName)
        #
        # self.lblServerStatus = cwidgets.XLabel()
        # self.lblServerStatus.setFixedWidth(160)
        # self.tbServer.addWidget(self.lblServerStatus)
        #
        self.buttClear = cwidgets.XToolButton(self, ico=Ico.clear, text="Clear", callback=self.on_clear)
        self.tbActions.addWidget(self.buttClear)
        #
        # self.buttWs = cwidgets.XToolButton(self, ico=Ico.save, both=False, callback=self.on_ws)
        # self.tbServer.addWidget(self.buttWs)

        self.model = WebSocketModel(serverConn=serverConn)

        #self.proxy = QtCore.QSortFilterProxyModel()
        #self.proxy.setSourceModel(self.model)


        ## Midx widgets
        self.tree = QtWidgets.QTreeView()
        self.mainLayout.addWidget(self.tree)

        self.tree.setModel(self.model)

        for c in [C.ts, C.ns, C.mtype]:
            self.tree.setColumnHidden(c, True)

        #self.tree.sortByColumn(C.ts, Qt.DescendingOrder)




    def init_load(self):

        # self.fetch()
        #self.on_login()
        pass

    def on_clear(self):
        self.model.clear()

class C:
    ts = 0
    ns = 1
    mtype = 2
    data = 3

    _count = 4


class WebSocketModel(QtCore.QAbstractTableModel):

    sigLoaded = pyqtSignal()

    def data(self, midx, role):

        rec = self.recs[midx.row()]
        cidx = midx.column()

        if role == Qt.DisplayRole:
            if cidx == C.ns:
                return rec['ns']

            elif cidx == C.mtype:
                return rec['mtype']

            elif cidx == C.data:
                return rec['data']

            elif cidx == C.ts:
                return rec['ts']

    def clear(self):
        del self.recs[:]
        self.layoutChanged.emit()


    def __init__(self, parent=None, serverConn=None):
        super(QtCore.QAbstractTableModel, self).__init__()

        assert serverConn != None
        self.serverConn = serverConn
        self.recs = []

        self.serverConn.sigWsMessage.connect(self.on_ws_message)

    def on_ws_message(self, recs):
        for r in recs:
            self.recs.append(r)
        self.layoutChanged.emit()


    def columnCount(self, pidx=None):
        return C._count

    def rowCount(self, pidx=None):
        return len(self.recs)

    def headerData(self, idx, orientation, role):
        if role == Qt.DisplayRole:
            return ["ts", "Ns", "Type", "Data"][idx]

