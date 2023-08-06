# -*- coding: utf-8 -*-

import os
from Qt import QtGui, QtCore, QtWidgets, Qt, pyqtSignal


from ogt import FORMATS
from ogt import ogt_doc
from ogt import ogt_cell

import app_globals as G

from img import Ico
import xwidgets

import ogtgui_doc
import ogtgui_groups
import ogtgui_widgets
import ogtgui_errors
import ogtgui_schedules
import ogtgui_samples
import ogtgui_sources
import ogtgui_dialogs
import ogtgui_excel

class OGTProjectWidget( QtWidgets.QWidget ):

    sigChanged = pyqtSignal()

    def __init__( self, parent=None):
        QtWidgets.QWidget.__init__( self, parent )

        self.ogtDoc = ogt_doc.OGTDocument()
        self.ogtDoc.sigChanged = self.sigChanged

        self.mainLayout = xwidgets.vlayout()
        self.setLayout(self.mainLayout)

        ##====== Top Bar ===
        lbl = QtWidgets.QLabel()
        lbl.setStyleSheet("background-color: #aaaaaa")
        lbl.setFixedHeight(1)
        self.mainLayout.addWidget(lbl)

        self.topLay = xwidgets.hlayout()
        self.mainLayout.addLayout(self.topLay)

        ## Header Label
        self.headerWidget = ogtgui_widgets.HeaderBarWidget(title="-", bg="#444444", bg2="#999999", fg="#eeeeee")
        self.topLay.addWidget(self.headerWidget, 100)

        lbl = QtWidgets.QLabel()
        lbl.setStyleSheet("background-color: #aaaaaa")
        lbl.setFixedHeight(1)
        self.mainLayout.addWidget(lbl)


        ## Add button
        self.buttActAdd = xwidgets.XToolButton(text="Add..", ico=Ico.Add, popup=True)
        self.topLay.addWidget(self.buttActAdd)
        self.buttActAdd.setMenu(QtWidgets.QMenu())

        #act = QtWidgets.QAction(Ico.icon(Ico.Groups), "Add required groups (PROJ, UNIT, etc)", self.on_add_default_groups)
        self.buttActAdd.menu().addAction(Ico.icon(Ico.Groups), "Add required groups (PROJ, UNIT, etc)", self.on_add_required_groups)

        ## Import button
        self.buttImport = xwidgets.XToolButton(text="Import", ico=Ico.Import, menu=True, popup=True)
        self.topLay.addWidget(self.buttImport)
        self.buttImport.menu()
        self.buttImport.menu().addAction(Ico(Ico.Excel), "Import excel", self.on_import_excel)

        ## Validate button
        self.buttValidate = xwidgets.XToolButton(text="Re-Validate", ico=Ico.Refresh, callback=self.on_validate)
        self.topLay.addWidget(self.buttValidate)

        ## Export button
        self.buttExport = xwidgets.XToolButton(text="Save & Export", ico=Ico.Export, callback=self.on_save_export)
        self.topLay.addWidget(self.buttExport)
        #for a in FORMATS:
        #    self.buttExport.menu().addAction("%s - TODO" % a)

        ## Reload button
        #self.buttReload = xwidgets.XToolButton(text="Reload", ico=Ico.Refresh, callback=self.on_reload)
        #self.topLay.addWidget(self.buttReload)



        self.mainLayout.addSpacing(5)

        ##========= Content ===============

        ## tabar + Stack
        tbarLay = xwidgets.hlayout(margin=0)
        self.mainLayout.addLayout(tbarLay)

        self.tabBar = QtWidgets.QTabBar()
        f = self.tabBar.font()
        f.setBold(True)
        self.tabBar.setFont(f)
        tbarLay.addWidget(self.tabBar)
        tbarLay.addStretch(5)

        self.stackWidget = QtWidgets.QStackedWidget()
        self.mainLayout.addWidget(self.stackWidget)

        ## Summary Tab
        self.tabBar.addTab(Ico.icon(Ico.Summary), "Summary")
        self.ogtProjSummaryWidget = OGTProjectSummaryWidget(ogtDoc=self.ogtDoc)
        self.stackWidget.addWidget(self.ogtProjSummaryWidget)
        self.ogtProjSummaryWidget.sigGoto.connect(self.on_goto)
        #self.ogtProjSummaryWidget.sigGotoSource.connect(self.on_goto_source)

        ## Groups Tab
        self.tabBar.addTab(Ico.icon(Ico.Groups), "Groups")
        self.ogtDocWidget = ogtgui_doc.OGTDocumentWidget(ogtDoc=self.ogtDoc)
        self.stackWidget.addWidget(self.ogtDocWidget)

        #self.ogtDoc.sigChanged.connect(self.on_changed)
        #self.ogtDocWidget.sigChanged.connect(self.on_changed)


        ## Samples Tab
        self.tabBar.addTab(Ico.icon(Ico.Samples), "Samples")
        self.ogtSamplesWidget = ogtgui_samples.OGTSamplesWidget(ogtDoc=self.ogtDoc)
        self.stackWidget.addWidget(self.ogtSamplesWidget)


        ## Schedule Tab
        self.tabBar.addTab(Ico.icon(Ico.Schedule), "Schedule")
        self.ogtScheduleWidget = ogtgui_schedules.OGTScheduleWidget(ogtDoc=self.ogtDoc)
        xidx = self.stackWidget.addWidget(self.ogtScheduleWidget)



        ## Source tab
        self.tabBar.addTab(Ico.icon(Ico.Source), "Source")
        self.ogtSourceViewWidget = ogtgui_sources.OGTSourceViewWidget(ogtDoc=self.ogtDoc)
        self.stackWidget.addWidget(self.ogtSourceViewWidget)

        """
        if False:
            self.tabBar.addTab(Ico.icon(Ico.Map), "Map")
            self.mapOverviewWidget = map_widgets.MapOverviewWidget()
            self.stackWidget.addWidget(self.mapOverviewWidget)
        """

        self.tabBar.currentChanged.connect(self.on_tab_changed)

        self.sigChanged.connect(self.on_changed)

        if G.args.dev:
            self.tabBar.setCurrentIndex(1)
            pass

    def init_load(self):
        pass

    def on_tab_changed(self, idx):
        self.stackWidget.setCurrentIndex(idx)
        self.stackWidget.widget(self.stackWidget.currentIndex()).do_update()


    def on_changed(self):
        #print("on_changed", self)
        #print(self.sender())
        self.on_validate()

    def on_butt_refresh_sched(self):
        self.ogtDoc.validate()
        self.ogtScheduleWidget.do_update()


    def on_validate(self):
        self.ogtDoc.validate()
        for widget in [self.ogtDocWidget]:
            widget.do_update()


    def add_ags4_file(self, file_path):

        #self.file_path = None
        """
        self.doc, err = ogt_doc.OGTDocument()
        err = self.doc.load_from_ags4_file(file_path)

        """
        #err = ogt_doc.create_doc_from_ags4_file(file_path)

        err = self.ogtDoc.add_ags4_file(file_path)

        # TODO
        self.ogtDoc.validate()
        self.do_update()

    def on_add_stuff(self):

        dial = ogtgui_dialogs.FileSelectDialog(self)
        dial.exec_()


    def on_add_test_ags(self):
        fn = "/home/geo2lab/z_drive/jobs/40101-40200/40153/AGS/40153 AGS.ags"
        self.do_update()

    def do_update(self):
        #proj = None #self.ogtDoc.proj_dict()
        proj = self.ogtDoc.proj_dict()

        if proj:
            self.headerWidget.setTitle(proj.get('PROJ_NAME', "PROJ_NAME is missing"))


        self.ogtDocWidget.do_update()
        self.ogtProjSummaryWidget.do_update()
        self.ogtSamplesWidget.do_update()
        self.ogtScheduleWidget.do_update()
        self.ogtSourceViewWidget.do_update()


        ## HACK
        #QtCore.QTimer.singleShot(4000, self.do_map_after)

    def do_map_after(self):
        self.mapOverviewWidget.load_document(self.ogtDoc)

    def on_goto(self, code):

        self.ogtDocWidget.select_group(code)
        idx = self.stackWidget.indexOf(self.ogtDocWidget)
        self.tabBar.setCurrentIndex(idx)



    def on_goto_source(self, lidx, cidx):

        self.ogtSourceViewWidget.select_cell(lidx, cidx)
        idx = self.stackWidget.indexOf(self.ogtSourceViewWidget)
        self.tabBar.setCurrentIndex(idx)


    def on_add_required_groups(self):

        self.ogtDoc.add_required_groups()


    def on_import_excel(self):
        #file_path = os.getcwd()
        file_path = "/home/ogt"

        dial = ogtgui_dialogs.FileSelectDialog(self, root=file_path)
        if dial.exec_():
            file_path = dial.file_path

            w = ogtgui_excel.ExcelBrowserDialog(self, file_path=file_path)
            w.exec_()

    def on_save_export(self):

        dial = ogtgui_dialogs.SaveExportDialog(self, self.ogtDoc)
        dial.exec_()

