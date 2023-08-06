# -*- coding: utf-8 -*-



import collections
from Qt import Qt, QtCore, QtGui, QtWidgets, pyqtSignal

import ogtgui_widgets
import xwidgets
from img import Ico

HOVER_COLOR = "#EBEBEB"

class OGTSamplesTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None, ogtDoc=None):
        QtCore.QAbstractTableModel.__init__(self)

        self.ogtDoc = ogtDoc
        self.loca_id = None

        self.cidx = None
        self.ridx = None

    def set_current(self, ridx=None, cidx=None):
        self.ridx = ridx
        self.cidx = cidx

    def row_index_from_samp_id(self, samp_id):
        grp = self.ogtDoc.group_from_code("SAMP")
        # cidx = grp.index_of_heading("SAMP_ID")
        for ridx, row in enumerate(grp.data):
            cell = row.get("SAMP_ID")
            #print cell.value, samp_id, cell.value == samp_id
            if cell.value == samp_id:
                return ridx
        return None

    def get_index_from_cell(self, scell):
        grp = self.ogtDoc.group_from_code("SAMP")
        for ridx in range(0, grp.data_rows_count):
            for cidx in range(0, grp.headings_count):
                cell = grp.data_cell(ridx, cidx)
                if cell == scell:
                    return self.index(ridx, cidx)
        return None

    def columnCount(self, pidx=None):
        grp = self.ogtDoc.group_from_code("SAMP")
        if grp:
            return grp.headings_count
        return 0

    def rowCount(self, pidx=None):
        grp = self.ogtDoc.group_from_code("SAMP")
        if grp:
            return grp.data_rows_count
        return 0

    def data_row(self, row):
        return self.ogtDoc.group_from_code("SAMP").data[row]

    def data(self, midx, role=Qt.DisplayRole):
        """Returns the data at the given index"""
        row = midx.row()
        col = midx.column()

        if role == Qt.DisplayRole:
            cell = self.ogtDoc.group_from_code("SAMP").data_cell(row, col)
            # print cell
            return cell.value

        if role == Qt.BackgroundRole:
            bg = "white"
            if midx.row() == self.ridx:
                bg = HOVER_COLOR
            return QtGui.QColor(bg)


        return None

    def headerData(self, idx, orient, role=None):
        if role == Qt.DisplayRole and orient == Qt.Horizontal:
            return self.ogtDoc.group_from_code("SAMP").heading_from_index(idx).head_code

        if role == Qt.DisplayRole and orient == Qt.Vertical:
            return idx + 1

        if role == Qt.TextAlignmentRole and orient == Qt.Horizontal:
            return Qt.AlignRight if idx == 0 else Qt.AlignLeft

        return None



class OGTScheduleTestsModel(QtCore.QAbstractTableModel):

    def __init__(self, parent=None, ogtDoc=None):
        QtCore.QAbstractTableModel.__init__(self)

        self.xheads = None

        self.ridx = None
        self.cidx = None

    def set_current(self, ridx=None, cidx=None):
        self.ridx = ridx
        self.cidx = cidx

    def rowCount(self, pidx=None):
        if self.xheads == None:
            return 0
        return 1

    def columnCount(self, pidx=None):
        if self.xheads == None:
            return 0
        return len(self.xheads)

    def to_no(self, v ):
        try:
            return float(v)
        except:
            return None

    def data(self, midx, role=Qt.DisplayRole):

        if role == Qt.DisplayRole:
            # only one row
            return self.xheads[midx.column()]

        if role == Qt.TextAlignmentRole:
            return Qt.AlignTop|Qt.AlignCenter

        if role == Qt.BackgroundRole:
            bg = "white"
            if midx.column() == self.cidx:
                bg = HOVER_COLOR
            return QtGui.QColor(bg)


    def headerData(self, idx, orient, role=None):
        if role == Qt.DisplayRole and orient == Qt.Vertical:
            return " "

