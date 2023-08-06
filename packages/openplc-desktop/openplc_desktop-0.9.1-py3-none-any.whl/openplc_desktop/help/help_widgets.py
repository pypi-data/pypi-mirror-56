# -*- coding: utf-8 -*-


import os
import sys
import platform
from Qt import Qt, QtCore, QtGui, QtWidgets, QtWebEngineWidgets, pyqtSignal

from img import Ico
#from core import ut

import cwidgets
import G
import ut


import mistune
from help import DOCS_PATH, TEMPLATES_PATH



class C:
    node = 0
    page = 1


class HelpWidget( QtWidgets.QWidget ):


    def __init__( self, parent=None, page=None):
        QtWidgets.QWidget.__init__( self, parent )


        self.debug = False

        outerLayout = QtWidgets.QVBoxLayout()
        outerLayout.setSpacing( 0 )
        margarine = 0
        outerLayout.setContentsMargins( margarine, margarine, margarine, margarine )
        self.setLayout( outerLayout )

        self.lblTitle = QtWidgets.QLabel()
        self.lblTitle.setText("Help")
        self.lblTitle.setStyleSheet("background-color: #333333; color: #999999; font-size: 19pt; padding: 4px; ")
        outerLayout.addWidget(self.lblTitle, 0)

        outerLayout.addSpacing(5)

        self.splitter = QtWidgets.QSplitter()
        outerLayout.addWidget(self.splitter, 100)

        ## Contents Tree
        self.tree = QtWidgets.QTreeWidget()
        self.splitter.addWidget(self.tree)
        hi = self.tree.headerItem()
        hi.setText(C.node, "File")
        hi.setText(C.page, "Page")

        #self.tree.header().hide()

        self.tree.setColumnHidden(C.page, not self.debug)
        self.tree.header().setStretchLastSection(True)
        self.tree.setUniformRowHeights(True)

        self.tree.setFixedWidth(200)
        self.tree.itemSelectionChanged.connect(self.on_tree_selection)


        ## Tab Widget
        self.tabWidget = QtWidgets.QTabWidget()
        self.splitter.addWidget(self.tabWidget)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.on_tab_close_requested)
        self.tabWidget.currentChanged.connect(self.on_tab_changed)

        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 2)

        self.load_content_tree()

    def init_load(self):
        pass

    def load_content_tree(self):

        self.tree.clear()
        self.tree.setUpdatesEnabled(False)


        item = cwidgets.XTreeWidgetItem()
        item.set(C.node, "Index", ico=Ico.help)

        item.setText(C.page, "index.md" )
        self.tree.addTopLevelItem(item)

        rootNode = self.tree.invisibleRootItem()
        self.load_dir_node(rootNode, DOCS_PATH)

        self.tree.setUpdatesEnabled(True)

        self.load_page("index.md")


    def load_dir_node(self, pItem, pth):

        files = os.listdir(pth)

        for f in sorted(files):
            xpth = os.path.join(pth, f)[len(DOCS_PATH):]
            #print f, xpth
            if f == "index.md" and pth == DOCS_PATH:
                continue
            if os.path.isdir(f):
                item = xtree.XTreeWidgetItem(pItem)
                item.set(C.node, f, ico=Ico.Folder)
                item.setText(C.page, xpth )

                self.load_dir_node(item, os.path.join(pth, f))
                item.setExpanded(True)

            elif f.endswith(".md"):
                item = xtree.XTreeWidgetItem(pItem)
                item.set(C.node, self.title_from_filename(f), ico=Ico.HelpPage)
                item.setText(C.page, xpth )


    # def dpage_path_fn(self, page):
    #     if page.endswith(".md"):
    #         "%s.md" % page
    #     read_fn = os.path.join(DOCS_CONTENT, page )
    #     #if self.debug:
    #     #	print "file_req=", read_fn, self.docs_root()
    #     if not os.path.exists(read_fn):
    #         print("ERROR: FILE not exits", read_fn)
    #         return

    def title_from_filename(self, fn):
        fn = os.path.basename(fn)
        if fn.endswith(".md"):
            fn = fn[0:-3]
        return fn.replace("_", " ").title()

    def select_page(self, page):
        if self.debug:
            print("select_page", page, self.tabWidget.count())
        idx = None
        if self.tabWidget.count() == 0:
            return idx
        ## check page is aleady loaded, and select
        for i in range(0, self.tabWidget.count()):
            if self.debug:
                print("i=", i, self.tabWidget.widget(i).page, page, self.tabWidget.widget(i).page == page)
            if self.tabWidget.widget(i).page == page:
                self.tabWidget.blockSignals(True)
                self.tabWidget.setCurrentIndex(i)
                self.tabWidget.blockSignals(False)
                idx = i
                if self.debug:
                    print("idx=", idx)
                break
        items = self.tree.findItems(page, Qt.MatchExactly|Qt.MatchRecursive, C.page)
        if len(items) > 0:
            self.tree.blockSignals(True)
            self.tree.setCurrentItem(items[0])
            self.tree.blockSignals(False)
        if self.debug:
            print("items=", idx, items)
        return idx



    def load_page(self, page):

        page = str(page)

        full_path = os.path.join(DOCS_PATH, page)
        if self.debug:
            print("------------------\nload_page=", page, full_path)
        if os.path.isdir(full_path):
            return
        elif not page.endswith(".md"):
            full_path = full_path + ".md"


        idx =  self.select_page(page)
        if idx != None:
            return

        if not os.path.exists(full_path):
            #print "ERROR: FILE not exits", full_path
            return

        container = ut.read_file( os.path.join(TEMPLATES_PATH, "help_container.html") )

        txt = ut.read_file(full_path)
        html = mistune.markdown(txt, escape=False)

        out_html = container.replace("##++CONTENT++##", html)



        self.tabWidget.blockSignals(True)
        if self.debug:
            print("## create view")
        webView = HelpPageView()
        nidx = self.tabWidget.addTab(webView, self.title_from_filename(page))
        webView.set_data(page, out_html )
        self.tabWidget.setTabIcon(nidx, Ico.icon(Ico.help))

        webView.sigPageLinkClicked.connect(self.load_page)

        self.tabWidget.setCurrentIndex(nidx)
        self.select_tree_node(page)
        if self.debug:
            print("## view done")
        self.tabWidget.blockSignals(False)




    def on_tree_selection(self):
        item = self.tree.currentItem()
        if item == None:
            return
        self.load_page( item.s(C.page) )


    def on_tab_close_requested(self, idx):
        if self.debug:
            print("on_tab_close_requested", idx)
        self.tabWidget.removeTab(idx)

    def on_tab_changed(self, nidx):
        if nidx == -1:
            self.tree.blockSignals(True)
            self.tree.clearSelection()
            self.tree.blockSignals(False)
            return
        page = self.tabWidget.widget(nidx).page
        self.select_tree_node(page)

    def select_tree_node(self, page, block=True):

        self.tree.blockSignals(True)
        items = self.tree.findItems(page, Qt.MatchExactly|Qt.MatchRecursive, C.page)
        if self.debug:
            print("select_tree_node", page, items)
        if len(items) > 0:
            self.tree.setCurrentItem(items[0])
        else:
            # page not in menu
            pass #print ere
        self.tree.blockSignals(False)

