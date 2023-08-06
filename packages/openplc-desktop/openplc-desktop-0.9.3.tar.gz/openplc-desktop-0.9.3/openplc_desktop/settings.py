# -*- coding: utf-8 -*-

import os
import urllib
import json

from Qt import Qt, QtCore


class XSettings( QtCore.QSettings ):

    CURR_SERVER_KI = "current/server_ki"

    def __init__( self, parent=None ):
        QtCore.QSettings.__init__( self, "OpenPLC", "openplc-desktop-pyqt")

        self.server_auth = False


    def servers_list(self):
        v = self.value("servers")
        if not v:
            return []
        return list(v.values())

    def save_server(self, srv):
        servs = self.value("servers")
        if not servs:
            servs = {}
        servs[srv['name']] = srv
        self.setValue("servers", servs)
        self.sync()

    def remove_server(self, srv):
        servs = self.qsettings.value("servers")
        if not servs:
            servs = {}
        if srv['name'] in servs:
            del servs[srv['name']]
        self.setValue("servers", servs)
        self.sync()

    ##==============================
    ## Window Save/Restore
    def save_window( self, window ):
        name = window.objectName()
        if len(name) == 0:
            return
        self.setValue( "window/%s/geometry" % name, QtCore.QVariant( window.saveGeometry() ) )

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
        v = self.value("splitter/%s" % wname)
        if v:
            splitter.restoreState(v)

    def save_list(self, key, lst):
        self.setValue(key, json.dumps(lst))
        self.sync()

    def get_list(self, key):
        s = self.value(key)
        if s == None or s == "":
            return []
        return json.loads(s)


