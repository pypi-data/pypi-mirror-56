# -*- coding: utf-8 -*-

## Custom and Extended widgets

from Qt import QtCore, QtGui, QtWidgets, Qt, pyqtSignal
from img import Ico

DEFAULT_SPACING = 0
DEFAULT_MARGIN = 0
DEFAULT_BUTTON_WIDTH = 80



#=====================================================
# Layouts

def hlayout(spacing=DEFAULT_SPACING, margin=DEFAULT_MARGIN):
    """Convenience function to create a QHBoxLayout"""
    lay = QtWidgets.QHBoxLayout()
    if isinstance(margin, bool):
        margin = DEFAULT_SPACING
    if isinstance(spacing, bool):
        spacing = DEFAULT_SPACING
    lay.setContentsMargins(margin, margin, margin, margin)
    lay.setSpacing(spacing)
    return lay

def vlayout(spacing=DEFAULT_SPACING, margin=DEFAULT_MARGIN):
    """Convenience function to create a QVBoxLayout"""
    lay = QtWidgets.QVBoxLayout()
    if isinstance(margin, bool):
        margin = DEFAULT_SPACING
    if isinstance(spacing, bool):
        spacing = DEFAULT_SPACING
    lay.setContentsMargins(margin, margin, margin, margin)
    lay.setSpacing(spacing)
    return lay


class CancelButton( QtWidgets.QPushButton ):
    def __init__( self, parent, text="Cancel", callback=None ):
        QtWidgets.QPushButton.__init__( self, parent )

        self.setText( text )
        self.setIcon( Ico.icon( Ico.cancel ) )
        if callback:
            self.clicked.connect(callback)
            return
        self.clicked.connect(parent.on_cancel)

class SaveButton( QtWidgets.QPushButton ):
    def __init__( self, parent, text="Save", ico=None, callback=None, width=None):
        super().__init__( parent )

        if width:
            self.setMinimumWidth( width )
        self.setText( text )
        self.setIcon( Ico.icon( ico if ico else Ico.save ) )

        if callback:
            self.clicked.connect(callback)
        else:
            self.clicked.connect(parent.on_save)

class DeleteButton( QtWidgets.QPushButton ):
    def __init__( self, parent, text="Delete", callback=None ):
        QtWidgets.QPushButton.__init__( self, parent )

        self.setText( text )
        self.setIcon( Ico.icon( Ico.delete ) )
        if callback:
            self.clicked.connect(callback)
            return
        self.clicked.connect(parent.on_delete)



class FormActionBar(QtWidgets.QWidget):

    def __init__(self, parent, delete=False, show_meta=True):
        super().__init__(parent)

        self.show_meta = show_meta

        self.mainLayout = vlayout(margin=5, spacing=10)
        self.setLayout(self.mainLayout)



        #---
        self.buttLay = hlayout(spacing=5)
        self.mainLayout.addLayout(self.buttLay)

        if delete:
            self.buttDelete = DeleteButton(parent)
            self.buttLay.addWidget(self.buttDelete)

        self.statusBar = StatusBar(self, refresh=False)
        self.buttLay.addWidget(self.statusBar)

        self.buttCancel = CancelButton(parent)
        self.buttLay.addWidget(self.buttCancel)


        self.buttSave = SaveButton(parent)
        self.buttLay.addWidget(self.buttSave)



        # ---
        if show_meta:
            self.metaLay = hlayout(spacing=5)
            self.mainLayout.addLayout(self.metaLay)

            self.lblIDName = QtWidgets.QLabel()
            self.metaLay.addWidget(self.lblIDName)
            self.lblID = QtWidgets.QLabel()
            self.metaLay.addWidget(self.lblID)
            self.lblID.setFrameStyle(QtWidgets.QFrame.Sunken | QtWidgets.QFrame.Panel)

            self.metaLay.addWidget(QtWidgets.QLabel("Created:"))
            self.lblCreated = QtWidgets.QLabel()
            self.metaLay.addWidget(self.lblCreated)
            self.lblCreated.setFrameStyle(QtWidgets.QFrame.Sunken | QtWidgets.QFrame.Panel)

            self.metaLay.addWidget(QtWidgets.QLabel("Updated:"))
            self.lblUpdated = QtWidgets.QLabel()
            self.metaLay.addWidget(self.lblUpdated)
            self.lblUpdated.setFrameStyle(QtWidgets.QFrame.Sunken | QtWidgets.QFrame.Panel)

            self.metaLay.addStretch(2)


    def set_meta(self, id_fld, rec):
        if not self.show_meta: # should never appen
            return
        self.lblIDName.setText(id_fld)
        self.lblID.setText(rec[id_fld])
        self.lblCreated.setText("%s" % rec["date_created"])
        self.lblUpdated.setText("%s" % rec["date_updated"])


    def set_reply(self, reply):
        self.statusBar.set_reply(reply)



