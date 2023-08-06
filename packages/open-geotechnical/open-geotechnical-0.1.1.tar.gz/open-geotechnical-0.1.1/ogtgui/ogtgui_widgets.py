# -*- coding: utf-8 -*-


import os
import collections

from Qt import QtGui, QtWidgets, QtCore, Qt, pyqtSignal

import xwidgets
from img import Ico
from ogt import ags4
from ogt.ogt_validate import OGTError
#from ogt import CELL_COLORS, HAVE_EXCEL
import ogtgui_excel
import ogtgui_errors



import app_globals as G

def bg_color(descr):
    if descr == ags4.AGS4.GROUP:
        return "#D4C557"

    if descr == ags4.AGS4.HEADING:
        return "#FCF66D"

    if descr in [ags4.AGS4.UNIT, ags4.AGS4.TYPE]:
        return "#FFE8B9"

    if descr == ags4.AGS4.DATA:
        return "#DFD1FF"

    return "#ffffff"

class FILTER_ROLE:
    warn = Qt.UserRole + 3
    err = Qt.UserRole + 5


class C_EG:
    """Columns for examples"""
    file_name = 0

class ExamplesWidget( QtWidgets.QWidget ):

    sigFileSelected = pyqtSignal(object)

    def __init__( self, parent):
        QtWidgets.QWidget.__init__( self, parent )

        self.debug = False

        self.setMinimumWidth(300)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.mainLayout)


        #=============================
        ## Set up tree
        self.tree = QtWidgets.QTreeWidget()
        self.mainLayout.addWidget(self.tree, 30)

        self.tree.setRootIsDecorated(False)
        self.tree.header().setStretchLastSection(True)
        self.tree.header().hide()

        hi = self.tree.headerItem()
        hi.setText(C_EG.file_name, "Example")


        self.tree.itemClicked.connect(self.on_tree_item_clicked)

        self.load_files_list()



    def load_files_list(self, sub_dir=None):

        files_list, err = ags4.examples_list()
        if err:
            pass #TODO
        self.tree.clear()
        if files_list == None:
            return
        for fd in files_list:
            file_name = fd["file_name"]
            item = QtWidgets.QTreeWidgetItem()
            item.setText(C_EG.file_name, file_name)
            item.setIcon(C_EG.file_name, Ico.icon(Ico.Ags4))
            f = item.font(C_EG.file_name)
            f.setBold(True)
            item.setFont(C_EG.file_name, f)
            self.tree.addTopLevelItem(item)



    def on_tree_item_clicked(self, item, col):

        file_name = str(item.text(C_EG.file_name))
        self.sigFileSelected.emit(file_name)


class ErrorsListSortFilterModel(QtCore.QSortFilterProxyModel):

    def __init__(self):
        QtCore.QSortFilterProxyModel.__init__(self)

        self.show_errors = True
        self.show_warnings = True


    def dfilterAcceptsRow(self, ridx, midx):
        pass





class HelpDialog(QtWidgets.QDialog):
    debug = False

    def __init__(self, parent=None, page=None):
        QtWidgets.QDialog.__init__(self, parent)

        self.setWindowTitle("Help")
        self.setWindowIcon(dIco.icon(dIco.Help))

        # self.setWindowFlags(QtCore.Qt.Popup)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.setMinimumWidth(900)
        self.setMinimumHeight(700)

        # self.setStyleSheet("border: 1px solid black;")

        outerLayout = QtWidgets.QVBoxLayout()
        outerLayout.setSpacing(0)
        margarine = 0
        outerLayout.setContentsMargins(margarine, margarine, margarine, margarine)
        self.setLayout(outerLayout)

        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.setSpacing(0)
        margarine = 0
        mainLayout.setContentsMargins(margarine, margarine, margarine, margarine)
        outerLayout.addLayout(mainLayout)

        self.helpWidget = HelpWidget.HelpWidget(page=page)
        mainLayout.addWidget(self.helpWidget)

    # if page:
    #	self.show_page(page)

    def show_page(self, page):
        self.helpWidget.load_page(page)
        self.exec_()



