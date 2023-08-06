
import math

from Qt import Qt, QtCore, QtGui, QtWidgets, QtChart, pyqtSignal

from ogt import utils
import ogtgui_widgets
import xwidgets
from img import Ico

SEL_COLOR = "#F5FFA7"

class OGTSamplesModel(QtCore.QAbstractItemModel):


    def __init__(self, parent=None, ogtDoc=None):
        QtCore.QAbstractItemModel.__init__(self)

        self.ogtDoc = ogtDoc
        self.loca_id = None


    def index(self, row, col, parent=None):
        return self.createIndex(row, col)

    def parent(self, pidx=None):
        return QtCore.QModelIndex()

    def row_index_from_samp_id(self, samp_id):
        grp = self.ogtDoc.group_from_code("SAMP")
        #cidx = grp.index_of_heading("SAMP_ID")
        for ridx, row in enumerate(grp.data):
            cell = row.get("SAMP_ID")
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

        if role == Qt.DisplayRole or role == Qt.EditRole:
            cell = self.ogtDoc.group_from_code("SAMP").data_cell(row, col)
            return cell.value




        #if role == Qt.DecorationRole:
        #    if self.ogtDoc.group_from_code("SAMPE").heading_from_index(col).head_code == "SAMP_ID":
        #        return Ico.icon(Ico.Samples)

        #if role == Qt.FontRole:
        #    if col == self.C.group_code:
        #        f = QtWidgets.QFont()
        #        f.setBold(True)
        #        f.setFamily("monospace")
        #        return f

        #if role == Qt.TextAlignmentRole:
        #    return Qt.AlignRight if col == 0 else Qt.AlignLeft

        if role == Qt.BackgroundRole:
            bg = None
            if self.loca_id:
                xloca = self.ogtDoc.group_from_code("SAMP").data[row].get("LOCA_ID")
                if xloca and xloca.value == self.loca_id:
                    bg = SEL_COLOR

            return QtGui.QColor(bg) if bg != None else None


        return None


    def headerData(self, idx, orient, role=None):
        if role == Qt.DisplayRole and orient == Qt.Horizontal:
            #heads = self.ogtDoc.group_from_code("SAMP").heading_from_index(idx)
            return self.ogtDoc.group_from_code("SAMP").heading_from_index(idx).head_code

        if role == Qt.TextAlignmentRole and orient == Qt.Horizontal:
            return Qt.AlignRight if idx == 0 else Qt.AlignLeft




class OGTTestPointsModel(QtCore.QAbstractItemModel):


    def __init__(self, parent=None, ogtDoc=None):
        QtCore.QAbstractItemModel.__init__(self)

        self.ogtDoc = ogtDoc
        self.loca_id = None


    def index(self, row, col, parent=None):
        return self.createIndex(row, col)

    def parent(self, pidx=None):
        return QtCore.QModelIndex()


    def columnCount(self, foo):
        grp = self.ogtDoc.group_from_code("LOCA")
        if grp:
            return grp.headings_count
        return 0

    def index_from_locaid(self, loca_id):
        grp = self.ogtDoc.group_from_code("LOCA")
        if grp:
            for ridx in range(0, grp.data_rows_count):
                cell = grp.data[ridx].get("LOCA_ID")
                if cell.value == loca_id:
                    return self.index(ridx, grp.index_of_heading("LOCA_ID"))
    def rowCount(self, midx):
        grp = self.ogtDoc.group_from_code("LOCA")
        if grp:
            return grp.data_rows_count
        return 0

    def data(self, midx, role=Qt.DisplayRole):
        """Returns the data at the given index"""
        row = midx.row()
        col = midx.column()

        if role == Qt.DisplayRole:
            #grp = self.ogtDoc.group_from_code("LOCA")
            #hd = grp.heading_from_index(col)

            cell = self.ogtDoc.group_from_code("LOCA").data_cell(row, col)

            return cell.value

        if role == Qt.DecorationRole:
            if self.ogtDoc.group_from_code("LOCA").heading_from_index(col).head_code == "LOCA_ID":
                return Ico.icon(Ico.TestPoint)

        if False and  role == Qt.FontRole:
            if self.ogtDoc.group_from_code("LOCA").heading_from_index(col).head_code == "LOCA_ID":
                f = QtWidgets.QFont()
                f.setBold(True)
                f.setFamily("monospace")
                return f

        if  role == Qt.TextAlignmentRole:
            return Qt.AlignLeft

        if role == Qt.BackgroundColorRole:
            grp = self.ogtDoc.group_from_code("LOCA")
            if self.loca_id:
                cell = grp.data_cell(row, grp.index_of_heading("LOCA_ID"))
                if self.loca_id == cell.value:
                    return QtGui.QColor(SEL_COLOR)


            return None


        return QtCore.QVariant()


    def headerData(self, idx, orient, role=None):
        if role == Qt.DisplayRole and orient == Qt.Horizontal:
            #heads = self.ogtDoc.group_from_code("SAMP").heading_from_index(idx)
            grp = self.ogtDoc.group_from_code("SAMP")
            if grp == None:
                return ""
            return grp.heading_from_index(idx).head_code


        return None



