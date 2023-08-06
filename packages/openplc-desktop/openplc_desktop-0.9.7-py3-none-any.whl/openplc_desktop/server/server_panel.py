




from Qt import QtCore, QtWidgets, Qt, pyqtSignal

import cwidgets
from img import Ico


from server import server_conn, server_dialog
from slave_devices import slave_devices_grid, modbus_widgets
from users import users_grid
from programs import programs_grid
from network import websocket_panel
from runtime import settings_dialog, runtime_commander, ssh_terminal
#from runtime import pyqterm_test

class ServerPanel(QtWidgets.QMainWindow):


    def __init__(self, parent=None, server=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.server = server
        self.serverConn = server_conn.ServerConn(self, server_address=server["address"])





        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # Creds -------------------------
        self.tbServer = cwidgets.ToolBarGroup(self, title="Server Connection")
        self.toolbar.addWidget(self.tbServer)

        self.lblServerName = cwidgets.XLabel()
        self.lblServerName.setFixedWidth(160)
        self.tbServer.addWidget(self.lblServerName)

        self.lblServerStatus = cwidgets.XLabel()
        self.lblServerStatus.setFixedWidth(160)
        self.tbServer.addWidget(self.lblServerStatus)

        self.buttServer = cwidgets.XToolButton(self, ico=Ico.server, both=False, callback=self.on_server_edit)
        self.tbServer.addWidget(self.buttServer)

        self.buttWs = cwidgets.XToolButton(self, ico=Ico.save, both=False, callback=self.on_ws)
        self.tbServer.addWidget(self.buttWs)

        self.toolbar.addSeparator()


        # Runtime
        self.tbRuntime = cwidgets.ToolBarGroup(self, title="OpenPLC Runtime", is_group=True, toggle_icons=False)
        self.toolbar.addWidget(self.tbRuntime)

        self.buttStop = cwidgets.XToolButton(self, ico=Ico.stop, text="Stop", callback=self.on_runtime_stop)
        self.tbRuntime.addWidget(self.buttStop)

        self.buttStart = cwidgets.XToolButton(self, ico=Ico.start, text="Start", callback=self.on_runtime_start)
        self.tbRuntime.addWidget(self.buttStart)


        self.lblRuntimeStatus = cwidgets.XLabel("Status")
        self.tbRuntime.addWidget(self.lblRuntimeStatus)

        self.toolbar.addSeparator()

        # Actions
        self.tbActions = cwidgets.ToolBarGroup(self, title="Actions")
        self.toolbar.addWidget(self.tbActions)

        self.buttSettings = cwidgets.XToolButton(self, ico=Ico.settings, text="Settings", callback=self.on_settings)
        self.tbActions.addWidget(self.buttSettings)

        self.buttMbConfig = cwidgets.XToolButton(self, ico=Ico.mbconfig, text="mbconfig.cfg", callback=self.on_mbconfig)
        self.tbActions.addWidget(self.buttMbConfig)

        self.mainWidget = QtWidgets.QWidget()
        self.mainLayout = cwidgets.vlayout()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

        self.mainLayout.addSpacing(10)


        ## Midx widgets
        self.tabWidget = QtWidgets.QTabWidget()
        self.mainLayout.addWidget(self.tabWidget)


        #self.pyQTerm = pyqterm_test.PyQTermWidget(self, serverConn=self.serverConn)
        #self.tabWidget.addTab(self.pyQTerm, Ico.icon(Ico.terminal), "PyQTermWidget")


        self.runCommander = runtime_commander.RuntimeCommanderWidget(self, serverConn=self.serverConn)
        self.tabWidget.addTab(self.runCommander, Ico.icon(Ico.commander), "Commander")

        self.programsGrid = programs_grid.ProgramsGrid(self, serverConn=self.serverConn)
        self.tabWidget.addTab(self.programsGrid, Ico.icon(Ico.programs), "Programs")

        self.usersGrid = users_grid.UsersGrid(self, serverConn=self.serverConn)
        self.tabWidget.addTab(self.usersGrid, Ico.icon(Ico.users), "Users")


        self.slavesGrid = slave_devices_grid.SlaveDevicesGrid(self, serverConn=self.serverConn)
        self.tabWidget.addTab(self.slavesGrid, Ico.icon(Ico.slaves), "Slaves")


        self.sshTerminal = ssh_terminal.SshTerminalWidget(self, serverConn=self.serverConn)
        self.tabWidget.addTab(self.sshTerminal, Ico.icon(Ico.terminal), "SSH Terminal")



        self.lblServerName.setText("-")
        self.lblServerStatus.setText("-")


        ## Docks
        dock = QtWidgets.QDockWidget("Web Socket")
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        self.webSockPanel = websocket_panel.WebSocketPanel(self, serverConn=self.serverConn)
        dock.setWidget(self.webSockPanel)


    def on_ws(self):
        #self.serverConn.connect_websocket()

        self.serverConn.connect_websocket()


    def init_load(self):

        # self.fetch()
        self.on_login()

    def on_login(self):
        creds = dict(login=self.server['login'], password=self.server['password'])
        self.serverConn.post(self, "/login", data=creds, tag="login")


    def on_server_reply(self, reply):

        if reply.error:

            self.lblServerStatus.setText(reply.error)
            return
            self.statusBar.set_reply(reply)

        if reply.tag == "login":

            self.lblServerName.setText("-")
            self.lblServerStatus.setText("-")

            if reply.data and "logged_in" in reply.data and reply.data["logged_in"] == True:
                self.on_logged_in()
                self.lblServerName.setText(self.server['address'])
                self.lblServerStatus.setText("Connected")

                # &*^&^^&*^^**
                #self.serverConn.connect_websocket()

        if reply.tag == "runtime":

            self.lblServerName.setText("-")
            self.lblServerStatus.setText("-")

            self.serverConn.connect_runtime()




    def on_mbconfig(self):
        dial = modbus_widgets.MbConfigDialog(self, serverConn=self.serverConn)
        dial.exec_()

    def on_logged_in(self):
        for idx in range(0, self.tabWidget.count()):
            self.tabWidget.widget(idx).init_load()

    def on_server_edit(self):
        dial = server_dialog.ServerDialog(self, server=self.server)
        dial.exec_()


    def on_settings(self):
        dial = settings_dialog.SettingsDialog(self, serverConn=self.serverConn)
        dial.exec_()


    def on_runtime_start(self):
        print("start")
        self.serverConn.post(self, "/runtime/start", tag="runtime")

    def on_runtime_stop(self):
        print("stop")
        self.serverConn.post(self, "/runtime/stop", tag="runtime")