class XToolButton( QtWidgets.QToolButton ):

    def __init__( self, parent=None, colors=None, style=None,
                    autoRaise=True, menu=None,
                    text="", tooltip=None, ico=None, iconTop=False, iconSize=16,
                    bold=False, disabled=False,
                    width=None, popup=False,
                    callback=None, ki=None,
                    both=True, checkable=False
                    ):

        QtWidgets.QToolButton.__init__(self, parent)

        self.colors = colors


        if ki:
            self.setProperty("ki", ki)

        if width:
            self.setFixedWidth(width)

        if style:
            self.setStyleSheet(style)

        if disabled:
            self.setDisabled(True)


        if both:
            if iconTop:
                self.setToolButtonStyle( Qt.ToolButtonTextUnderIcon)
            else:
                self.setToolButtonStyle( Qt.ToolButtonTextBesideIcon)
        else:
            self.setToolButtonStyle( Qt.ToolButtonIconOnly)

        if checkable:
            self.setCheckable(True)

        if callback:
            self.clicked.connect(callback)

        if tooltip:
            self.setToolTip(tooltip)

        if text:
            self.setText(text)

        #== Font
        # Try and avoid styleSheet maybe
        if bold:
            self.setBold(bold)
        # < font

        if ico:
            self.setIco(ico)
            if iconSize:
                if isinstance(iconSize, list):
                    self.setIconSize( QtCore.QSize(iconSize[0],iconSize[0]))
                else:
                    self.setIconSize( QtCore.QSize(iconSize, iconSize))

        self.setAutoRaise(autoRaise)
        if popup:
            self.setPopupMode(QtWidgets.QToolButton.InstantPopup)

        if menu:
            self.setMenu(QtWidgets.QMenu())

    def setIco(self, ico, iconSize=16):
        self.setIcon(Ico.icon(ico))
        self.setIconSize( QtCore.QSize(iconSize, iconSize))

    def setEnabled(self, state):
        if self.colors:
            color = self.colors[1] if state else self.colors[0]
            self.setStyleSheet("background-color: %s" % color)
        QtWidgets.QToolButton.setEnabled(self, state)

    def setBold(self, state):
        f = self.font()
        f.setBold(state)
        self.setFont(f)



C_FG = "color: #222222;"
C_BG = "background-color: white;"

C_FG_FOCUS = "color: black;"
C_BG_FOCUS = "background-color: #FFFA93"



