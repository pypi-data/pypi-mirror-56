

import platform



from Qt import QtCore, QtWidgets, Qt, pyqtSignal

from img import Ico
import G
import cwidgets



class SlaveDialog(QtWidgets.QDialog):

    sigSaved = pyqtSignal(dict)


    DATA_TYPE_ROLE = Qt.UserRole + 3

    def __init__(self, parent=None, dev_id=None, serverConn=None):
        super().__init__(parent)

        self.dev_id = dev_id
        self.serverConn = serverConn
        assert self.serverConn != None
        self.rec = None

        self.setWindowTitle("Slave Details")
        self.setWindowIcon(Ico.icon(Ico.slave))
        self.setMinimumWidth(800)



        self.mainLayout = cwidgets.vlayout(margin=20)
        self.setLayout(self.mainLayout)

        colLayout = cwidgets.hlayout(spacing=10)
        self.mainLayout.addLayout(colLayout)

        leftLay = cwidgets.vlayout()
        colLayout.addLayout(leftLay)

        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(10)
        leftLay.addLayout(self.grid)

        row = 0
        self.chkActive = QtWidgets.QCheckBox()
        self.chkActive.setText("Active")
        self.grid.addWidget(self.chkActive, row, 1)

        self.lblID = QtWidgets.QLabel()
        self.grid.addWidget(self.lblID, row, 2)

        row += 1
        self.grid.addWidget(QtWidgets.QLabel("Label / Name"), row, 0, Qt.AlignRight)
        self.txtDeviceName = cwidgets.XLineEdit()
        self.grid.addWidget(self.txtDeviceName, row, 1)
        self.txtDeviceName.setPlaceholderText("eg RPI #1")

        row  += 1
        self.grid.addWidget(QtWidgets.QLabel("Type"), row, 0, Qt.AlignRight)
        self.cmbDeviceType = QtWidgets.QComboBox()
        self.grid.addWidget(self.cmbDeviceType, row, 1, 1, 2)
        self.cmbDeviceType.currentIndexChanged.connect(self.on_combo_dev_type)


        row += 1
        self.grid.addWidget(QtWidgets.QLabel("Slave ID"), row, 0, Qt.AlignRight)
        self.spinSlaveID = QtWidgets.QSpinBox()
        self.spinSlaveID.setRange(0, 100)
        self.grid.addWidget(self.spinSlaveID, row, 1)

        row += 1
        self.lblIpAddress = QtWidgets.QLabel("IP Address")
        self.grid.addWidget(self.lblIpAddress, row, 0, Qt.AlignRight)
        self.txtIPAddress = cwidgets.XLineEdit()
        self.grid.addWidget(self.txtIPAddress, row, 1, 1, 2)
        #self.txtIPAddress.setInputMask("000.000.000.000;_")

        row += 1
        self.lblIpPort = QtWidgets.QLabel("Port")
        self.grid.addWidget(self.lblIpPort, row, 0, Qt.AlignRight)
        self.spinIpPort = QtWidgets.QSpinBox()
        self.spinIpPort.setRange(0, 65535)
        self.grid.addWidget(self.spinIpPort, row, 1)

        row += 1
        self.lblCommPort = QtWidgets.QLabel("Comm Port")
        self.grid.addWidget(self.lblCommPort , row, 0, Qt.AlignRight)
        self.cmbCommPort = QtWidgets.QComboBox()
        self.grid.addWidget(self.cmbCommPort, row, 1)
        self.cmbCommPort.setEditable(True)

        row += 1
        self.lblBaudRate = QtWidgets.QLabel("Baud Rate")
        self.grid.addWidget(self.lblBaudRate , row, 0, Qt.AlignRight)
        self.cmbBaudRate = QtWidgets.QComboBox()
        self.grid.addWidget(self.cmbBaudRate, row, 1)
        self.cmbBaudRate.setEditable(True)
        for b in [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]:
            self.cmbBaudRate.addItem(str(b))


        row += 1
        self.lblParity = QtWidgets.QLabel("Parity")
        self.grid.addWidget(self.lblParity , row, 0, Qt.AlignRight)
        self.cmbParity = QtWidgets.QComboBox()
        self.grid.addWidget(self.cmbParity, row, 1)
        for p in ["none", "odd", "even"]:
            self.cmbParity.addItem(p)


        row += 1
        self.lblDataBits = QtWidgets.QLabel("Data Bits")
        self.grid.addWidget(self.lblDataBits , row, 0, Qt.AlignRight)
        self.spinDataBits = QtWidgets.QSpinBox()
        self.spinDataBits.setRange(0, 256)
        self.grid.addWidget(self.spinDataBits, row, 1)


        row += 1
        self.lblStopBits = QtWidgets.QLabel("Stop Bits")
        self.grid.addWidget(self.lblStopBits , row, 0, Qt.AlignRight)
        self.spinStopBits = QtWidgets.QSpinBox()
        self.spinStopBits.setRange(0, 2)
        self.grid.addWidget(self.spinStopBits, row, 1)

        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 1)
        self.grid.setColumnStretch(2, 1)

        leftLay.addStretch(20)


        #========================
        rightLay = cwidgets.vlayout(spacing=15)
        colLayout.addLayout(rightLay)

        self.ioWidgets = {}

        for item in IO_PREFIXES:

            self.ioWidgets[item['prefix']] = IO_ItemWidget(prefix=item['prefix'], label=item['label'])
            rightLay.addWidget(self.ioWidgets[item['prefix']])


        self.actionBar = cwidgets.FormActionBar(self)
        self.mainLayout.addWidget(self.actionBar)

        self.fetch()




    def on_cancel(self):
        self.reject()

    def on_validate(self):

        s = self.txtServerAddress.s()
        url = QtCore.QUrl(s)
        ena = False
        if url.isValid() and url.scheme() in ["http", "https"]:
            ena = True
        self.buttPing.setEnabled(ena)

    def selected_conn_type(self):
        if self.cmbDeviceType.currentIndex() == 0:
            return None
        return self.cmbDeviceType.itemData(self.cmbDeviceType.currentIndex(), self.DATA_TYPE_ROLE)['conn_type']

    def on_save(self):



        for w in [self.txtDeviceName]:
            if len(w.s()) < 4:
                #w.borderInvalid()
                w.setFocus()
                return

        typ = self.selected_conn_type()
        if typ == None:
            self.cmbDeviceType.setFocus()
            return

        if typ == "net":
            if len(self.txtIPAddress.s()) < 4:
                self.txtIPAddress.setFocus()
                return
            if self.spinIpPort.value() < 10:
                self.spinIpPort.setFocus()
                return

        elif type == "serial":

            if self.cmbCommPort.len() < 4:
                self.cmbCommPort.setFocus()
                return


        nrec = dict(
            dev_id = self.dev_id,
            active = self.chkActive.isChecked(),
            dev_name = self.txtDeviceName.s(),
            dev_type = self.cmbDeviceType.currentData(),
            slave_id = self.spinSlaveID.value(),

            ip_address = self.txtIPAddress.s(),
            ip_port = self.spinIpPort.value(),

            com_port = self.cmbCommPort.currentText(),
            baud_rate = int(self.cmbBaudRate.currentText()),
            parity = self.cmbParity.currentText(),
            data_bits = self.spinDataBits.value(),
            stop_bits =self.spinStopBits.value(),

            conn_type = typ

        )

        for dt in IO_PREFIXES:
            dic = self.ioWidgets[dt['prefix']].get_values()
            nrec.update(dic)

        self.serverConn.post(self, "/slave-devices/%s" % self.dev_id, data=nrec)


    def fetch(self):
        self.serverConn.get(self, "/slave-devices/%s" % self.dev_id)

    def on_server_reply(self, reply):

        if reply.busy:
            return
        #print(reply)

        #print(reply.data)
        if reply.data and "error" in reply.data and reply.data['error']:
            print(reply.data)
            self.actionBar.status
            return

        if reply.post:
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<")
            print("POST+", reply)
            if reply.error:
                dsadsa()
                return
            self.sigSaved.emit(reply.data['slave'])
            self.accept()

            #for k in reply.data['pre']:
            #    print(" " if reply.data['pre'][k] == reply.data['merge'][k] else "#", k, reply.data['pre'][k], reply.data['merge'][k], reply.data['src'][k])
            #pprint(reply.data['pre'])
            #pprint(reply.data['merge'])
            return

        self.rec = reply.data['slave']
        #for k in sorted(self.rec.keys()):
        #    print(k, self.rec[k])

        self.actionBar.set_meta("dev_id", self.rec)

        # Serial
        self.cmbCommPort.addItem("")
        for r in reply.data['serial_ports']:
            self.cmbCommPort.addItem(r)




        # Types
        self.cmbDeviceType.addItem("-- select --")
        for idx, dt in enumerate(reply.data['device_types']):
            self.cmbDeviceType.addItem(dt['label'], dt['dev_type'])
            self.cmbDeviceType.setItemData(idx + 1, dt, self.DATA_TYPE_ROLE)
        idx = self.cmbDeviceType.findData(self.rec['dev_type'])
        if idx != -1:
            self.cmbDeviceType.setCurrentIndex(idx)

        self.chkActive.setChecked(self.rec['active'] == True)

        self.lblID.setText(self.rec['dev_id'])
        self.txtDeviceName.setText(self.rec['dev_name'])

        self.txtIPAddress.setText(self.rec['ip_address'])
        self.spinIpPort.setValue(self.rec['ip_port'])

        self.spinStopBits.setValue(self.rec['stop_bits'])
        self.spinDataBits.setValue(self.rec['data_bits'])

        for dt in IO_PREFIXES:
            self.ioWidgets[dt['prefix']].set_values(self.rec)

    def show_serial_widgets(self, is_serial):

        self.lblIpAddress.setVisible(not is_serial)
        self.txtIPAddress.setVisible(not is_serial)

        self.lblIpPort.setVisible(not is_serial)
        self.spinIpPort.setVisible(not is_serial)

        self.lblCommPort.setVisible(is_serial)
        self.cmbCommPort.setVisible(is_serial)

        self.lblBaudRate.setVisible(is_serial)
        self.cmbBaudRate.setVisible(is_serial)

        self.lblParity.setVisible(is_serial)
        self.cmbParity.setVisible(is_serial)

        self.lblDataBits.setVisible(is_serial)
        self.spinDataBits.setVisible(is_serial)

        self.lblStopBits.setVisible(is_serial)
        self.spinStopBits.setVisible(is_serial)

    def show_ip_widgets(self, state):

        self.lblIpAddress.setVisible(state)
        self.txtIPAddress.setVisible(state)

        self.lblIpPort.setVisible(state)
        self.spinIpPort.setVisible(state)


    def on_combo_dev_type(self, idx=None):

        idx = self.cmbDeviceType.currentIndex()
        if idx == 0:
            self.show_serial_widgets(False)
            self.show_ip_widgets(False)
            return

        data = self.cmbDeviceType.itemData(idx, self.DATA_TYPE_ROLE)
        self.show_serial_widgets(data['conn_type'] == "serial")
        self.show_ip_widgets(data['conn_type'] == "net")