class OGTScheduleTableModel(QtCore.QAbstractTableModel):

    def __init__(self, parent=None, ogtDoc=None):
        QtCore.QAbstractTableModel.__init__(self)

        self.xcells = None
        self.xheads = None
        self.row_counts = None
        self.col_counts = None

        self.hi_row = None
        self.hi_col = None

    def set_current(self, ridx, cidx):
        self.curr = [ridx, cidx]
        self.layoutChanged.emit()

    def rowCount(self, pidx=None):
        if self.xheads == None:
            return 0
        return len(self.xcells)

    def columnCount(self, pidx=None):
        if self.xheads == None:
            return 0
        return len(self.xheads)

    def to_no(self, v ):
        try:
            return float(v)
        except:
            return None


    def data(self, midx, role=Qt.DisplayRole):

        if False and role == Qt.DisplayRole or role == Qt.EditRole:
            cell = self.xcells[midx.row()][midx.column()]
            if cell:
                return "YES"

        if False and role == Qt.CheckStateRole:
            cell = self.xcells[midx.row()][midx.column()]
            if cell:
                return Qt.Checked
            return Qt.Unchecked

        if  False and role == Qt.BackgroundRole:
            #cell = self.xcells[midx.row()][midx.column()]
            #if cell:
            #    return QtWidgets.QColor("orange")

            if self.hi_row != None:
                if self.hi_row == midx.row():
                    return QtGui.QColor("#eeeeee")

    def headerData(self, idx, orient, role=None):
        if role == Qt.DisplayRole and orient == Qt.Horizontal:
            v = self.col_counts.get(idx)
            if v != None:
                return v
            return ""

        if role == Qt.DisplayRole and orient == Qt.Vertical:
            v = self.row_counts.get(idx)
            if v != None:
                return v
            return ""

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        return None

