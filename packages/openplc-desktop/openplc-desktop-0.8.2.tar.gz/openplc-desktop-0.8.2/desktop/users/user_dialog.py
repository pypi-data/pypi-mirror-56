# -*- coding: utf-8 -*-

from Qt import QtCore, QtWidgets, Qt, pyqtSignal

from img import Ico

import cwidgets



class UserDialog(QtWidgets.QDialog):

    sigSaved = pyqtSignal(dict)
    sigDeleted = pyqtSignal(str)

    @property
    def url(self):
        return "/users/%s" % self.user_id

    def __init__(self, parent=None, serverConn=None, user_id=None):
        super().__init__(parent)

        assert serverConn != None
        assert user_id != None

        self.serverConn = serverConn
        self.user_id = user_id

        self.setWindowTitle("User")
        self.setWindowIcon(Ico.icon(Ico.user))
        self.setMinimumWidth(500)
        #self.setMinimumHeight(600)


        self.mainLayout = cwidgets.vlayout(margin=20)
        self.setLayout(self.mainLayout)


        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(10)
        self.mainLayout.addLayout(self.grid)


        row = 0
        self.chkActive = QtWidgets.QCheckBox()
        self.chkActive.setText("Active")
        self.grid.addWidget(self.chkActive, row, 1)

        row += 1
        self.grid.addWidget(QtWidgets.QLabel("Login"), row, 0, Qt.AlignRight)
        self.txtLogin = cwidgets.XLineEdit()
        self.grid.addWidget(self.txtLogin, row, 1, 1, 1)

        row += 1
        self.grid.addWidget(QtWidgets.QLabel("Full Name"), row, 0, Qt.AlignRight)
        self.txtName = cwidgets.XLineEdit()
        self.grid.addWidget(self.txtName, row, 1, 1, 2)

        row += 1
        self.grid.addWidget(QtWidgets.QLabel("Email"), row, 0, Qt.AlignRight)
        self.txtEmail = cwidgets.XLineEdit()
        self.grid.addWidget(self.txtEmail, row, 1, 1, 2)

        row += 1
        self.chkPass = QtWidgets.QCheckBox("Set Password")
        self.grid.addWidget(self.chkPass, row, 1, 1, 1)
        self.chkPass.stateChanged.connect(self.on_set_pass)

        row += 1
        self.grid.addWidget(QtWidgets.QLabel("Password"), row, 0, Qt.AlignRight)
        self.txtPass = cwidgets.XLineEdit()
        self.grid.addWidget(self.txtPass, row, 1, 1, 1)
        self.txtPass.setDisabled(True)





        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 1)
        self.grid.setColumnStretch(2, 2)

        self.formBar = cwidgets.FormActionBar(self)
        self.mainLayout.addWidget(self.formBar)

        self.init_load()

    def init_load(self):
        self.serverConn.get(self, self.url)

    def on_server_reply(self, reply):

        if reply.busy:
            return
        print(reply.data, reply.error)
        if reply.post:
            print(reply.data)
            if reply.data.get("saved") == True:
                self.sigSaved.emit(reply.data['user'])
                self.accept()
            return

        self.formBar.set_reply(reply)

        rec = reply.data.get('user')

        self.chkActive.setChecked(rec['active'])
        self.txtLogin.setText(rec['login'])
        self.txtName.setText(rec['name'])
        self.txtEmail.setText(rec['email'])

        if rec['user_id'] == "new":
            self.chkPass.setChecked(True)
            self.chkPass.setDisabled(True)


        self.formBar.set_meta("user_id", rec)

        self.setDisabled(False)
        self.txtName.setFocus()



    def on_cancel(self):
        self.reject()

    def on_save(self):

        if self.txtLogin.s() == "":
            self.txtLogin.setFocus()
            return

        if self.chkPass.isChecked() and self.txtPass.s() == "":
            self.txtPass.setFocus()
            return

        rec = dict(active=self.chkActive.isChecked(),
                   login=self.txtLogin.s(),
                   name=self.txtName.s(),
                   email=self.txtEmail.s()
                   )
        if self.chkPass.isChecked():
            rec['password'] = self.txtPass.s()

        self.serverConn.post(self, self.url, data=rec)


    def on_delete(self):
        self.sigDeleted.emit(self.user_id)
        self.accept()

    def on_set_pass(self, state=False):
        self.txtPass.setEnabled(self.chkPass.isChecked())