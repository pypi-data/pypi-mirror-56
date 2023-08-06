# -*- coding: utf-8 -*-

from Qt import QtCore, QtWidgets, Qt, pyqtSignal

from img import Ico

import cwidgets

def gen_group(title, chk, help=None):

    widget = QtWidgets.QGroupBox()
    widget.setTitle(title)
    widget.setCheckable(chk)
    lay = QtWidgets.QGridLayout()
    widget.setLayout(lay)

    if help:
        lbl = cwidgets.XLabel()
        lbl.setText(help)
        lbl.setStyleSheet("background-color: white; color: #000099; padding: 4px; border-radius: 4px;")
        #lbl.setMaximumWidth(300)
        lbl.setWordWrap(True)
        lay.addWidget(lbl, 0, 0, 1, 2)
    lay.setColumnStretch(0, 0)
    lay.setColumnStretch(1, 1)
    return widget


class SettingsDialog(QtWidgets.QDialog):

    sigSaved = pyqtSignal(dict)
    sigDeleted = pyqtSignal(str)

    @property
    def url(self):
        return "/settings"

    def __init__(self, parent=None, serverConn=None):
        super().__init__(parent)

        assert serverConn != None

        self.serverConn = serverConn

        self.setWindowTitle("Settings")
        self.setWindowIcon(Ico.icon(Ico.settings))
        self.setMinimumWidth(500)
        self.setMaximumWidth(600)


        self.mainLayout = cwidgets.vlayout(margin=20)
        self.setLayout(self.mainLayout)


        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(10)
        self.mainLayout.addLayout(self.grid)

        row = 0
        hlp = "Modbus slave enables reading and writing located variables through the" \
            "modbus interface. This starts a Modbus server (also know as a slave) " \
            "running in the OpenPLC runtime."
        self.grpModbusSlave = gen_group("Modbus Slave Enabled", True, help=hlp)
        self.grid.addWidget(self.grpModbusSlave, row, 0)

        self.grpModbusSlave.layout().addWidget(QtWidgets.QLabel("Port"), 1, 0, Qt.AlignRight)
        self.spinModbusSlavePort = QtWidgets.QSpinBox()
        self.spinModbusSlavePort.setRange(0, 30000)
        self.spinModbusSlavePort.setMaximumWidth(80)
        self.grpModbusSlave.layout().addWidget(self.spinModbusSlavePort, 1, 1)

        row += 1
        hlp = "Modbus master enables reading and writing located variables through the " \
                "modbus interface. This starts capabilities to poll one or more Modbus " \
                " servers and exchange data with the located variables."
        self.grpModbusMaster = gen_group("Modbus Master Enabled", True, help=hlp)
        self.grid.addWidget(self.grpModbusMaster, row, 0)

        self.grpModbusMaster.layout().addWidget(QtWidgets.QLabel("Address"), 1, 0, Qt.AlignRight)
        self.txtModbusMasterAddress = cwidgets.XLineEdit()
        self.grpModbusMaster.layout().addWidget(self.txtModbusMasterAddress, 1, 1)

        self.grpModbusMaster.layout().addWidget(QtWidgets.QLabel("Port"), 2, 0, Qt.AlignRight)
        self.spinModbusMasterPort = QtWidgets.QSpinBox()
        self.spinModbusMasterPort.setRange(0, 30000)
        self.spinModbusMasterPort.setMaximumWidth(80)
        self.grpModbusMaster.layout().addWidget(self.spinModbusMasterPort, 3, 1)


        row += 1
        self.grpDnp = gen_group("DNP3 Enabled", True)
        self.grid.addWidget(self.grpDnp, row, 0)

        self.grpDnp.layout().addWidget(QtWidgets.QLabel("Port"), 0, 0, Qt.AlignRight)
        self.spinDNP3Port = QtWidgets.QSpinBox()
        self.spinDNP3Port.setRange(0, 30000)
        self.grpDnp.layout().addWidget(self.spinDNP3Port, 0, 1)

        row += 1
        self.grpSlave = gen_group("Slave", False)
        self.grid.addWidget(self.grpSlave, row, 0)

        self.grpSlave.layout().addWidget(QtWidgets.QLabel("Polling (ms)"), 0, 0, Qt.AlignRight)
        self.spinSlavePolling = QtWidgets.QSpinBox()
        self.spinSlavePolling.setRange(0, 30000)
        self.grpSlave.layout().addWidget(self.spinSlavePolling, 0, 1)

        self.grpSlave.layout().addWidget(QtWidgets.QLabel("Timeout (ms)"), 1, 0, Qt.AlignRight)
        self.spinSlaveTimeout = QtWidgets.QSpinBox()
        self.spinSlaveTimeout.setRange(0, 30000)
        self.grpSlave.layout().addWidget(self.spinSlaveTimeout, 1, 1)

        self.grid.setColumnStretch(0, 2)
        #self.grid.setColumnStretch(1, 1)
        #self.grid.setColumnStretch(1, 1)
        #self.grid.setColumnStretch(2, 2)

        self.mainLayout.addSpacing(20)

        self.formBar = cwidgets.FormActionBar(self, show_meta=False)
        self.mainLayout.addWidget(self.formBar)

        self.init_load()

    def init_load(self):
        self.serverConn.get(self, self.url)

    def on_server_reply(self, reply):

        if reply.busy:
            return


        if reply.post:

            if reply.data.get("saved") == True:
                self.sigSaved.emit(reply.data['settings'])
                self.accept()
            return

        self.formBar.set_reply(reply)

        rec = reply.data.get('settings')

        #self.grpModbus.setChecked(rec["modbus_enabled"])
        #self.spinModbusPort.setValue(rec['modbus_port'])

        self.grpDnp.setChecked(rec["dnp3_enabled"])
        self.spinDNP3Port.setValue(rec['dnp3_port'])

        self.spinSlavePolling.setValue(rec['slave_polling'])
        self.spinSlaveTimeout.setValue(rec['slave_timeout'])



        self.formBar.set_meta("prog_id", rec)

        self.setDisabled(False)




    def on_cancel(self):
        self.reject()

    def on_save(self):


        rec = dict(modbus_enabled = self.grpModbus.isChecked(),
                   modbus_port = self.spinModbusPort.value(),
                   dnp3_enabled = self.grpDnp.isChecked(),
                   dnp3_port = self.spinDNP3Port.value(),
                   slave_polling = self.spinSlavePolling.value(),
                   slave_timeout = self.spinSlaveTimeout.value(),
                   )

        self.serverConn.post(self, self.url, data=rec)


    def on_delete(self):
        self.sigDeleted.emit(self.user_id)
        self.accept()

    def on_set_pass(self, state=False):
        self.txtPass.setEnabled(self.chkPass.isChecked())