#import mistune
#from help import DOCS_PATH, DOCS_CONTENT

class C:
    node = 0
    page = 1


class HelpWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, page=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.debug = False

        outerLayout = QtWidgets.QVBoxLayout()
        outerLayout.setSpacing(0)
        margarine = 0
        outerLayout.setContentsMargins(margarine, margarine, margarine, margarine)
        self.setLayout(outerLayout)

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

    def load_content_tree(self):

        self.tree.clear()
        self.tree.setUpdatesEnabled(False)

        item = TreeWidgetItem()
        item.set(C.node, "Index", ico=dIco.HelpPage)

        item.setText(C.page, "index.md")
        self.tree.addTopLevelItem(item)

        rootNode = self.tree.invisibleRootItem()
        self.load_dir_node(rootNode, DOCS_CONTENT)

        self.tree.setUpdatesEnabled(True)

    def load_dir_node(self, pItem, pth):

        files = os.listdir(pth)

        for f in sorted(files):
            xpth = os.path.join(pth, f)[len(DOCS_CONTENT):]
            if f == "index.md" and pth == DOCS_CONTENT:
                continue
            if os.path.isdir(f):
                item = TreeWidgetItem(pItem)
                item.set(C.node, f, ico=dIco.Folder)
                item.setText(C.page, xpth)

                self.load_dir_node(item, os.path.join(pth, f))
                self.tree.setItemExpanded(item, True)

            elif f.endswith(".md"):
                item = TreeWidgetItem(pItem)
                item.set(C.node, self.title_from_filename(f), ico=dIco.HelpPage)
                item.setText(C.page, xpth)

    def dpage_path_fn(self, page):
        if page.endswith(".md"):
            "%s.md" % page
        read_fn = os.path.join(DOCS_CONTENT, page)
        # if self.debug:
        if not os.path.exists(read_fn):
            print("ERROR: FILE not exits", read_fn, self)
            return

    def title_from_filename(self, fn):
        fn = os.path.basename(fn)
        if fn.endswith(".md"):
            fn = fn[0:-3]
        return fn.replace("_", " ").title()

    def select_page(self, page):

        idx = None
        if self.tabWidget.count() == 0:
            return idx
        ## check page is aleady loaded, and select
        for i in range(0, self.tabWidget.count()):

            if self.tabWidget.widget(i).page == page:
                self.tabWidget.blockSignals(True)
                self.tabWidget.setCurrentIndex(i)
                self.tabWidget.blockSignals(False)
                idx = i

                break
        items = self.tree.findItems(page, Qt.MatchExactly | Qt.MatchRecursive, C.page)
        if len(items) > 0:
            self.tree.blockSignals(True)
            self.tree.setCurrentItem(items[0])
            self.tree.blockSignals(False)
        return idx

    def load_page(self, page):

        page = str(page)

        full_path = DOCS_CONTENT + page

        if os.path.isdir(full_path):
            return
        elif not page.endswith(".md"):
            full_path = full_path + ".md"

        idx = self.select_page(page)
        if idx != None:
            return

        if not os.path.exists(full_path):
            # print "ERROR: FILE not exits", full_path
            return

        container = G.ut.read_file(os.path.join(DOCS_PATH, "templates", "help_container.html"))

        txt = G.ut.read_file(full_path)
        html = mistune.markdown(txt, escape=False)

        out_html = container.replace("##++CONTENT++##", html)

        self.tabWidget.blockSignals(True)
        webView = HelpPageView()
        nidx = self.tabWidget.addTab(webView, self.title_from_filename(page))
        webView.set_data(page, out_html)
        self.tabWidget.setTabIcon(nidx, dIco.icon(dIco.HelpPage))

        webView.sigPageLinkClicked.connect(self.load_page)

        self.tabWidget.setCurrentIndex(nidx)
        self.select_tree_node(page)
        self.tabWidget.blockSignals(False)

    def on_tree_selection(self):
        item = self.tree.currentItem()
        if item == None:
            return
        self.load_page(item.s(C.page))

    def on_tab_close_requested(self, idx):
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
        items = self.tree.findItems(page, Qt.MatchExactly | Qt.MatchRecursive, C.page)
        if len(items) > 0:
            self.tree.setCurrentItem(items[0])
        else:
            # page not in menu
            pass
        self.tree.blockSignals(False)


