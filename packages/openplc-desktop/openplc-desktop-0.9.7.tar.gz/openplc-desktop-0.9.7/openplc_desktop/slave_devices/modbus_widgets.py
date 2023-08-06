# -*- coding: utf-8 -*-

from Qt import QtCore, QtWidgets, Qt, pyqtSignal

from img import Ico

import cwidgets

class MbConfigDialog(QtWidgets.QDialog):

    def __init__(self, parent, serverConn):
        QtWidgets.QDialog.__init__(self, parent)

        assert serverConn != None
        self.serverConn = serverConn

        self.setMinimumWidth(800)
        self.setMinimumHeight(800)


        self.setWindowTitle("mbconfig.cfg")
        self.setWindowIcon(Ico.icon(Ico.mbconfig))

        self.mainLayout = cwidgets.vlayout()
        self.setLayout(self.mainLayout)

        self.txt = QtWidgets.QTextEdit()
        self.mainLayout.addWidget(self.txt)

        self.fetch()

    def fetch(self):

        self.serverConn.get(self, "/modbus-config")


    def on_server_reply(self, reply):
        if reply.busy:
            return
        print(reply)
        self.txt.setPlainText(reply.data['mbconfig'])

