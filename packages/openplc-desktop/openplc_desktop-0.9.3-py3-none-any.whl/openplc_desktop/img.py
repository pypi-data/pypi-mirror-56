# -*- coding: utf-8 -*-

import os
from Qt import  QtWidgets, QtGui
import G


# see https://github.com/spyder-ide/qtawesome

import qtawesome as qta

class Ico():

    caret_down = "fa5s.angle-down"
    help = "fa5s.question-circle"
    node = "fa5s.angle-right"

    commander = "fa5s.solar-panel"
    terminal = "fa5s.desktop"
    return_key = "ei.return-key"
    connect = "fa5s.sign-in-alt"

    add = "fa5s.plus"
    edit = "fa5.edit"
    delete = "fa5.trash-alt"

    cancel = "ei.remove"
    save = "ei.ok-circle"

    settings = "fa5s.cog"
    refresh = "ei.refresh"
    login = "ei.lock"

    start = "fa5s.play"
    stop = "fa5s.stop"

    up = "ei.arrow-up"
    down = "ei.arrow-down"

    quit = "ei.eject"
    clear = "ei.remove-circle"

    filter_on = "fa5s.server"
    filter_off = "fa5s.server"


    server = "fa5s.server"
    servers = "ei.th-list"

    slaves = "fa5s.sitemap"
    slave = "fa5s.microchip"
    mbconfig = "fa5s.cogs"



    programs = "fa5s.window-restore"
    program = "fa5s.file-code"

    users = "fa5s.user-friends"
    user = "fa5s.user"

    @staticmethod
    def icon(name):
        return qta.icon(name)



    @staticmethod
    def logo():
        pth = os.path.join(G.HERE_PATH, "static", "favicon.png")
        return QtGui.QIcon(pth)

    @staticmethod
    def from_path(pth):
          return QtGui.QIcon(pth)