class HelpPageView(QtWidgets.QWidget):
    sigPageLinkClicked = pyqtSignal(str)

    def __init__(self, parent=None, page=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.debug = False
        self.page = None

        lay = QtWidgets.QVBoxLayout()
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        self.setLayout(lay)

        self.webView = QtWebKit.QWebView()
        lay.addWidget(self.webView, 2)

        if self.debug:
            page = self.webView.page()
            page.settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
            # elf.webView.settings().globalSettings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)

            self.webInspector = QtWebKit.QWebInspector(self)
            self.webInspector.setPage(page)
            lay.addWidget(self.webInspector, 3)

        self.webView.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.webView.linkClicked.connect(self.on_link_clicked)

    def set_data(self, page, html):
        self.page = page
        base_url = QtCore.QUrl.fromLocalFile(DOCS_PATH + "/")
        # bu.setScheme("file")

        self.webView.setHtml(html, base_url)

    def on_link_clicked(self, url):
        page = str(url.path())[1:]

        self.sigPageLinkClicked.emit(page)




class ExpPortalWidget( QtWidgets.QWidget ):
    """The SourceViewWidget info which in row 0 """



    def __init__( self, parent=None):
        QtWidgets.QWidget.__init__( self, parent )

        self.debug = False
        self.setObjectName("OGTSourceViewWidget")

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.mainLayout)


        self.tabWidget = QtWidgets.QTabWidget()
        self.mainLayout.addWidget(self.tabWidget)

        self.excelBrowse = ogtgui_excel.ExpExcelBrowserWidget()
        self.tabWidget.addTab(self.excelBrowse, "Excel Browse")

        self.pasteText = ExpPasteWidget()
        self.tabWidget.addTab(self.pasteText, "Paste clipboard from Excel")


    def init_load(self):
        pass

TEST_TXT = """
SAMP_TOP	SAMP_REF	SAMP_TYPE
m		
2DP	X	PA
4.50		U
"""



class ExpPasteWidget( QtWidgets.QWidget ):
    """The SourceViewWidget info which in row 0 """



    def __init__( self, parent=None):
        QtWidgets.QWidget.__init__( self, parent )

        self.debug = False
        self.setObjectName("OGTSourceViewWidget")

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.mainLayout)


        #self.tabWidget = QtWidgets.QTabWidget()
        #self.mainLayout.addWidget(self.tabWidget)

        self.txtSrc = QtWidgets.QPlainTextEdit()
        self.mainLayout.addWidget(self.txtSrc)
        self.txtSrc.textChanged.connect(self.on_text_changed)

        self.table = QtWidgets.QTableWidget()
        self.mainLayout.addWidget(self.table)
        self.txtSrc.setPlainText(TEST_TXT)


    def init_load(self):
        pass

    def on_text_changed(self):
        s = str(self.txtSrc.toPlainText())
        lines = s.split("\n")

        ridx = 0
        for rridx, rline in enumerate(lines):
            line = rline.strip()
            if line == "":
                continue
            if self.table.rowCount() < ridx + 1:
                self.table.setRowCount(ridx + 1)
            cols = line.split("\t")
            if self.table.columnCount() < len(cols):
                self.table.setColumnCount(len(cols))
            for cidx, cell in enumerate(cols):


                item = QtWidgets.QTableWidgetItem()
                item.setText(cell)
                self.table.setItem(ridx, cidx, item)
            ridx += 1