class XLineEdit( QtWidgets.QLineEdit ):

    sigFocused = pyqtSignal(bool)
    sigMove = pyqtSignal(bool)
    sigDoubleClicked = pyqtSignal()

    def __init__( self, parent=None, show_focus=False, width=None,
                  dirty=True, changed=None ):
        QtWidgets.QLineEdit.__init__(self, parent )

        self._show_focus = show_focus

        if width:
            self.setFixedWidth(width)

        if dirty:
            if hasattr(parent, "set_dirty"):
                self.textChanged.connect(parent.set_dirty)
        if changed:
            self.textChanged.connect(changed)

    def stripped(self):
        self.setText( self.text().strip() )
        return self.text()

    def s(self):
        return self.stripped()

    def len(self):
        return len(self.text().strip())

    def setText(self, txt):
        if txt == None:
            self.setText("")
            return
        super().setText(txt.strip())

    def set_bold(self, state):
        f = self.font()
        f.setBold(state)
        self.setFont(f)

    def mouseDoubleClickEvent_MAYBE(self, ev):
        ev.ignore()
        self.sigDoubleClicked.emit(ev)

    def focusInEvent(self, ev):
        """Changes style if show_focus """
        if self._show_focus:
            self.setStyleSheet(C_FG_FOCUS + C_BG_FOCUS)
        QtWidgets.QLineEdit.focusInEvent(self, ev)
        self.sigFocused.emit(True)

    def focusOutEvent(self, ev):
        """Changes style if show_focus """
        if self._show_focus:
            self.setStyleSheet(C_FG + C_BG)

        QtWidgets.QLineEdit.focusOutEvent(self, ev)
        self.sigFocused.emit(False)


    def keyPressEvent(self, ev):
        """Clear field with esc, otherwise passthough"""
        if ev.key() == Qt.Key_Escape:
            self.setText("")
            return
        if ev.key() == Qt.Key_Up:
            self.sigMove.emit(False)
            return
        if ev.key() == Qt.Key_Down:
            self.sigMove.emit(True)
            return
        QtWidgets.QLineEdit.keyPressEvent( self, ev )

class XToolBar(QtWidgets.QToolBar):

    def __init__( self, parent=None):
        QtWidgets.QToolBar.__init__(self, parent)

    def addStretch(self):

        widget = QtWidgets.QWidget()
        sp = QtWidgets.QSizePolicy()
        sp.setHorizontalPolicy(QtWidgets.QSizePolicy.Expanding)
        widget.setSizePolicy(sp)

        self.addWidget(widget)