IO_PREFIXES = [
    {"prefix": "di", "label": "Discrete Inputs (%IX100.0)"},
    {"prefix": "coil", "label": "Coils (%QX100.0)"},
    {"prefix": "ir", "label": "Input Registers (%IW100)"},
    {"prefix": "hr_read", "label": "Holding Registers - Read (%IW100)"},
    {"prefix": "hr_write", "label": "Holding Registers - Write (%QW100)"},
]

class IO_ItemWidget(QtWidgets.QGroupBox):


    def __init__(self, parent=None, prefix=None, label=None):
        super().__init__(parent)

        self.prefix = prefix
        self.setTitle(label)



        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(10)
        self.setLayout(self.grid)

        row = 0
        self.grid.addWidget(QtWidgets.QLabel("Start Address"), row, 0)

        self.spinStart = QtWidgets.QSpinBox()
        self.grid.addWidget(self.spinStart, row, 1)

        self.grid.addWidget(QtWidgets.QLabel("Size"), row, 2)

        self.spinSize = QtWidgets.QSpinBox()
        self.grid.addWidget(self.spinSize, row, 3)


    def set_values(self, rec):

        v = rec["%s_start" % self.prefix]
        self.spinStart.setValue(v)

        v = rec["%s_size" % self.prefix]
        self.spinSize.setValue(v)

    def get_values(self):
        dic = {}
        dic["%s_start" % self.prefix] = self.spinStart.value()
        dic["%s_size" % self.prefix] = self.spinSize.value()
        return dic