class OGTSamplesWidget( QtWidgets.QWidget ):


    #sigGoto = pyqtSignal(str)

    def __init__( self, parent=None, ogtDoc=None):
        QtWidgets.QWidget.__init__( self, parent )

        self.debug = False
        self.ogtDoc = ogtDoc

        self.containerLayout = xwidgets.vlayout()
        self.setLayout(self.containerLayout)

        self.headerWidget = ogtgui_widgets.HeaderBarWidget(title="Samples", bg="#F7E194")
        self.containerLayout.addWidget(self.headerWidget, 0)

        self.mainLayout = xwidgets.hlayout()
        self.containerLayout.addLayout(self.mainLayout, 100)

        self.splitter = QtWidgets.QSplitter()
        self.mainLayout.addWidget(self.splitter)

        ## ========= Test Points
        self.treeLocations = QtWidgets.QTreeView()
        self.splitter.addWidget(self.treeLocations)

        self.modelTestPoints = OGTTestPointsModel(ogtDoc=self.ogtDoc)
        self.treeLocations.setModel(self.modelTestPoints)

        self.treeLocations.setRootIsDecorated(False)
        self.treeLocations.setExpandsOnDoubleClick(False)
        self.treeLocations.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.treeLocations.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)


        self.treeLocations.selectionModel().selectionChanged.connect(self.on_tree_locs_selection)

        ## ========= Samples
        self.treeSamples = QtWidgets.QTreeView()
        self.splitter.addWidget(self.treeSamples)

        self.modelSamples = OGTSamplesModel(ogtDoc=self.ogtDoc)
        self.treeSamples.setModel(self.modelSamples)

        self.treeSamples.setRootIsDecorated(False)
        self.treeSamples.setExpandsOnDoubleClick(False)
        self.treeSamples.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.treeSamples.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        self.treeSamples.selectionModel().selectionChanged.connect(self.on_tree_samples_selection_changed)


        chartContainerWidget = QtWidgets.QWidget()
        self.splitter.addWidget(chartContainerWidget)
        chartLayout = xwidgets.vlayout()
        chartContainerWidget.setLayout(chartLayout)

        lbl = xwidgets.XLabel(text="Chart below is a placeholder and needs stacked bar or alike",
                              style="background-color: #FFFCBF; padding: 5px")
        chartLayout.addWidget(lbl)

        self.chart = QtChart.QChartView()
        chartLayout.addWidget(self.chart)

        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 0)
        self.splitter.setStretchFactor(3, 6)


    def on_tree_samples_selection_changed(self, sel, dsel):

        self.treeLocations.blockSignals(True)
        self.treeLocations.clearSelection()
        self.treeLocations.blockSignals(False)

        indexes = self.treeSamples.selectionModel().selectedIndexes()
        loca_id = None



        self.modelTestPoints.loca_id = loca_id
        self.modelTestPoints.layoutChanged.emit()

        self.modelSamples.loca_id = loca_id
        self.modelSamples.layoutChanged.emit()



    def on_tree_locs_selection(self, sel, dsel):

        loca_id = None
        indexes = self.treeLocations.selectionModel().selectedIndexes()
        if len(indexes):
            loca_id = self.modelTestPoints.data(indexes[0], Qt.DisplayRole)



        self.modelSamples.loca_id = loca_id
        self.modelSamples.layoutChanged.emit()

        self.treeSamples.blockSignals(True)
        self.treeSamples.clearSelection()
        self.treeSamples.blockSignals(False)


    def do_update(self):
        self.modelTestPoints.layoutChanged.emit()
        self.modelSamples.layoutChanged.emit()

        self.series = {}
        max_d = 0
        locas = {}
        sampGrp = self.ogtDoc.group_from_code("SAMP")
        if sampGrp == None:
            return
        for rec in sampGrp.data:
            locaCell = rec.get("LOCA_ID")
            if locaCell:
                loca_id = locaCell.value
                if not loca_id in locas:
                    locas[loca_id] = []
                    self.series[loca_id] = []
                locas[loca_id].append(rec)


                dd = None
                st = rec.get("SAMP_TOP")
                if st:
                    dd = utils.to_float(st.value)
                    self.series[loca_id].append(dd)
                # rec['__DEPTH__'] = dd      # @@@DEPTH
                if dd != None and dd > max_d:
                    max_d = dd

        self.locas = sorted(locas.keys())

        self.chart.chart().removeAllSeries()


        axisX = QtChart.QBarCategoryAxis()
        axisX.append(self.locas)
        self.chart.chart().addAxis(axisX, Qt.AlignTop)

        axisY = QtChart.QValueAxis()
        self.chart.chart().addAxis(axisY, Qt.AlignLeft)


        for loca in self.locas:

            series = QtChart.QStackedBarSeries()
            series.setName(loca)

            barSet = QtChart.QBarSet(loca)
            for dpt in self.series[loca]:

                if dpt is not None:
                    barSet.append(dpt)

            series.append(barSet)

            self.chart.chart().addSeries(series)
            series.attachAxis(axisX)
            series.attachAxis(axisY)

        self.chart.setMinimumWidth(600)
        # self.chart.chart().createDefaultAxes()


