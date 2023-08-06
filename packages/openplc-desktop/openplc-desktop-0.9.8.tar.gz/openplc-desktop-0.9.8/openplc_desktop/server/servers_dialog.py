# -*- coding: utf-8 -*-

from Qt import QtCore, QtWidgets, Qt, pyqtSignal

import cwidgets
from img import Ico
import G


from server import server_dialog, servers_model

class ServersDialog(QtWidgets.QDialog):

    sigConnect = pyqtSignal(dict)

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self.model = servers_model.ServersModel()


        self.setWindowIcon(Ico.icon(Ico.servers))
        self.setWindowTitle("Servers")

        self.setMinimumWidth(500)
        self.setMinimumHeight(500)

        self.mainLayout = cwidgets.vlayout()
        self.setLayout(self.mainLayout)


        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.mainLayout.addWidget(self.toolbar)

        # Creds

        self.actionAdd = cwidgets.XToolButton(text="Add", ico=Ico.add, callback=self.on_add)
        self.toolbar.addWidget(self.actionAdd)

        self.actionEdit = cwidgets.XToolButton(text="Edit", ico=Ico.edit, callback=self.on_edit)
        self.toolbar.addWidget(self.actionEdit)



        self.actionDelete = cwidgets.XToolButton(text="Delete", ico=Ico.delete, callback=self.on_delete)
        self.toolbar.addWidget(self.actionDelete)


        self.toolbar.addSeparator()
        self.actionConnect = cwidgets.XToolButton(text="Connect", ico=Ico.connect, callback=self.on_connect)
        self.toolbar.addWidget(self.actionConnect)


        self.tree = QtWidgets.QTreeView()
        self.mainLayout.addWidget(self.tree)

        self.tree.setModel(self.model)
        self.tree.doubleClicked.connect(self.on_tree_double)
        self.tree.selectionModel().selectionChanged.connect(self.on_tree_selection)

        self.on_tree_selection()
        self.load()



    def load(self):
       self.model.load()

    def on_tree_double(self):
        self.on_edit()

    def on_tree_selection(self, sel=None, desel=None):
        ena = self.get_rec() is not None
        self.actionDelete.setEnabled(ena)
        self.actionEdit.setEnabled(ena)
        self.actionConnect.setEnabled(ena)


    def get_rec(self):
        sm = self.tree.selectionModel()
        if not sm.hasSelection():
            return
        return self.model.recs[sm.selectedIndexes()[0].row()]
    def on_add(self):
        self.show_edit_dialog()

    def on_edit(self):
        rec = self.get_rec()
        self.show_edit_dialog(rec)

    def show_edit_dialog(self, srv=None):

        dial = server_dialog.ServerDialog(self, server=srv)
        if dial.exec_():
            self.load()

    def on_delete(self):
        sm = self.tree.selectionModel()
        if not sm.hasSelection():
            return

        resp = QtWidgets.QMessageBox.question(self, "Delete ?", "delete server")
        if resp == QtWidgets.QMessageBox.Yes:
            rec = self.model.recs[sm.selectedIndexes()[0].row()]#
            G.settings.remove_server(rec)
            self.load()


    def on_connect(self):
        rec = self.get_rec()
        self.sigConnect.emit(rec)