class CP:
    node = 0
    group_code = 1
    group_description = 2



class OGTProjectsModel(QtCore.QAbstractItemModel):

    class C:
        node = 0
        group_code = 1
        group_description = 2

    def __init__( self, parent=None):
        QtCore.QAbstractItemModel.__init__( self, parent )

        self.ogtDoc = None

    def load_document(self, ogtDoc):
        self.ogtDoc = ogtDoc
        self.modelReset.emit()

    def columnCount(self, pidx):
        return 3

    def headerData(self, p_int, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            lst = ["Rows", "Group", "Description"]
            return QtCore.QVariant(lst[p_int])
        return QtCore.QVariant()

    def rowCount(self, pidx):
        if self.ogtDoc == None:
            return 0
        if pidx.row() == -1:
            return self.ogtDoc.groups_count()
        return 0 #self.ogtDoc.groups_count()

    def index(self, row, col, pidx):
        return self.createIndex(row, col, None)
        #return QtCore.QModelIndex()

    def parent(self, index):

        if not index.isValid():
            return QtCore.QModelIndex()
        node = index.internalPointer()
        if node != None and node.parent() is None:
            ss
            return QtCore.QModelIndex()
        else:
            return self.createIndex(0, 0, None)
            return self.createIndex(node.parent.row, 0, node.parent)


        if False: #child.isValid():

            ip =  child.internalPointer()

            if ip:
                return self.createIndex(ip.parent().row(), 0, ip.parent())
            #return QtCore.QModelIndex()
        #return self.createIndex(child.row(), child.column(), None)
        return QtCore.QModelIndex()

    def data(self, midx, role):

        if role == Qt.DecorationRole:
            return QtCore.QVariant()

        if role == Qt.TextAlignmentRole:
            return QtCore.QVariant(int(Qt.AlignTop | Qt.AlignLeft))

        if role != Qt.DisplayRole:
            return QtCore.QVariant()

        #node = self.nodeFromIndex(midx)

        if midx.column() == 0:
            return QtCore.QVariant(self.ogtDoc.group_by_index(midx.row()))

        elif midx.column() == 1:
            return QtCore.QVariant(self.ogtDoc.group_by_index(midx.row()))

        elif midx.column() == 2:
            return QtCore.QVariant(self.ogtDoc.group_by_index(midx.row()))

        return QtCore.QVariant()




class OGTProjectSummaryWidget( QtWidgets.QWidget ):

    sigGoto = pyqtSignal(object)
    #sigGotoSource = pyqtSignal(int, int)

    def __init__( self, parent=None, ogtDoc=None):
        QtWidgets.QWidget.__init__( self, parent )

        self.ogtDoc = ogtDoc

        self.mainLayout = xwidgets.vlayout()
        self.setLayout(self.mainLayout)

        self.headerWidget = ogtgui_widgets.HeaderBarWidget(title="Project Summary", bg="#56B8F9")
        self.mainLayout.addWidget(self.headerWidget, 0)

        self.splitter = QtWidgets.QSplitter()
        self.mainLayout.addWidget(self.splitter, 100)


        self.treeSummary = QtWidgets.QTreeWidget()
        hi = self.treeSummary.headerItem()
        hi.setText(0, "Summary")
        self.splitter.addWidget(self.treeSummary)



        self.errorsWidget = ogtgui_errors.ErrorsWidget(mode=ogtgui_errors.VIEW_ERR_MODE.document, ogtDoc=self.ogtDoc)
        self.splitter.addWidget(self.errorsWidget)
        #self.errorsWidget.sigGotoSource.connect(self.on_goto_source)
        self.errorsWidget.sigGotoError.connect(self.on_goto_error)

        self.groupsListWidget = ogtgui_groups.GroupsListWidget(ogtDoc=self.ogtDoc)
        self.splitter.addWidget(self.groupsListWidget)

    def clear(self):

        self.errorsWidget.clear()
        self.tree.clear()

    def do_update(self):

        self.errorsWidget.do_update()
        self.groupsListWidget.do_update()

        self.treeSummary.clear()
        item = xwidgets.XTreeWidgetItem()
        item.setText(0, "TODO")
        self.treeSummary.addTopLevelItem(item)



    def on_tree_double_clicked(self, item, cidx):

        item = self.tree.currentItem()
        if item == None:
            return
        self.sigGoto.emit(item.text(CP.group_code))

    def DEADon_goto_source(self, lidx, cidx):
        self.sigGotoSource.emit(lidx, cidx)

    def on_goto_error(self, ogtErr):
        return
        self.sigGotoError.emit(ogtErr)

#
# class XStackedWidget( QtWidgets.QWidget ):
#
#     """Psuedo Stack as it containes a header/label and widget"""
#     def __init__( self, parent=None):
#         QtWidgets.QWidget.__init__( self, parent )
#
#         self.mainLayout = QtWidgets.QVBoxLayout()
#         self.mainLayout.setContentsMargins(0,0,0,0)
#         self.mainLayout.setSpacing(4)
#         self.setLayout(self.mainLayout)
#
#         self.headerStack = QtWidgets.QStackedWidget()
#         self.mainLayout.addWidget(self.headerStack, 0)
#
#         self.contentStack = QtWidgets.QStackedWidget()
#         self.mainLayout.addWidget(self.contentStack, 100)
#
#     def addWidget(self, widget, header_text, bg="#dddddd"):
#
#         tbar = QtWidgets.QWidget()
#         tlay = QtWidgets.QHBoxLayout()
#         tlay.setContentsMargins(0,0,0,0)
#         tlay.setSpacing(0)
#         tbar.setLayout(tlay)
#
#         lbl = QtWidgets.QLabel()
#         lbl.setText(header_text)
#         sty = " color: #666666; font-size: 14pt; padding: 2px 5px;"
#         sty += "background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, "
#         sty += "stop: 0 #efefef "
#         sty += ", stop: 0.3 #efefef "
#         sty += "stop: 1 %s" % bg
#         sty += ");"
#         lbl.setStyleSheet(sty)
#         tlay.addWidget(lbl, 10)
#
#         self.headerStack.addWidget(tbar)
#
#         nidx = self.contentStack.addWidget(widget)
#
#         return nidx
#
#     def setCurrentIndex(self, idx):
#         self.headerStack.setCurrentIndex(idx)
#         self.contentStack.setCurrentIndex(idx)
#
#     def addHeaderWidget(self, idx, widget):
#
#         wid = self.headerStack.widget(idx)
#         wid.layout().addWidget(widget, 0)
class OGTProjectOverviewWidget( QtWidgets.QWidget ):

    sigGoto = pyqtSignal(object)
    #sigGotoSource = pyqtSignal(int, int)

    def __init__( self, parent=None, ogtDoc=None):
        QtWidgets.QWidget.__init__( self, parent )

        self.ogtDoc = ogtDoc

        self.mainLayout = xwidgets.vlayout()
        self.setLayout(self.mainLayout)

        self.treeWidget = QtWidgets.QTreeWidget()

        self.mainLayout.addWidget(self.treeWidget)
