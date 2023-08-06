




from Qt import QtCore, QtWidgets, Qt, pyqtSignal

import cwidgets
from img import Ico

from users import users_model
from users import user_dialog


class UsersGrid(QtWidgets.QWidget):

    def __init__(self, parent, serverConn=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.serverConn = serverConn
        assert self.serverConn != None

        self.model = users_model.UsersModel(self, serverConn=self.serverConn)
        self.proxyModel = QtCore.QSortFilterProxyModel()
        self.proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxyModel.setSourceModel(self.model)

        self.mainLayout = cwidgets.vlayout()
        self.setLayout(self.mainLayout)

        #===================
        # Toolbar
        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.mainLayout.addWidget(self.toolbar)

        # User Actions
        grp = cwidgets.ToolBarGroup(self, "User Actions")
        self.toolbar.addWidget(grp)

        self.actionAdd = cwidgets.XToolButton(text="Add", ico=Ico.add, callback=self.on_add)
        grp.addWidget(self.actionAdd)

        self.actionEdit = cwidgets.XToolButton(text="Edit", ico=Ico.edit, callback=self.on_edit)
        grp.addWidget(self.actionEdit)
        self.actionEdit.setDisabled(True)


        # ===================
        # Tree
        self.tree = QtWidgets.QTreeView()
        self.mainLayout.addWidget(self.tree)

        self.tree.setModel(self.proxyModel)
        self.tree.setSortingEnabled(True)

        self.tree.selectionModel().selectionChanged.connect(self.on_tree_selection)
        self.tree.doubleClicked.connect(self.on_tree_double_clicked)



        self.statusBar = cwidgets.StatusBar(self)
        self.mainLayout.addWidget(self.statusBar)



    def init_load(self):

        self.fetch()

    def on_refresh(self):
        self.fetch()

    def fetch(self):
        self.model.fetch()



    def on_add(self):
        self.edit_user("new")

    def on_edit(self):
        if not self.tree.selectionModel().hasSelection():
            return

        pidx = self.tree.selectionModel().selectedIndexes()[0]
        sidx = self.proxyModel.mapToSource(pidx)
        tidx = self.model.index(sidx.row(), users_model.C.user_id)
        user_id = self.model.data(tidx, Qt.DisplayRole)
        print(user_id)
        self.edit_user(user_id)

    def edit_user(self, user_id):
        dial = user_dialog.UserDialog(self, serverConn=self.serverConn, user_id=user_id)
        dial.sigSaved.connect(self.on_saved)
        dial.exec_()

    def on_saved(self, rec):
        print(rec)
        ss



    def on_tree_selection(self, sel=None, desel=None):
        self.actionEdit.setEnabled(self.tree.selectionModel().hasSelection())

    def on_tree_double_clicked(self, midx):
        self.on_edit()