class HelpPageView( QtWidgets.QWidget ):

    sigPageLinkClicked = pyqtSignal(str)

    def __init__( self, parent=None, page=None):
        QtWidgets.QWidget.__init__( self, parent )

        self.debug = True
        self.page = None

        lay = QtWidgets.QVBoxLayout()
        lay.setSpacing(0)
        lay.setContentsMargins(0,0,0,0)
        self.setLayout(lay)

        self.webView = QtWebEngineWidgets.QWebEngineView()
        lay.addWidget(self.webView, 2)


        #self.webView.page().javaScriptConsoleMessage()
        # if self.debug:
        #     page = self.webView.page()
        #     page.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.JavascriptEnabled, True)
        #     #elf.webView.settings().globalSettings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
        #
        #     self.webInspector = QtWebEngineWidgets.QWebEngineProfile(self)
        #     self.webInspector.set(page)
        #     lay.addWidget(self.webInspector, 3)



        #self.webView.page().setLinkDelegationPolicy(QtWebEngineWidgets.QWebPage.DelegateAllLinks)
        #self.webView.linkClicked.connect(self.on_link_clicked)



    def on_console(self, v):
        print(v)

    def set_data(self, page, html ):
        self.page = page
        base_url = QtCore.QUrl.fromLocalFile( G.STATIC_PATH  + "/" )
        #bu.setScheme("file")
        #print "  > out stuff=", base_url.toString(), base_url.isValid()
        self.webView.setHtml(html, base_url)

    def on_link_clicked(self, url):

        page = str(url.path())[1:]
        #print url,  page, type(page)
        self.sigPageLinkClicked.emit( page )
