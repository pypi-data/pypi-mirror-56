# -*- coding: utf-8 -*-

import paramiko
from Qt import QtCore, QtWidgets, QtNetwork, Qt, pyqtSignal

from img import Ico

import cwidgets


class RuntimeCommanderWidget(QtWidgets.QWidget):

    def __init__(self, parent, serverConn):
        QtWidgets.QWidget.__init__(self, parent)

        assert serverConn != None
        self.serverConn = serverConn

        self.serverConn.sigRuntimeMessage.connect(self.on_runtime_message)


        self.mainLayout = cwidgets.vlayout()
        self.setLayout(self.mainLayout)

        # self.toolbar = QtWidgets.QToolBar()
        # self.mainLayout.addWidget(self.toolbar)



        # ===============
        midLay = cwidgets.hlayout()
        self.mainLayout.addLayout(midLay)
        #grp = cwidgets.ToolBarGroup(title="Commands")
        #self.toolbar.addWidget(grp)

        self.txt = QtWidgets.QTextEdit()
        midLay.addWidget(self.txt)


        rightLay = cwidgets.vlayout(spacing=5)
        midLay.addLayout(rightLay)

        grp = cwidgets.ToolBarGroup(title="RunTime Connect")
        rightLay.addWidget(grp)
        self.buttConnect = cwidgets.XToolButton(ico=Ico.start, text="Connect", callback=self.on_connect)
        grp.addWidget(self.buttConnect)

        self.buttConnect = cwidgets.XToolButton(ico=Ico.start, text="SSH", callback=self.on_ssh)
        grp.addWidget(self.buttConnect)

        self.lblStatus = cwidgets.XLabel()
        grp.addWidget(self.lblStatus)



        rightLay.addSpacing(10)
        lbl = cwidgets.XLabel(text="Commands")
        rightLay.addWidget(lbl)

        self.buttGroup = QtWidgets.QButtonGroup(self)
        self.buttGroup.setExclusive(False)
        self.buttGroup.buttonClicked.connect(self.on_exec_button)
        for cmd in ["runtime_logs()", "exec_time()",
                    "start_modbus()", "stop_modbus()",
                    "start_dnp3()", "stop_dnp3()",
                    "start_enip()", "stop_enip()",
                    "start_pstorage()", "stop_pstorage()",
                    "quit()"
                    ]:
            butt = cwidgets.XToolButton(text=cmd, autoRaise=False)
            rightLay.addWidget(butt)
            self.buttGroup.addButton(butt)
            butt.setFixedWidth(200)
            butt.setDisabled(True)

        rightLay.addStretch(10)

        self.show_status(False)


    def init_load(self):
        pass


    def on_connect(self):
        self.serverConn.connect_runtime()

    def on_runtime_message(self, mess):
        print(mess)
        self.show_status(mess.connected)
        if mess.message:
            self.txt.setPlainText(mess.message)
        for b in self.buttGroup.buttons():
            b.setEnabled(mess.connected)

    def on_exec_button(self, butt):
        cmd = butt.text()
        self.serverConn.send_runtime(cmd)


    def show_status(self, connected):
        self.lblStatus.setText("Connected" if connected else "Disconnected")
        sty = "background-color: %s" % ("#EDFFDA" if connected else "#FFDFDA")
        self.lblStatus.setStyleSheet(sty)

    def on_ssh(self):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)

        print("on_ssh")
        client.connect("192.168.1.222", port=22, username="pi", password="raspberry")
        print("connect")
        stdin, stdout, stderr = client.exec_command("ls -al")
        #print( stdout.read(), )
        s = str(stdout.read(), encoding="ascii")
        print(s)
        self.txt.setText(s)


