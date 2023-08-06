# -*- coding: utf-8 -*-

import os
import re
from Qt import QtCore, QtWidgets, QtGui, Qt, pyqtSignal

from img import Ico
import G
import ut

import cwidgets


class INIEditorWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)



        self.mainLayout = cwidgets.vlayout()
        self.setLayout(self.mainLayout)

        self.txtEdit = QtWidgets.QPlainTextEdit()
        self.mainLayout.addWidget(self.txtEdit)
        f = self.txtEdit.font()
        f.setFamily("monospace")
        f.setPointSize(9)
        self.txtEdit.setFont(f)

        syntax = BasicIniHighlighter(self.txtEdit.document())



    def init_load(self):

        p = os.path.join(G.STATIC_PATH, "example.ini")
        s = ut.read_file(p)
        self.txtEdit.setPlainText(s)


class BasicIniHighlighter(QtGui.QSyntaxHighlighter):
    '''
    QSyntaxHighlighter class for use with QTextEdit for highlighting
    ini config files.

    I looked high and low to find a high lighter for basic ini config
    format, so I'm leaving this in the project even though I'm not
    using.
    '''

    def __init__(self, parent, theme=None):
        QtGui.QSyntaxHighlighter.__init__(self, parent)
        self.parent = parent

        self.highlightingRules = []

        # keyword
        self.highlightingRules.append(HighlightingRule(r"^[^:=\s][^:=]*[:=]",
                                                       Qt.blue,
                                                       Qt.SolidPattern))

        # section
        self.highlightingRules.append(HighlightingRule(r"^\[[^\]]+\]",
                                                       Qt.red,
                                                       Qt.SolidPattern))

        # comment
        self.highlightingRules.append(HighlightingRule(r"#[^\n]*",
                                                       Qt.darkYellow,
                                                       Qt.SolidPattern))

    def highlightBlock(self, text):
        for rule in self.highlightingRules:
            for match in rule.pattern.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), rule.highlight)
        self.setCurrentBlockState(0)


class HighlightingRule():
    def __init__(self, pattern, color, style):
        if isinstance(pattern, str):
            self.pattern = re.compile(pattern)
        else:
            self.pattern = pattern
        charfmt = QtGui.QTextCharFormat()
        brush = QtGui.QBrush(color, style)
        charfmt.setForeground(brush)
        self.highlight = charfmt