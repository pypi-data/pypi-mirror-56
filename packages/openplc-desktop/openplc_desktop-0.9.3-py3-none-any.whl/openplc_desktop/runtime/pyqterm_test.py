

import sys

# Import from here...
# another fork to fix things,, https://pyqtx.gitlab.io/pyqtermwidget/

sys.path.append("/home/oplc/pyqtermwidget/")


# -*- coding: utf-8 -*-

from Qt import QtCore, QtWidgets, QtNetwork, Qt, pyqtSignal

from img import Ico

import cwidgets

import pyqterm


class PyQTermWidget(QtWidgets.QWidget):

    def __init__(self, parent, serverConn=None):
        QtWidgets.QWidget.__init__(self, parent)

        assert serverConn != None
        self.serverConn = serverConn





        self.mainLayout = cwidgets.vlayout()
        self.setLayout(self.mainLayout)

        self.toolbar = cwidgets.XToolBar()
        self.mainLayout.addWidget(self.toolbar)

        ## ------------ credentials
        grp = cwidgets.ToolBarGroup(title="Terminal")
        self.toolbar.addWidget(grp)

        self.txtHost = cwidgets.XLineEdit()
        grp.addWidget(self.txtHost)
        self.txtHost.setText("192.168.1.222")
        self.txtHost.setMaximumWidth(120)

        self.spinPort = QtWidgets.QSpinBox()
        grp.addWidget(self.spinPort)
        self.spinPort.setValue(22)

        self.txtUser = cwidgets.XLineEdit()
        grp.addWidget(self.txtUser)
        self.txtUser.setText("pi")
        self.txtUser.setMaximumWidth(80)

        self.txtPass = cwidgets.XLineEdit()
        grp.addWidget(self.txtPass)
        self.txtPass.setText("raspberry")
        self.txtPass.setMaximumWidth(80)

        #self.buttConnect = cwidgets.XToolButton(ico=Ico.start, text="Connect", callback=self.on_connect)
        #grp.addWidget(self.buttConnect)

        self.lblStatus = cwidgets.XLabel()
        grp.addWidget(self.lblStatus)



        ## ------------ send command
        grp = cwidgets.ToolBarGroup(title="Execute")
        self.toolbar.addWidget(grp)

        self.txtCommand = cwidgets.XLineEdit()
        grp.addWidget(self.txtCommand)
        self.txtCommand.setText("ls -l")
        #self.txtCommand.returnPressed.connect(self.on_execute)

        #self.buttConnect = cwidgets.XToolButton(ico=Ico.return_key, text="Execute", callback=self.on_execute)
        #grp.addWidget(self.buttConnect)



        self.terminal = pyqterm.TerminalWidget(self)
        self.mainLayout.addWidget(self.terminal)



    def init_load(self):
        pass
