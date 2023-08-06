


from Qt import Qt, QtGui, QtCore, pyqtSignal


class C:
    node = 0

    dev_id = 1
    dev_name = 2
    dev_type = 3
    conn_type = 4
    slave_id = 5

    com_port = 6
    baud_rate = 7
    data_bits = 8
    stop_bits = 9

    ip_address = 10
    ip_port = 11

    di_start = 12
    di_size = 13

    coil_start = 14
    coil_size = 15

    ir_start = 16
    ir_size = 17

    hr_read_start = 18
    hr_read_size = 19

    hr_write_start = 20
    hr_write_size = 21

    active = 22

    _count = 23


class SlaveDevicesModel(QtCore.QAbstractTableModel):

    sigLoaded = pyqtSignal()

    def data(self, midx, role):

        rec = self.recs[midx.row()]
        cidx = midx.column()

        if role == Qt.DisplayRole:
            if cidx == C.active:
                return "Yes" if rec['active'] else "-"

            elif cidx == C.dev_id:
                return rec['dev_id']

            elif cidx == C.dev_name:
                return rec['dev_name']

            elif cidx == C.dev_type:
                return rec['dev_type']

            elif cidx == C.conn_type:
                return rec['conn_type']

            elif cidx == C.slave_id:
                return rec['slave_id']

            elif cidx == C.com_port:
                return rec['com_port']
            elif cidx == C.baud_rate:
                return rec['baud_rate']
            elif cidx == C.data_bits:
                return rec['data_bits']
            elif cidx == C.stop_bits:
                return rec['stop_bits']

            elif cidx == C.ip_address:
                return rec['ip_address']
            elif cidx == C.ip_port:
                return rec['ip_port']

            elif cidx == C.di_start:
                return rec['di_start']
            elif cidx == C.di_size:
                return rec['di_size']


            elif cidx == C.ir_start:
                return rec['ir_start']
            elif cidx == C.ir_size:
                return rec['ir_size']

            elif cidx == C.coil_start:
                return rec['coil_start']
            elif cidx == C.coil_size:
                return rec['coil_size']

            elif cidx == C.hr_read_start:
                return rec['hr_read_start']
            elif cidx == C.hr_read_size:
                return rec['hr_read_size']

            elif cidx == C.hr_write_start:
                return rec['hr_write_start']
            elif cidx == C.hr_write_size:
                return rec['hr_write_size']

            elif cidx == C.dev_id:
                return  rec['dev_id']

        if role == Qt.BackgroundRole:
            if cidx == C.active:
                return QtGui.QColor("#D8FFB2") if rec['active'] else QtGui.QColor("white")

    def __init__(self, parent=None, serverConn=None):
        super(QtCore.QAbstractTableModel, self).__init__()

        self.serverConn = serverConn
        self.recs = []


    def columnCount(self, pidx=None):
        return C._count

    def rowCount(self, pidx=None):
        return len(self.recs)

    def headerData(self, idx, orientation, role):
        if role == Qt.DisplayRole:
            return ["", "dev_id", "Name", "Type", "Conn Type", "Slave ID",
                    "Com Port", "Baud Rate", "Data Bits", "Stop Bits",
                    "IP Address", "IP Port",
                    "DI Start", "DI Size",
                    "Coil Start", "Coil Size",
                    "IR Start", "IR Size",
                    "HR Read Start", "HR Read Size",
                    "HR Write Start", "HR Write Size",
                    "Active"
                    ][idx]

    def fetch(self):
         self.serverConn.get(self, "/slave-devices")

    def on_server_reply(self, reply):
        if reply.busy:
            return

        if reply.data == None:
            return

        self.recs = reply.data['slaves']

        self.modelReset.emit()
        self.sigLoaded.emit()

    def upsert(self, rec):
        for idx, r in enumerate(self.recs):
            if r['dev_id'] == rec['dev_id']:
                self.recs[idx] = rec
                self.layoutChanged.emit()
                return
        self.recs.append(rec)
        self.layoutChanged.emit()
