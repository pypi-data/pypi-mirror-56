# -*- coding: utf-8 -*-

import paramiko
from Qt import QtCore, QtWidgets, QtNetwork, Qt, pyqtSignal

from img import Ico

import cwidgets

from runtime import terminal_widget

class SshTerminalWidget(QtWidgets.QWidget):

    def __init__(self, parent, serverConn):
        QtWidgets.QWidget.__init__(self, parent)

        assert serverConn != None
        self.serverConn = serverConn

        self.sshClient = paramiko.SSHClient()
        self.sshClient.load_system_host_keys()
        self.sshClient.set_missing_host_key_policy(paramiko.WarningPolicy)



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

        self.buttConnect = cwidgets.XToolButton(ico=Ico.start, text="Connect", callback=self.on_connect)
        grp.addWidget(self.buttConnect)

        self.lblStatus = cwidgets.XLabel()
        grp.addWidget(self.lblStatus)



        ## ------------ send command
        grp = cwidgets.ToolBarGroup(title="Execute")
        self.toolbar.addWidget(grp)

        self.txtCommand = cwidgets.XLineEdit()
        grp.addWidget(self.txtCommand)
        self.txtCommand.setText("ls -l")
        self.txtCommand.returnPressed.connect(self.on_execute)

        self.buttConnect = cwidgets.XToolButton(ico=Ico.return_key, text="Execute", callback=self.on_execute)
        grp.addWidget(self.buttConnect)



        self.terminal = terminal_widget.Terminal(self)
        self.mainLayout.addWidget(self.terminal)

        ## ------------ tree
        self.model = LinesModel(self)

        #self.tree = QtWidgets.QTreeView()
        #self.mainLayout.addWidget(self.tree)
        #self.tree.setModel(self.model)

        #self.txt = QtWidgets.QTextEdit()
        #self.mainLayout.addWidget(self.txt)



        self.serverConn.sigSSHMessage.connect(self.on_ssh_message)

        self.terminal.add()

    def init_load(self):
        pass


    def deadon_connect(self):
        self.serverConn.connect_ssh(self.txtHost.s(), self.spinPort.value(),
                                    self.txtUser.s(), self.txtPass.s())

    def on_ssh_message(self, mess, err):
        #print(mess)
        print(err, len(err))

        if err:
            self.model.add_rec(2, err)
            self.txt.setPlainText(err)
            return
        self.txt.setPlainText(mess)
        self.model.add_rec(1, mess)



    def on_execute(self):
        cmd = self.txtCommand.s()
        #self.serverConn.send_ssh(cmd)
        self.terminal.run(cmd)



    def on_connect(self):
        # print("on_ssh")
        self.sshClient.connect(self.txtHost.s(), self.spinPort.value(),
                                    self.txtUser.s(), self.txtPass.s())
        self.send_ssh("uname -a")
        self.send_ssh("whoami")

    def send_ssh(self, cmd):
        stdin, stdout, stderr = self.sshClient.exec_command(cmd)
        # print( stdout.read(), )
        sout = str(stdout.read(), encoding="ascii")
        serr = str(stderr.read(), encoding="ascii")
        self.model.add_rec(0, serr)


class LinesModel(QtCore.QAbstractTableModel):

    def __init__(self, parent=None):
        super(QtCore.QAbstractTableModel, self).__init__()

        self.lines = []
        self.ltypes = []

    def data(self, midx, role):
        cidx = midx.column()

        if role == Qt.DisplayRole:
            if cidx == 0:
                return "^" if self.ltypes[midx.row()] else ">"

            elif cidx == 1:
                return self.lines[midx.row()]


    def columnCount(self, pidx=None):
        return 2

    def rowCount(self, pidx=None):
        return len(self.lines)

    def headerData(self, idx, orientation, role):
        if role == Qt.DisplayRole:
            return ["Exec", "RESP"][idx]

    def add_rec(self, typ, recv_lines):

        #lst = [s.strip() for s in recv_lines.split("\n")]
        for l in [s.strip() for s in recv_lines.split("\n")]:
            if l:
                self.ltypes.append(typ)
                self.lines.append(l)
        self.layoutChanged.emit()

