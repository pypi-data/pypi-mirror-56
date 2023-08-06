

from Qt import Qt, QtGui, QtCore, pyqtSignal


class C:
    node = 0

    user_id = 1
    login = 2
    pass_hash = 3
    name = 4
    email = 5

    active = 6
    date_created = 7
    date_updated = 8

    _cols_count = 9


class UsersModel(QtCore.QAbstractTableModel):

    sigLoaded = pyqtSignal()

    def data(self, midx, role):

        rec = self.recs[midx.row()]
        cidx = midx.column()

        if role == Qt.DisplayRole:
            if cidx == C.active:
                return "Yes" if rec['active'] else "-"

            elif cidx == C.user_id:
                return rec['user_id']

            elif cidx == C.login:
                return rec['login']

            elif cidx == C.pass_hash:
                return rec['password_hash']

            elif cidx == C.name:
                return rec['name']

            elif cidx == C.date_created:
                return rec['date_created']

            elif cidx == C.date_updated:
                return rec['date_updated']


        if role == Qt.BackgroundRole:
            if cidx == C.active:
                return QtGui.QColor("#D8FFB2") if rec['active'] else QtGui.QColor("white")

    def __init__(self, parent=None, serverConn=None):
        super(QtCore.QAbstractTableModel, self).__init__()

        self.serverConn = serverConn
        self.recs = []


    def columnCount(self, pidx=None):
        return C._cols_count

    def rowCount(self, pidx=None):
        return len(self.recs)

    def headerData(self, idx, orientation, role):
        if role == Qt.DisplayRole:
            return ["", "UserID", "Syslogin", "Pass", "Full Name", "Email",
                    "Active", "Created", "Updated"][idx]

    def fetch(self):
         self.serverConn.get(self, "/users")

    def on_server_reply(self, reply):
        if reply.busy:
            return

        #print(reply)
        if reply.data == None:
            return

        self.recs = reply.data['users']

        self.modelReset.emit()
        self.sigLoaded.emit()