class ToolBarGroup(QtWidgets.QWidget):
    def __init__(self, parent=None, title=None, width=None, hide_labels=False, bg='#999999',
                 is_group=False, toggle_icons=False, toggle_callback=None):
        QtWidgets.QWidget.__init__(self, parent)

        if width:
            self.setFixedWidth(width)

        self.icon_on = Ico.filter_on
        self.icon_off = Ico.filter_off
        self.toggle_icons = toggle_icons
        self.toggle_callback = toggle_callback
        self.hide_labels = hide_labels

        self.buttonGroup = None
        self.is_group = is_group
        if self.is_group:
            self.buttonGroup = QtWidgets.QButtonGroup()
            self.buttonGroup.setExclusive(True)
            if self.toggle_callback:
                self.buttonGroup.buttonClicked.connect(self.on_button_clicked)

        self.group_var = None
        self.callback = None
        self.show_icons = True
        self.icon_size = 12
        self.bg_color = bg

        ## Main Layout
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        self.setLayout(mainLayout)

        ## Label
        self.label = QtWidgets.QLabel()
        #bg = "#8F8F8F"  ##eeeeee"
        fg = "#eeeeee"  ##333333"
        lbl_sty = "background: %s; " % self.bg_color  # qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #fefefe, stop: 1 #CECECE);"
        lbl_sty += " color: %s; font-size: 8pt; padding: 1px;" % fg  # border: 1px outset #cccccc;"
        self.label.setStyleSheet(lbl_sty)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setFixedHeight(20)
        mainLayout.addWidget(self.label)

        ## Toolbar
        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolbar.setFixedHeight(30)

        mainLayout.addWidget(self.toolbar)

        if title:
            self.set_title(title)
        #print(ere)
    def set_title(self, title):
        self.label.setText("%s" % title)

    def addWidget(self, widget):
        self.toolbar.addWidget(widget)
        return widget

    def addAction(self, act):
        self.toolbar.addAction(act)

    def addButton(self, ico=None, text=None, callback=None, idx=None, toggle_callback=None, tooltip=None,
                  ki=None, bold=False, checkable=False, checked=None, width=None, return_action=False):

        butt = XToolButton()

        if self.is_group:
            if idx != None:
                self.buttonGroup.addButton(butt, idx)
            else:
                self.buttonGroup.addButton(butt)
        if self.hide_labels == False:
            if text != None:
                butt.setText(text)
        if text == None:
            butt.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        else:
            butt.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        if tooltip:
            butt.setToolTip(tooltip)

        if self.toggle_icons:
            butt.setIconSize(QtCore.QSize(10, 10))
            butt.setIcon(Ico.icon(self.icon_off))
        if ico:
            butt.setIcon(Ico.icon(ico))
            butt.setIconSize(QtCore.QSize(10, 10))

        butt.setCheckable(checkable)
        if checked != None:
            butt.setChecked(checked)


        butt.setProperty("ki", ki)
        nuAct = self.toolbar.addWidget(butt)
        if callback:
            self.connect(butt, QtCore.SIGNAL("clicked()"), callback)
        #if toggle_callback:
        #   self.connect(butt, QtCore.SIGNAL("toggled(bool)"), toggle_callback)
        if bold:
            self.set_bold(butt)
        if width:
            butt.setFixedWidth(width)

        self.on_button_clicked(block=True)

        if return_action:
            return nuAct
        return butt

    def set_bold(self, w):
        f = w.font()
        f.setBold(True)
        w.setFont(f)

    def on_button_clicked(self, butt=None, block=False):
        if self.is_group:
            for b in self.buttonGroup.buttons():
                b.setIcon( Ico.icon(self.icon_on if b.isChecked() else self.icon_off) )

                if block == False and b.isChecked():
                    if self.toggle_callback:
                        self.toggle_callback(self.buttonGroup.id(b))

    def get_id(self):
        id = self.buttonGroup.checkedId()
        if id == -1:
            return None
        return id



class XLabel(QtWidgets.QLabel):

    sigClicked = pyqtSignal()
    sigDoubleClicked = pyqtSignal()

    def __init__( self, parent=None, bold=False,
                  style=None, base_style="", align=None,
                  text=None, frame=None,
                  wrap=False, hover_color=None,
                  height=None, width=None):
        QtWidgets.QLabel.__init__( self, parent )

        self.hover_color = hover_color

        self.base_style = base_style
        self.style = ""
        if style != None:
            self.style = style
        self.setStyleSheet(self.style)

        if bold:
            f = self.font()
            f.setBold(True)
            self.setFont(f)

        if align != None:
            self.setAlignment(align)

        if text:
            self.setText(text)

        if height:
            self.setFixedHeight(height)
        if width:
            self.setFixedWidth(width)

        self.setWordWrap(wrap)

        if frame:
            self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)

        if self.hover_color:
            self.set_border("#dddddd")

    def setStyleSheet(self, sty):
        QtWidgets.QLabel.setStyleSheet(self, sty + self.base_style)



