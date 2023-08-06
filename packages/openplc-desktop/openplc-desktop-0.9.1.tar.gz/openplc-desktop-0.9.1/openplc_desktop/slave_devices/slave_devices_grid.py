




from Qt import QtCore, QtWidgets, Qt, pyqtSignal

import cwidgets
from img import Ico

from slave_devices import slave_devices_model, slave_dialog


class SlaveDevicesGrid(QtWidgets.QWidget):



    def __init__(self, parent, serverConn=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.serverConn = serverConn
        assert self.serverConn != None

        self.model = slave_devices_model.SlaveDevicesModel(self, serverConn=self.serverConn)

        self.mainLayout = cwidgets.vlayout()
        self.setLayout(self.mainLayout)



        #===================
        # Toolbar
        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.mainLayout.addWidget(self.toolbar)

        # Actions
        grp = cwidgets.ToolBarGroup(self, "Slave Actions")
        self.toolbar.addWidget(grp)

        self.actionAdd = cwidgets.XToolButton(text="Add", ico=Ico.add, callback=self.on_add)
        grp.addWidget(self.actionAdd)

        self.actionEdit = cwidgets.XToolButton(text="Edit", ico=Ico.edit, callback=self.on_edit)
        grp.addWidget(self.actionEdit)
        self.actionEdit.setDisabled(True)




        self.tree = QtWidgets.QTreeView()
        self.mainLayout.addWidget(self.tree)

        self.tree.setModel(self.model)
        self.tree.doubleClicked.connect(self.on_tree_double)
        self.tree.selectionModel().selectionChanged.connect(self.on_tree_selection)



        self.statusBar = cwidgets.StatusBar(self)
        self.mainLayout.addWidget(self.statusBar)



    def init_load(self):
        self.fetch()

    def on_refresh(self):
        self.fetch()

    def fetch(self):
        self.model.fetch()



    def on_add(self):

        self.show_edit_dialog("new")

    def on_edit(self):
        sm = self.tree.selectionModel()
        if not sm.hasSelection():
            return
        rec = self.model.recs[sm.selectedIndexes()[0].row()]
        self.show_edit_dialog(rec['dev_id'])

    def show_edit_dialog(self, dev_id=None):

        dial = slave_dialog.SlaveDialog(self, dev_id=dev_id, serverConn=self.serverConn)
        dial.sigSaved.connect(self.on_rec_saved)
        dial.exec_()

    def on_rec_saved(self, rec):
        self.model.upsert(rec)



    def on_tree_double(self):
        self.on_edit()

    def on_tree_selection(self, sel=None, desel=None):
        ena = self.tree.selectionModel().hasSelection()
        self.actionEdit.setEnabled(ena)
        #self.actionDelete.setEnabled(ena)