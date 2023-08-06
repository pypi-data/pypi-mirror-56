# -*- coding: utf-8 -*-

import os
import sys


from Qt import QtCore, QtWidgets, Qt, pyqtSignal

import G
import cwidgets
from img import Ico


from server import server_dialog, server_panel, servers_dialog
from help import help_widgets
from runtime import ini_editor

class MainWindow(QtWidgets.QWidget):

    def on_after(self):

        self.on_help()

        inied = ini_editor.INIEditorWidget(self)
        self.add_widget(inied, "INI")


        for srv in G.settings.servers_list():
            #if srv['auto_connect']:
            #    self.open_server(srv)
            pass

    def __init__(self, parent=None, args=None):
        QtWidgets.QWidget.__init__(self, parent)

        G.args = args

        self.setWindowTitle("⊣OpenPLC⊢ Desktop")
        self.setWindowIcon(Ico.logo())

        self.mainLayout = cwidgets.vlayout()
        self.setLayout(self.mainLayout)

        # menu
        self.menuBar = QtWidgets.QMenuBar()
        self.mainLayout.addWidget(self.menuBar)

        self.menuFile = QtWidgets.QMenu("File")
        self.menuBar.addMenu(self.menuFile)

        self.menuFile.addAction(Ico.icon(Ico.quit), "Quit", self.on_quit)

        #== servers menu
        self.menuServers = QtWidgets.QMenu("Servers")
        self.menuBar.addMenu(self.menuServers)


        self.actServers = self.menuServers.addAction(Ico.icon(Ico.servers), "Servers", self.on_servers_dialog)

        self.menuServers.addSeparator()
        self.actAddServer = self.menuServers.addAction(Ico.icon(Ico.add), "Add Server", self.on_add_server)

        # == help menu
        self.menuHelp = QtWidgets.QMenu("Help")
        self.menuBar.addMenu(self.menuHelp)

        self.actHelp = self.menuHelp.addAction(Ico.icon(Ico.help), "Help", self.on_help)



        ## Top toolbar
        self.topToolbar = cwidgets.hlayout()
        self.mainLayout.addLayout(self.topToolbar, 0)

        #self.buttAddServer = cwidgets.XToolButton(self, text="Add Server", ico=Ico.add, callback=self.on_add_server)
        #self.topToolbar.addWidget(self.buttAddServer)

        self.topTB = QtWidgets.QToolBar()
        self.topTB.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.topToolbar.addWidget(self.topTB)

        self.buttConnect = cwidgets.XToolButton(ico=Ico.connect, text="Connect", popup=True)
        self.buttConnect.setMenu(QtWidgets.QMenu())
        self.buttConnect.menu().aboutToShow.connect(self.on_load_server_to_menu)
        self.buttConnect.menu().triggered.connect(self.on_connect_action)

        self.topTB.addWidget(self.buttConnect)
        self.topTB.addAction(self.actServers)
        self.topTB.addAction(self.actAddServer)



        self.lblHeader = QtWidgets.QLabel()
        self.lblHeader.setAlignment(Qt.AlignRight)
        self.topToolbar.addWidget(self.lblHeader, 10)
        self.lblHeader.setText("⊣OpenPLC⊢")
        style_grad = "background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #444444, stop: 0.2 #D95343, stop: 1 #444444);"
        style_grad += "font-size: 14pt; color: #efefef; padding: 3px 10px 0 0;"
        self.lblHeader.setStyleSheet(style_grad)



        if 1:
            self.devToolbar = QtWidgets.QToolBar()
            self.mainLayout.addWidget(self.devToolbar)

            self.buttNoNo = QtWidgets.QPushButton()
            self.buttNoNo.setText("Magic Button")
            self.buttNoNo.setToolTip("Though shalt not click this button before 6am gmt")
            self.devToolbar.addWidget(self.buttNoNo)
            self.buttNoNo.clicked.connect(self.on_nono_clicked)


        ## Central tabs
        tlay = cwidgets.hlayout()
        self.mainLayout.addLayout(tlay)

        self.tabBar = QtWidgets.QTabBar()
        self.tabBar.setTabsClosable(True)
        tlay.addWidget(self.tabBar, 0)
        tlay.addStretch(5)

        self.appStack = QtWidgets.QStackedWidget()
        self.mainLayout.addWidget(self.appStack, 20)






        if G.args.pedro:
            self.move(1800, 20)
            self.setMinimumWidth(600)
            self.setMinimumHeight(600)
            self.setWindowState(Qt.WindowMaximized)
        else:
            self.setWindowState(Qt.WindowMaximized)

        self.tabBar.currentChanged.connect(self.on_tab_changed)
        self.tabBar.tabCloseRequested.connect(self.on_tab_close_requested)
        QtCore.QTimer.singleShot(200, self.on_after)

    def add_widget(self, new_widget, text, ico=None, prop=None, val=None):

        if prop is not None:
            new_widget.setProperty(prop, val)

        self.appStack.addWidget(new_widget)
        idx = self.tabBar.addTab(text)
        if ico:
            self.tabBar.setTabIcon(idx, Ico.icon(ico))
        self.tabBar.setCurrentIndex(idx)
        new_widget.init_load()

    def get_widget_index(self, xtype, prop=None, val=None):

        for idx in range(0, self.appStack.count()):
            xwidget = self.appStack.widget(idx)
            if isinstance(xwidget, xtype):
                if prop:
                    v = xwidget.property(prop)
                    if v != None and v == val:
                        return idx
                    continue
                return idx
        return None

    def on_tab_changed(self, nidx):
        self.appStack.setCurrentIndex(nidx)

    def on_tab_close_requested(self, idx):
        widget = self.appStack.widget(idx)
        if isinstance(widget, server_panel.ServerPanel):
            mbox = QtWidgets.QMessageBox
            resp = mbox.question(self, "Close connection", "Will close any connections to this server")
            if resp != mbox.Yes:
                return
            widget.close_all()
        self.tabBar.removeTab(idx)
        self.appStack.removeWidget(widget)

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

    def on_servers_dialog(self):
        dial = servers_dialog.ServersDialog(self)
        dial.sigConnect.connect(self.open_server)
        dial.exec_()

    def open_server(self, srv):
        idx = self.get_widget_index(server_panel.ServerPanel, prop="srv", val=srv['address'])
        if idx is None:
            widget = server_panel.ServerPanel(server=srv)
            self.add_widget(widget, srv['name'], ico=Ico.server, prop="srv", val=srv['address'])
        else:
            self.tabBar.setCurrentIndex(idx)

    def on_help(self):

        idx = self.get_widget_index(help_widgets.HelpWidget)
        if idx is None:
            hw = help_widgets.HelpWidget(self)
            self.add_widget(hw, "Help", Ico.help)

    def on_load_server_to_menu(self):
        self.buttConnect.menu().clear()
        for srv in G.settings.servers_list():
            s = "%s - %s" % (srv['name'], srv['address'])
            act = self.buttConnect.menu().addAction(s)
            act.setProperty("srv", srv)

    def on_connect_action(self, act):
        self.open_server(act.property("srv"))