class StatusBar(QtWidgets.QWidget):
    """A QWidget with many embedded widgets for StatusBar"""

    sigRefresh = pyqtSignal()

    def __init__(self, parent, refresh=True, status=True,
                 pager=False, mode=True):
        QtWidgets.QWidget.__init__(self, parent)

        if isinstance(parent, bool):
            print("STATUSBar is not correct parent")
            # print Tantrum
            return

        self._lastReply = None

        self._refresh = refresh
        self._status = status

        self.mainLayout = QtWidgets.QHBoxLayout()
        m = 0
        self.mainLayout.setContentsMargins(m, m, m, m)
        self.setLayout(self.mainLayout)


        ##=======================================================================
        ## Status Bar
        self.statusBar = QtWidgets.QStatusBar()
        self.statusBar.setSizeGripEnabled(False)
        self.showMessage(" ")
        self.mainLayout.addWidget(self.statusBar, 1)

        ## Main layout to add
        self.extrasLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.extrasLayout, 0)

        ## Status widget setup

        self.lblStatus = QtWidgets.QLabel()
        self.lblStatus.setFixedWidth(30)
        self.lblStatus.setStyleSheet("background-color: yellow;")
        self.mainLayout.addWidget(self.lblStatus)


        #== Progress Bar
        progressWidget = QtWidgets.QWidget()
        progressWidget.setFixedWidth(40)
        #progressWidget.setMaximumWidth(200)
        self.mainLayout.addWidget(progressWidget)

        progressLayout = QtWidgets.QHBoxLayout()
        m = 0
        progressLayout.setContentsMargins(m, m, m, m)
        progressWidget.setLayout(progressLayout)

        self.progress = QtWidgets.QProgressBar(self)
        # self.progress.setFixedWidth( 40 )
        self.progress.setFixedHeight(15)
        # self.setContentsMargins( m, m, m, m )
        self.progress.setMinimum(0)
        self.progress.setMaximum(1)
        self.progress.setInvertedAppearance(False)
        self.progress.setTextVisible(False)
        self.progress.setVisible(False)
        # self.connect( self.progress, QtCore.SIGNAL('valueChanged(int)'), self.on_progress_value_changed)
        progressLayout.addWidget(self.progress)


        ################################################################
        ## Refrehsing Button
        self.buttRefresh = None
        self.popMenu = None
        if refresh:
            self.buttRefresh = QtWidgets.QToolButton()
            self.mainLayout.addWidget(self.buttRefresh)

            self.buttRefresh.setIcon(Ico.icon(Ico.refresh))
            # self.buttRefresh.setFlat(True)
            self.buttRefresh.setAutoRaise(True)
            self.buttRefresh.setIconSize(QtCore.QSize(16, 16))
            self.buttRefresh.setStyleSheet("padding: 0px;")
            self.buttRefresh.clicked.connect(self.on_refresh)
            if hasattr(parent, "on_refresh"):
                self.buttRefresh.clicked.connect(parent.on_refresh)




    def on_refresh(self):
        self.sigRefresh.emit()



    ###################################################################
    def showMessage(self, mess, timeout=None, warn=None, info=None):
        # print "showMessage=", mess
        if warn:
            self.statusBar.setStyleSheet("color: #990000;")
        elif info:
            self.statusBar.setStyleSheet("color: #3361C2;")
        else:
            self.statusBar.setStyleSheet("")

        if timeout == None:
            self.statusBar.showMessage(mess)
        else:
            self.statusBar.showMessage(mess, timeout)

    def addWidget(self, widget):
        self.extrasLayout.addWidget(widget)

    def addPermanentWidget(self, widget):
        self.mainLayout.addWidget(widget)

    def insertPermanentWidget(self, idx, widget):
        self.statusBar.insertPermanentWidget(idx, widget)


    def set_status(self, sta):
        self.lblStatus.setText(sta.status)
        if sta.busy == False:
            self.progress_stop()
            return

        self.progress_start()

    def set_reply(self, reply):
        self.lblStatus.setText(reply.status)
        if reply.busy:
            self.progress_start()
            return

        self.progress_stop()
        self._reply = reply
        if reply.error:
            self.showMessage(reply.error, warn=True)

    def progress_start(self):
        self.progress.setMaximum(0)
        self.progress.setVisible(True)
        if self.buttRefresh:
            self.buttRefresh.setDisabled(True)

    def progress_stop(self):
        self.progress.setVisible(False)
        self.progress.setMaximum(1)
        if self.buttRefresh:
            self.buttRefresh.setDisabled(False)

    def set_busy(self, state):
        if state:
            self.progress_start()
        else:
            self.progress_stop()


