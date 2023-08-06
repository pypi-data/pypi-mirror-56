# -*- coding: utf-8 -*-

import os
import sys


from Qt import QtCore, QtWidgets, Qt, pyqtSignal

import G
import cwidgets
from img import Ico

from server import server_dialog, server_panel, servers_dialog
from help import help_widgets

class MainWindow(QtWidgets.QWidget):

    def on_after(self):


        if os.path.exists("PEDRO.txt"):
            pass #QtCore.QTimer.singleShot(300, self.maximizeWindow)

        self.init_help()

        for srv in G.settings.servers_list():
            if srv['auto_connect']:
                self.open_server(srv)

    def __init__(self, parent=None, args=None):
        QtWidgets.QWidget.__init__(self, parent)

        G.args = args

        self.setWindowTitle("OpenPLC Desktop")
        self.setWindowIcon(Ico.logo())

        self.mainLayout = cwidgets.vlayout()
        self.setLayout(self.mainLayout)

        # menu
        self.menuBar = QtWidgets.QMenuBar()
        self.mainLayout.addWidget(self.menuBar)

        self.menuFile = QtWidgets.QMenu("File")
        self.menuBar.addMenu(self.menuFile)

        self.menuFile.addAction(Ico.icon(Ico.quit), "Quit", self.on_quit)


        self.menuServers = QtWidgets.QMenu("Servers")
        self.menuBar.addMenu(self.menuServers)

        self.menuServers.addAction(Ico.icon(Ico.servers), "Servers", self.on_servers)

        self.menuServers.addSeparator()
        self.menuServers.addAction(Ico.icon(Ico.add), "Add Server", self.on_add_server)


        ## Top toolbar
        self.topToolbar = cwidgets.hlayout()
        self.mainLayout.addLayout(self.topToolbar, 0)

        self.lblHeader = QtWidgets.QLabel()
        self.topToolbar.addWidget(self.lblHeader, 10)
        self.lblHeader.setText("OpenPLC")
        style_grad = "background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #444444, stop: 1 #D95343);"
        style_grad += "font-size: 18pt; color: #efefef; padding: 5px 10px;"
        self.lblHeader.setStyleSheet(style_grad)

        self.buttAddServer = cwidgets.XToolButton(self, text="Add Server", ico=Ico.add, callback=self.on_add_server)
        self.topToolbar.addWidget(self.buttAddServer)

        if 1:
            self.devToolbar = QtWidgets.QToolBar()
            self.mainLayout.addWidget(self.devToolbar)

            self.buttNoNo = QtWidgets.QPushButton()
            self.buttNoNo.setText("Magic Button")
            self.buttNoNo.setToolTip("Though shalt not click this button before 6am gmt")
            self.devToolbar.addWidget(self.buttNoNo)
            self.buttNoNo.clicked.connect(self.on_nono_clicked)



        tlay = cwidgets.hlayout()
        self.mainLayout.addLayout(tlay)
        self.tabBar = QtWidgets.QTabBar()
        tlay.addWidget(self.tabBar, 0)
        tlay.addStretch(5)

        self.appStack = QtWidgets.QStackedWidget()
        self.mainLayout.addWidget(self.appStack, 20)


        self.helpWidget = None



        if 0:
            self.serverPanel = server_panel.ServerPanel()
            self.add_widget(self.serverPanel, "Server", Ico.server)

        if G.args.pedro:
            self.move(1800, 20)
            self.setMinimumWidth(600)
            self.setMinimumHeight(600)
            self.setWindowState(Qt.WindowMaximized)

        self.tabBar.currentChanged.connect(self.on_tab_changed)

        ## dev mode so switch to wizz
        # self.tabBar.setCurrentIndex(1)

        QtCore.QTimer.singleShot(200, self.on_after)

    def add_widget(self, widget, text, ico=None):
        self.appStack.addWidget(widget)
        idx = self.tabBar.addTab(text)
        if ico:
            self.tabBar.setTabIcon(idx, Ico.icon(ico))

        widget.init_load()

    def on_tab_changed(self, nidx):
        self.appStack.setCurrentIndex(nidx)

    def on_nono_clicked(self):
        print("panic")
        self.appStack.widget(0).load_data()

    def on_bank_holiday_clicked(self):
        print("on_bank_holiday", self)

    def on_add_server(self, autologin=False):

        dial = server_dialog.ServerDialog(self)
        dial.sigSaved.connect(self.on_server_saved)
        dial.exec_()

    def on_server_saved(self, server):

        if server:
            s = "%s\n%s" % (user['username'], user['email'])
            self.lblLogin.setText(s)

    def on_quit(self):
        sys.exit(0)

    def on_servers(self):

        dial = servers_dialog.ServersDialog(self)
        dial.exec_()

    def open_server(self, srv):

        widget = server_panel.ServerPanel(server=srv)
        self.add_widget(widget, srv['name'],ico=Ico.server)


    def init_help(self):
        hw = help_widgets.HelpWidget(self)
        self.add_widget(hw, "Help", Ico.help)