class OGTScheduleWidget( QtWidgets.QWidget ):
    """The SourceViewWidget info which in row 0 """

    TOP_HEIGHT = 100

    def __init__( self, parent=None, ogtDoc=None):
        QtWidgets.QWidget.__init__( self, parent )

        self.ogtDoc = ogtDoc

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.mainLayout)

        self.headerBar = ogtgui_widgets.HeaderBarWidget(title="Schedule", bg="#B3C256")
        self.mainLayout.addWidget(self.headerBar, 0)

        self.buttRefreshSched = QtWidgets.QToolButton()
        self.buttRefreshSched.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.buttRefreshSched.setText("Reload")
        self.buttRefreshSched.setIcon(Ico.icon(Ico.Refresh))
        self.headerBar.addWidget(self.buttRefreshSched)
        self.buttRefreshSched.clicked.connect(self.on_butt_refresh)

        self.splitter = QtWidgets.QSplitter()
        self.mainLayout.addWidget(self.splitter, 200)
        self.splitter.setOrientation(Qt.Horizontal)

        ### left -------------------------

        self.leftWidget = QtWidgets.QWidget()
        self.splitter.addWidget(self.leftWidget )
        self.leftLay = xwidgets.vlayout()
        self.leftWidget.setLayout(self.leftLay)

        self.lblCorner = QtWidgets.QLabel()
        self.lblCorner.setText("---")
        self.lblCorner.setFixedHeight(self.TOP_HEIGHT)
        self.leftLay.addWidget(self.lblCorner)

        ## == Samples
        self.tableSamples = XTableHoverView()
        self.leftLay.addWidget(self.tableSamples, 100)

        self.modelSamples = OGTSamplesTableModel(ogtDoc=self.ogtDoc)
        self.tableSamples.setModel(self.modelSamples)

        self.tableSamples.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableSamples.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableSamples.selectionModel().selectionChanged.connect(self.on_tree_samples_selection)

        #self.tableSamples.verticalScrollBar().hide()
        self.tableSamples.verticalScrollBar().valueChanged.connect(self.on_table_samples_v_scroll)
        self.tableSamples.sigHover.connect(self.on_table_samples_hover)

        ## === Right ---------------------

        self.rightWidget = QtWidgets.QWidget()
        self.splitter.addWidget(self.rightWidget)
        self.rightLay = xwidgets.vlayout()
        self.rightWidget.setLayout(self.rightLay)

        ## Tests
        self.tableTests = XTableHoverView()
        self.rightLay.addWidget(self.tableTests)


        self.modelTests = OGTScheduleTestsModel(ogtDoc=self.ogtDoc)
        self.tableTests.setModel(self.modelTests)

        self.tableTests.horizontalHeader().hide()
        self.tableTests.setFixedHeight(self.TOP_HEIGHT)
        self.tableTests.sigHover.connect(self.on_table_tests_hover)


        ## Schedule
        self.tableSched = QtWidgets.QTableView()
        self.rightLay.addWidget(self.tableSched, 100)

        self.modelSchedule = OGTScheduleTableModel(ogtDoc=self.ogtDoc)
        self.tableSched.setModel(self.modelSchedule)

        self.tableSched.setMouseTracking(True)
        #self.tableSched.verticalScrollBar().hide()
        self.tableSched.verticalScrollBar().valueChanged.connect(self.on_table_sched_v_scroll)

        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 2)

    def on_butt_refresh(self):
        pass


    def on_table_samples_v_scroll(self, x):
        self.tableSched.verticalScrollBar().setValue(x)

    def on_table_sched_v_scroll(self, x):
        self.tableSamples.verticalScrollBar().setValue(x)


    def on_table_samples_hover(self, ridx, cidx):
        self.on_cell_enter(ridx, None)

    def on_table_tests_hover(self, ridx, cidx):
        self.on_cell_enter(None, cidx)

    def on_tree_samples_selection(self):
        # print "on_tree_samples_selection", "do_update"
        #self.ogtDoc.validate()
        #self.do_update()
        self.modelSchedule.hi_row = None
        idxx = self.tableSamples.selectionModel().selectedIndexes()
        if len(idxx):
            self.modelSchedule.hi_row = idxx[0].row()

        self.modelSchedule.layoutChanged.emit()



    def do_update(self):

        self.modelSamples.layoutChanged.emit()

        for c in range(0, self.modelSamples.rowCount()):
            self.tableSamples.resizeColumnToContents(c)

        sched_group = self.ogtDoc.group_from_code("LBST")
        if sched_group == None:
            return

        # first walks and get unique `tests` defined in LBST_TEST
        testsDic = {}
        for ridx, row in enumerate(sched_group.data):
            tstCell = row.get('LBST_TEST')
            if tstCell:
                tst = tstCell.value
                if not tst in testsDic:
                    testsDic[tst] = dict(test=tst, recs=[])
                testsDic[tst]["recs"].append(row)

        ## set test headings = kinda description
        self.modelTests.xheads = sorted(testsDic.keys())
        self.modelSchedule.xheads = self.modelTests.xheads

        ## create blank dict with ridx/cidx.. of None's
        self.modelSchedule.xcells = {}
        for ridx in range(0, self.modelSamples.rowCount()):
            if not ridx in self.modelSchedule.xcells:
                self.modelSchedule.xcells[ridx] = {}
                for cidx in range(0, len(self.modelSchedule.xheads)):
                    self.modelSchedule.xcells[ridx][cidx] = None




        for cidx, tst in enumerate(self.modelSchedule.xheads):
            recs = testsDic[tst]["recs"]

            for rec in recs:
                sam_id_cell = rec.get("SAMP_ID")

                ridx = self.modelSamples.row_index_from_samp_id(sam_id_cell.value)
                if ridx != None:
                    self.modelSchedule.xcells[ridx][cidx] = "YES"

        for ridx in range(0, self.modelSchedule.rowCount()):
            for cidx in range(0, self.modelSchedule.columnCount()):

                # Cell widget
                idx = self.modelSchedule.index(ridx, cidx)
                widget = self.tableSched.indexWidget(idx)
                if widget == None:
                    widget = XSchedCellWidget(ridx=ridx, cidx=cidx)
                    self.tableSched.setIndexWidget(idx, widget)
                    widget.sigEnter.connect(self.on_cell_enter)
                    widget.sigChanged.connect(self.on_check_changed)

                v = self.modelSchedule.xcells[ridx][cidx]
                if v:
                    widget.set_enabled(True)


        self.update_totals()

        self.modelTests.layoutChanged.emit()
        self.modelSchedule.layoutChanged.emit()
        self.modelSamples.layoutChanged.emit()

        self.tableTests.setRowHeight(0, self.TOP_HEIGHT)
        self.tableTests.verticalHeader().setFixedWidth(30)
        self.tableSched.verticalHeader().setFixedWidth(30)

        HEI = 24
        for ridx in range(0, self.modelSamples.rowCount()):
            self.tableSamples.setRowHeight(ridx, HEI)
            self.tableSched.setRowHeight(ridx, HEI )

    def on_check_changed(self):
        self.update_totals()
        self.modelSchedule.layoutChanged.emit()

    def update_totals(self):
        ## update totals

        self.modelSchedule.row_counts = {}
        self.modelSchedule.col_counts = {}

        for ridx in range(0, self.modelSchedule.rowCount()):
            for cidx in range(0, self.modelSchedule.columnCount()):

                # Cell widget
                widget = self.tableSched.indexWidget( self.modelSchedule.index(ridx, cidx) )
                if widget.isChecked():

                    if not ridx in self.modelSchedule.row_counts:
                        self.modelSchedule.row_counts[ridx] = 0
                    self.modelSchedule.row_counts[ridx] += 1

                    if not cidx in self.modelSchedule.col_counts:
                        self.modelSchedule.col_counts[cidx] = 0
                    self.modelSchedule.col_counts[cidx] += 1
        self.modelSchedule.layoutChanged.emit()


    def on_cell_enter(self, xridx, xcidx):
        #self.modelSchedule.set_current(ridx, cidx)

        for ridx in range(0, self.modelSchedule.rowCount()):
            for cidx in range(0, self.modelSchedule.columnCount()):
                # Cell widget
                widget = self.tableSched.indexWidget(self.modelSchedule.index(ridx, cidx))
                widget.set_hover(xridx, xcidx)

        self.modelSamples.set_current(ridx=xridx)
        self.modelSamples.layoutChanged.emit()

        self.modelTests.set_current(cidx=xcidx)
        self.modelTests.layoutChanged.emit()

