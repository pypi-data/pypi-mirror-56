

from Qt import QtCore, QtWidgets, Qt, pyqtSignal

from img import Ico
import G
import cwidgets

from server import server_conn

class ServerDialog(QtWidgets.QDialog):

    sigSaved = pyqtSignal(dict)


    def __init__(self, parent=None, server=None):
        super().__init__(parent)



        self.setWindowTitle("Server Details")
        self.setWindowIcon(Ico.icon(Ico.server))
        self.setMinimumWidth(400)


        self.mainLayout = cwidgets.vlayout(margin=20, spacing=10)
        self.setLayout(self.mainLayout)


        if server == None:
            s = "Create a new server connection"
            self.lbl = cwidgets.InfoLabel(s, style=cwidgets.InfoLabel.INFO)
            self.mainLayout.addWidget(self.lbl)

        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(10)
        self.mainLayout.addLayout(self.grid)

        row = 0
        self.grid.addWidget(QtWidgets.QLabel("Label / Name"), row, 0, Qt.AlignRight)
        self.txtServerName = cwidgets.XLineEdit()
        self.grid.addWidget(self.txtServerName, row, 1)
        self.txtServerName.setPlaceholderText("eg My Server")

        row  += 1
        self.grid.addWidget(QtWidgets.QLabel("Server Http Address"), row, 0, Qt.AlignRight)
        self.txtServerAddress = cwidgets.XLineEdit()

        self.grid.addWidget(self.txtServerAddress, row, 1, 1, 2)
        self.txtServerAddress.textChanged.connect(self.on_validate)

        self.buttPing = cwidgets.XToolButton(self, text="Ping", autoRaise=False, callback=self.on_ping)
        self.grid.addWidget(self.buttPing, row, 3)

        row += 1
        self.grid.addWidget(QtWidgets.QLabel("eg http://192.168.1.123:8080"), row, 1, Qt.AlignRight)


        row += 1
        self.grid.addWidget(QtWidgets.QLabel("User"), row, 0, Qt.AlignRight)
        self.txtUser = cwidgets.XLineEdit()
        self.grid.addWidget(self.txtUser, row, 1)

        row += 1
        self.grid.addWidget(QtWidgets.QLabel("Password"), row, 0, Qt.AlignRight)
        self.txtPass = cwidgets.XLineEdit()
        self.grid.addWidget(self.txtPass, row, 1)

        row += 1

        self.buttTestLogin = cwidgets.XToolButton(self, text="Test Login", autoRaise=False, callback=self.on_test_login)
        self.grid.addWidget(self.buttTestLogin, row, 1, Qt.AlignRight)


        row += 1
        self.chkAutoConnect = QtWidgets.QCheckBox()
        self.chkAutoConnect.setText("Auto connect at startup")
        self.grid.addWidget(self.chkAutoConnect, row, 1)

        row += 1
        self.txtMess = QtWidgets.QLabel("")
        self.grid.addWidget(self.txtMess, row, 1)

        self.statusBar = cwidgets.StatusBar(self, refresh=False)
        self.mainLayout.addWidget(self.statusBar)

        self.formBar = cwidgets.FormActionBar(self, show_meta=False)
        self.mainLayout.addWidget(self.formBar)

        self.formBar.buttSave.setIcon(Ico.icon(Ico.login))
        self.formBar.buttSave.setText("Login")

        if server:
            self.load(server)

    def load(self, srv):
        self.txtServerName.setText(srv['name'])
        self.txtServerAddress.setText(srv['address'])
        self.txtUser.setText(srv['login'])
        self.txtPass.setText(srv['password'])
        self.chkAutoConnect.setChecked(srv['auto_connect'])


    def on_cancel(self):
        self.reject()

    def on_validate(self):

        s = self.txtServerAddress.s()
        url = QtCore.QUrl(s)
        ena = False
        if url.isValid() and url.scheme() in ["http", "https"]:
            ena = True
        self.buttPing.setEnabled(ena)


    def on_save(self):

        for w in self.txtServerName, self.txtServerAddress, self.txtUser, self.txtPass:
            if len(w.s()) < 4:
                #w.borderInvalid()
                w.setFocus()
                return

        srv = dict(
            name = self.txtServerName.s(),
            address = self.txtServerAddress.s(),
            login = self.txtUser.s(),
            password = self.txtPass.s(),
            auto_connect = self.chkAutoConnect.isChecked()
        )
        G.settings.save_server(srv)


        self.accept()




    def on_ping(self):
        addr = self.txtServerAddress.s()
        server = server_conn.ServerConn(self, server_address=addr)
        server.get(self, "/ping", tag="ping")

    def on_test_login(self):

        data = dict(login=self.txtUser.s(), password=self.txtPass.s())

        addr = self.txtServerAddress.s()
        server = server_conn.ServerConn(self, server_address=addr)
        server.post(self, "/login", tag="login", data=data)

    def on_server_reply(self, reply):

        self.statusBar.set_reply(reply)
        if reply.busy:
            return

        if reply.error:
            self.statusBar.set_reply(reply)
            return


        if reply.tag == "ping":
            if reply.data['ping'] == "pong":
                self.statusBar.showMessage("PING Success :-)", info=True, timeout=3000)

        if reply.tag == "login":
            if reply.data['logged_in']:
                self.statusBar.showMessage("Login Success :-)", info=True, timeout=3000)
            else:
                self.statusBar.showMessage("Login fail", timeout=3000)

