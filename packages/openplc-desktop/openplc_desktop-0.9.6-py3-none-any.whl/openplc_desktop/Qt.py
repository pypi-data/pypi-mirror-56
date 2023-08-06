# -*- coding: utf-8 -*-

#ENGINE = "pyside"
ENGINE = "pyqt5"


if ENGINE == "pyside":

    from PySide2 import QtCore
    from PySide2.QtCore import Qt
    from PySide2.QtCore import Signal as pyqtSignal

    from PySide2 import QtGui
    from PySide2 import QtWidgets

    from PySide2 import QtNetwork




else:

    from PyQt5 import QtCore
    from PyQt5.QtCore import Qt
    from PyQt5.QtCore import pyqtSignal

    from PyQt5 import QtGui
    from PyQt5 import QtWidgets

    from PyQt5 import QtNetwork

    # from PyQt5 import QtWebEngineWidgets


    # from PyQt5 import QtWebSockets
    # from PyQt5 import QtWebKit

    # from PyQt5 import QtSql