class XSchedCellWidget(QtWidgets.QWidget):

    sigLeave = pyqtSignal(int, int)
    sigEnter = pyqtSignal(int, int)
    sigChanged = pyqtSignal()

    def __init__(self, parent=None, ridx=None, cidx=None):
        QtWidgets.QWidget.__init__(self)

        self.ridx = ridx
        self.cidx = cidx

        self.mainLayout = xwidgets.hlayout()
        self.setLayout(self.mainLayout)


        self.buttEna = QtWidgets.QToolButton()
        self.buttEna.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.buttEna.setCheckable(True)
        self.buttEna.setAutoRaise(True)
        self.buttEna.setFixedWidth(20)
        self.buttEna.setIcon(Ico.icon(Ico.TickOff))
        self.mainLayout.addWidget(self.buttEna, 0)
        self.buttEna.toggled.connect(self.on_enabled_toggled)
        self.buttEna.clicked.connect(self.on_butt_clicked)

        self.lblDetails = xwidgets.XLabel()
        self.mainLayout.addWidget(self.lblDetails, 2)

    def set_enabled(self, state):
        self.buttEna.setChecked(state)

    def isChecked(self):
        return self.buttEna.isChecked()

    def on_enabled_toggled(self, state=None):
        self.up_widgets()

    def on_butt_clicked(self):
        self.sigChanged.emit()

    def up_widgets(self):
        state = self.buttEna.isChecked()
        ico = Ico.TickOn if state else Ico.TickOff
        self.buttEna.setIcon(Ico.icon(ico))

        s = "background-color: #FFFA8A;" if state else ""
        self.buttEna.setStyleSheet(s)
        self.lblDetails.setStyleSheet(s)

    def enterEvent(self, ev):
        self.sigEnter.emit(self.ridx, self.cidx)

    def leaveEvent(self, ev):
        self.sigLeave.emit(self.ridx, self.cidx)

    def set_hover(self, ridx, cidx):
        #print "set_hover", ridx, self.ridx, cidx, self.cidx
        if self.buttEna.isChecked():
            return
        color = "white"

        if ridx == self.ridx or cidx == self.cidx:
            color = HOVER_COLOR

        self.lblDetails.setStyleSheet("background-color: %s" % color)
        self.buttEna.setStyleSheet("background-color: %s" % color)


class XTableHoverView(QtWidgets.QTableView):

    sigHover = pyqtSignal(int, int)

    def __init__(self, parent=None):
        QtWidgets.QTableView.__init__(self)

        self.setMouseTracking(True)

    def mouseMoveEvent(self, ev):

        idx = self.indexAt(ev.pos())
        self.sigHover.emit(idx.row(), idx.column())

