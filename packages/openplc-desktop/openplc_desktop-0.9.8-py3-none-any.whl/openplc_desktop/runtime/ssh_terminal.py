# -*- coding: utf-8 -*-

import re

import paramiko
from Qt import QtCore, QtWidgets, QtGui, Qt, pyqtSignal

from img import Ico
import cwidgets
import ut
import G

from runtime import terminal_widget

class SshTerminalWidget(QtWidgets.QWidget):

    def __init__(self, parent, serverConn):
        QtWidgets.QWidget.__init__(self, parent)

        assert serverConn != None
        self.serverConn = serverConn





        self.mainLayout = cwidgets.vlayout()
        self.setLayout(self.mainLayout)

        self.toolbar = cwidgets.XToolBar()
        self.mainLayout.addWidget(self.toolbar)

        ## ------------ credentials
        grp = cwidgets.ToolBarGroup(title="SSH Terminal")
        self.toolbar.addWidget(grp)

        self.txtHost = cwidgets.XLineEdit()
        grp.addWidget(self.txtHost)
        self.txtHost.setMaximumWidth(120)
        self.txtHost.setPlaceholderText("eg 192.168.1.100")

        self.spinPort = QtWidgets.QSpinBox()
        grp.addWidget(self.spinPort)
        self.spinPort.setValue(22)

        self.txtUser = cwidgets.XLineEdit()
        grp.addWidget(self.txtUser)
        self.txtUser.setPlaceholderText("pi")
        self.txtUser.setMaximumWidth(80)

        self.txtPass = cwidgets.XLineEdit()
        grp.addWidget(self.txtPass)
        self.txtPass.setPlaceholderText("raspberry")
        self.txtPass.setMaximumWidth(80)

        self.buttConnect = cwidgets.XToolButton(ico=Ico.start, text="Connect", callback=self.on_connect)
        grp.addWidget(self.buttConnect)

        self.lblStatus = cwidgets.XLabel()
        grp.addWidget(self.lblStatus)



        ## ------------ send command
        self.grpExecute = cwidgets.ToolBarGroup(title="Execute")
        self.toolbar.addWidget(self.grpExecute)

        self.txtCommand = cwidgets.XLineEdit()
        self.grpExecute.addWidget(self.txtCommand)
        self.txtCommand.setText("ls -al")
        self.txtCommand.returnPressed.connect(self.on_execute)

        self.buttConnect = cwidgets.XToolButton(ico=Ico.return_key, text="Execute", callback=self.on_execute)
        self.grpExecute.addWidget(self.buttConnect)


        self.grpExecute.setDisabled(True)



        ## ------------ Actions
        self.grpActions = cwidgets.ToolBarGroup(title="Actions")
        self.toolbar.addWidget(self.grpActions)

        self.buttClear = cwidgets.XToolButton(ico=Ico.clear, text="Clear", callback=self.on_clear)
        self.grpActions.addWidget(self.buttClear)


        ## ------------ tree


        self.term = TerminalTextEdit()
        self.mainLayout.addWidget(self.term)

        if False:
            self.syntax = terminal_widget.name_highlighter(self.term.document(),
                                                       host_name="anabel",
                                                       user_name=self.txtUser.s())

        self.ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')

        #=============================================
        self.sshClient = paramiko.SSHClient()
        self.sshClient.load_system_host_keys()
        self.sshClient.set_missing_host_key_policy(paramiko.WarningPolicy)

        self.shell = None
        #self.serverConn.sigSSHMessage.connect(self.on_ssh_message)
        # G.settings.setValue("ssh-port", 22)
        #G.settings.sync()
        self.txtHost.setText(G.settings.value("ssh-host"))
        v = ut.to_int(G.settings.value("ssh-port"), 22)
        self.spinPort.setValue(v)
        self.txtUser.setText(G.settings.value("ssh-login", "pi"))
        self.txtPass.setText(G.settings.value("ssh-pass", "raspberry"))

    def init_load(self):
        pass


    def term_creds(self):
        self.name = "[" + str(getpass.getuser()) + "@" + str(socket.gethostname()) + "]" + "  ~" + str(
        os.getcwd()) + " >$ "


    def on_connect(self):
        # print("on_ssh")

        for widget in [self.txtHost, self.txtUser, self.txtPass]:
            if widget.len() == 0:
                widget.setFocus()
                return

        G.settings.setValue("ssh-host", self.txtHost.s())
        G.settings.setValue("ssh-port", self.spinPort.value())
        G.settings.setValue("ssh-login", self.txtUser.s())
        G.settings.setValue("ssh-pass", self.txtPass.s())
        G.settings.sync()

        self.sshClient.connect(self.txtHost.s(), self.spinPort.value(),
                                    self.txtUser.s(), self.txtPass.s())

        self.sshClient.exec_command("/bin/bash")
        self.shell = self.sshClient.invoke_shell()

        self.grpExecute.setDisabled(False)

        print(self.shell)

        #self.send_ssh("uname -a")
        #self.send_ssh("whoami")

    def send_ssh(self, cmd):
        print("send_ssh=", cmd)
        self.shell.send(cmd + "\n")
        self.sshclient_rev()
        return

        stdin, stdout, stderr = self.sshClient.exec_command(cmd, get_pty=False)
        #print( stdout.read(), stderr.read() )
        sout = str(stdout.read(), encoding="ascii")
        serr = str(stderr.read(), encoding="ascii")

        print( serr, stdin )
        self.term.appendPlainText(sout.strip() + "\n")

        newCursor = QtGui.QTextCursor(self.term.document())
        newCursor.movePosition(QtGui.QTextCursor.End)
        self.term.setTextCursor(newCursor)

    def sshclient_rev(self):
        #while True:
        alldata = self.shell.recv(65000)
        print("======", alldata, type(alldata))

        s = alldata.decode('utf8', "ignore").replace('\r', '').strip()
        s = self.ansi_escape.sub('', s)
        print("s=", s)

        self.term.appendPlainText(s)

        return

        if alldata:
            s = alldata.decode('utf-8', "ignore")
            s = s.replace('\r', '')
            # print("s:",s)
        else:
            s = None
            # print("s is none")
        #print(alldata)
        return s



    def on_execute(self):
        cmd = self.txtCommand.s()
        #self.serverConn.send_ssh(cmd)
        self.send_ssh(cmd)

    def on_clear(self):
        self.term.clear()


    def close_all(self):
        self.sshClient.close()
        self.shell = None
        self.sshClient = None

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


class TerminalTextEdit(QtWidgets.QPlainTextEdit):


    def __init__(self):
        QtWidgets.QPlainTextEdit.__init__(self)

        self.setStyleSheet("QPlainTextEdit{background-color: #212121; color: white; padding: 8;}")
        self.font = QtGui.QFont()
        self.font.setFamily("monospace")
        self.font.setPointSize(9)
        self.text = None
        self.setFont(self.font)