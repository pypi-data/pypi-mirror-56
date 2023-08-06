# -*- coding: utf-8 -*-

from Qt import QtCore, QtWidgets, Qt, pyqtSignal

from img import Ico

import cwidgets



class ProgramDialog(QtWidgets.QDialog):

    sigSaved = pyqtSignal(dict)
    sigDeleted = pyqtSignal(str)

    @property
    def url(self):
        return "/programs/%s" % self.prog_id

    def __init__(self, parent=None, serverConn=None, prog_id=None):
        super().__init__(parent)

        assert serverConn != None
        assert prog_id != None

        self.serverConn = serverConn
        self.prog_id = prog_id

        self.setWindowTitle("User")
        self.setWindowIcon(Ico.icon(Ico.user))
        self.setMinimumWidth(500)



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
        self.grid.addWidget(QtWidgets.QLabel("Name"), row, 0, Qt.AlignRight)
        self.txtName = cwidgets.XLineEdit()
        self.grid.addWidget(self.txtName, row, 1, 1, 2)

        row += 1
        self.grid.addWidget(QtWidgets.QLabel("Description"), row, 0, Qt.AlignRight|Qt.AlignTop)
        self.txtDescription = QtWidgets.QTextEdit()
        self.txtDescription.setFixedHeight(100)
        self.grid.addWidget(self.txtDescription, row, 1, 1, 2)



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

        print(reply.data)
        if reply.post:

            if reply.data.get("saved") == True:
                self.sigSaved.emit(reply.data['program'])
                self.accept()
            return

        self.formBar.set_reply(reply)

        rec = reply.data.get('program')

        self.chkActive.setChecked(rec['active'])
        self.txtDescription.setText(rec['description'])
        self.txtName.setText(rec['name'])
        #self.txtEmail.setText(rec['email'])

        self.formBar.set_meta("prog_id", rec)

        self.setDisabled(False)
        self.txtName.setFocus()



    def on_cancel(self):
        self.reject()

    def on_save(self):

        if self.txtName.len() < 4:
            self.txtName.setFocus()
            return


        rec = dict(active=self.chkActive.isChecked(),
                   description=self.txtDescription.toPlainText(),
                   name=self.txtName.s(),
                   prog_id= self.prog_id
                   )

        self.serverConn.post(self, self.url, data=rec)


    def on_delete(self):
        self.sigDeleted.emit(self.user_id)
        self.accept()

    def on_set_pass(self, state=False):
        self.txtPass.setEnabled(self.chkPass.isChecked())