class ExpPathBrowseWidget( QtWidgets.QWidget ):
    """The SourceViewWidget info which in row 0 """

    sigOpenFile = pyqtSignal(str)

    def __init__( self, parent=None):
        QtWidgets.QWidget.__init__( self, parent )

        self.debug = False
        self.setObjectName("ExcelBrowserWidget")

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.mainLayout)

        self.toolbar = QtWidgets.QToolBar()
        self.mainLayout.addWidget(self.toolbar, 0)

        tbg = xwidgets.ToolBarGroup(title="Selected Dir")
        self.toolbar.addWidget(tbg)

        buttSel = xwidgets.XToolButton(text="Select")
        self.toolbar.addWidget(buttSel)

        self.txtPath = QtWidgets.QLineEdit()
        tbg.addWidget(self.txtPath)
        if G.args.dev:
            self.txtPath.setText("/home/ogt/gstl_examples/35579")

        self.tree = QtWidgets.QTreeView()
        self.mainLayout.addWidget(self.tree, 30)

        self.dirModel = QtWidgets.QFileSystemModel()
        self.dirModel.setRootPath(self.txtPath.text())
        self.dirModel.setNameFilters(["*.xlsx"])

        self.tree.setModel(self.dirModel)
        self.tree.setRootIndex( self.dirModel.index(self.txtPath.text()) )


        if G.args.dev:
            ed = os.path.join(str(self.txtPath.text()), "ATTS")
            self.tree.expand( self.dirModel.index(ed ) )

        self.tree.setColumnWidth(0, 400)

        self.tree.doubleClicked.connect(self.on_tree_double_clicked)



    def on_tree_double_clicked(self, midx):
        filename = str(self.dirModel.filePath(midx))
        self.sigOpenFile.emit(filename)




class HeaderBarWidget( QtWidgets.QWidget ):

    """Psuedo Stack as it containes a header/label and widget"""
    def __init__( self, parent=None, title=None,
                  bg=None, bg2=None, fg=None):
        QtWidgets.QWidget.__init__( self, parent )

        self.bg = bg
        self.bg2 = bg2
        self.fg = fg


        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)

        self.lblLead = QtWidgets.QLabel()
        self.lblLead.setText("")
        self.lblLead.setFixedWidth(20)
        self.mainLayout.addWidget(self.lblLead, 0)

        self.lblTitle = QtWidgets.QLabel()
        self.lblTitle.setText("")
        self.mainLayout.addWidget(self.lblTitle, 10)

        self.setTitle(title)
        self.update_style()


    def setTitle(self, t):
        self.lblTitle.setText(t)

    def update_style(self):

        bg = self.bg if self.bg else "#dddddd"
        bg2 = self.bg2 if self.bg2 else "#efefef"
        fg = self.fg if self.fg else "#666666"

        sty = " color: %s; font-size: 12pt; padding: 2px 5px;" % fg
        sty += "background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, "
        sty += "stop: 0  %s" % bg
        sty += ", stop: 0.7 %s " % bg2
        sty  += "stop: 1 %s" % bg2
        sty += ");"
        self.lblLead.setStyleSheet(sty)

        sty = " color: %s; font-size: 12pt; padding: 2px 5px;"  % fg
        sty += "background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, "
        sty += "stop: 0 %s" % bg2
        sty += ", stop: 0.1 %s " % bg2
        sty  += "stop: 1 %s" % bg
        sty += ");"
        self.lblTitle.setStyleSheet(sty)

    def setCurrentIndex(self, idx):
        self.headerStack.setCurrentIndex(idx)
        self.contentStack.setCurrentIndex(idx)

    def addWidget(self, widget):
        self.mainLayout.addWidget(widget)

