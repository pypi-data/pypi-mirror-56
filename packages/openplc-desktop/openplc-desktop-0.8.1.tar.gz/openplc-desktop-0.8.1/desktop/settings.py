# -*- coding: utf-8 -*-

import os
import urllib
import json

from Qt import Qt, QtCore




class XSettings( QtCore.QObject ):

    CURR_SERVER_KI = "current/server_ki"

    def __init__( self, parent=None ):
        QtCore.QObject.__init__( self, parent )

        self.qsettings = QtCore.QSettings("OpenPLC", "openplc-desktop-pyqt")


        self.server_auth = False


    def servers_list(self):
        v = self.qsettings.value("servers")
        if not v:
            return []
        return list(v.values())

    def save_server(self, srv):
        servs = self.qsettings.value("servers")
        if not servs:
            servs = {}
        servs[srv['name']] = srv
        self.qsettings.setValue("servers", servs)
        self.qsettings.sync()

    def remove_server(self, srv):
        servs = self.qsettings.value("servers")
        if not servs:
            servs = {}
        if srv['name'] in servs:
            del servs[srv['name']]
        self.qsettings.setValue("servers", servs)
        self.qsettings.sync()

    ##==============================
    ## Window Save/Restore
    def save_window( self, window ):
        name = window.objectName()
        if len(name) == 0:
            return
        self.qsettings.setValue( "window/%s/geometry" % name, QtCore.QVariant( window.saveGeometry() ) )

    def restore_window( self, window ):
        name = str(window.objectName())
        if len(name) == 0:
            return
        window.restoreGeometry( self.qsettings.value( "window/%s/geometry" % name ) )


    def save_splitter(self, splitter):
        wname = str(splitter.objectName())
        if not wname:
            print ("Splitter has no name", splitter)
        self.qsettings.setValue("splitter/%s" % wname, splitter.saveState())

    def restore_splitter(self, splitter):
        wname = str(splitter.objectName())
        if not wname :
            print ("Splitter has no name")
            return
        v = self.qsettings.value("splitter/%s" % wname)
        if v:
            splitter.restoreState(v)

    def save_list(self, key, lst):
        self.qsettings.setValue(key, json.dumps(lst))
        self.qsettings.sync()

    def get_list(self, key):
        s = self.qsettings.value(key)
        if s == None or s == "":
            return []
        return json.loads(s)


