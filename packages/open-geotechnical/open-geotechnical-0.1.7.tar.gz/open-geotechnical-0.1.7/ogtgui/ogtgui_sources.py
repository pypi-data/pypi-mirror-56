# -*- coding: utf-8 -*-

from Qt import Qt, QtCore, QtWidgets, QtGui, pyqtSignal

from ogt import ogt_cell

import app_globals as G
import ogtgui_widgets
import xwidgets

class SourceGridModel(QtCore.QAbstractTableModel):

    sigChanged = pyqtSignal()

    def __init__(self, parent=None, ogtDoc=None):
        QtCore.QAbstractTableModel.__init__(self, parent)

        self.ogtDoc = ogtDoc

        self.xcells = None
        self.max_cols = None

    def rowCount(self, parent=None, *args):
        """Returns the number of rows of the model"""
        if self.xcells == None:
            return 0
        return len(self.xcells)

    def columnCount(self, parent=None, *args):
        """Returns the number of columns of the model"""
        if self.max_cols != None:
            return self.max_cols
        return 0

    def DEADflags(self, midx):

        #print(midx)
        cell = self.xcells[midx.row()].get(midx.column())
        #head = self.ogtGroup.heading_from_index(idx.column())
        #dt = head.data_type
        if cell and isinstance(cell, ogt_cell.OGTCell) and cell.parentHeading:
            if cell.parentHeading.data_type == "PA":
            #if dt == "PA":  # or dt == "ID"
                flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled

            else:
                flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
            # if index.column() != 0:
            #    flags |= Qt.ItemIsEditable
            return flags
        flags =  Qt.ItemIsEnabled
        return flags

    # def setData(self, index, value, role=None):
    #     """Updates DATA when modified in the view"""
    #     if role == Qt.EditRole:
    #         cell = self.ogtGroup.data_cell(index.row(), index.column())
    #         cell.value = value.strip()
    #         self.ogtGroup.emit()
    #         #success = self.ogtGroup.set_data_cell_value(index.row(), index.column(), value)
    #         #self.layoutChanged.emit()
    #         #self.modelReset.emit()
    #         #self.sigChanged.emit()
    #         return True
    #         #self.dataChanged.emit(index, index)
    #         #return True
    #     return False

    def data(self, index, role=Qt.DisplayRole):
        """Returns the data at the given index"""

        row = index.row()
        col = index.column()

        cell_val = self.xcells[row].get(col)

        if role == Qt.DisplayRole:
            if isinstance(cell_val, ogt_cell.OGTCell):
                return cell_val.value
            return cell_val if cell_val else ""

        if role == Qt.BackgroundColorRole:
            if cell_val:
                if isinstance(cell_val, ogt_cell.OGTCell):
                    # all the data is cells
                    return QtGui.QColor(cell_val.background())
                # the descriptions are string
                if cell_val == "DATA":
                    return QtGui.QColor("#DCF1FA")
                elif cell_val == "GROUP":
                    return QtGui.QColor("#78DAFF")
                else:
                    return QtGui.QColor("#ABDBFE")
            return QtGui.QColor("#dddddd")

        return None

    def headerData(self, idx, orientation, role=Qt.DisplayRole):

        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return str(idx + 1)

        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(idx + 1)

        return None

    def do_update(self):

        self.xcells, self.max_cols = self.ogtDoc.to_grid()
        self.modelReset.emit()


class SourceGridTableWidget( QtWidgets.QWidget ):

    #sigGoto = pyqtSignal(str)
    sigSelect = pyqtSignal(object)

    def __init__( self, parent=None, ogtDoc=None):
        QtWidgets.QWidget.__init__( self, parent )


        self.ogtDoc = ogtDoc

        self.mainLayout = xwidgets.vlayout()
        self.setLayout(self.mainLayout)


        ## Sources Table --------------
        self.tableGrid = QtWidgets.QTableView()
        self.mainLayout.addWidget(self.tableGrid, 0)


        self.modelGrid = SourceGridModel(ogtDoc=self.ogtDoc)
        self.tableGrid.setModel(self.modelGrid)

        f = self.tableGrid.font()
        f.setFamily("monospace")
        self.tableGrid.setFont(f)
        verticalHeader = self.tableGrid.verticalHeader()
        #TODO verticalHeader.setResizeMode(QtWidgets.QHeaderView.Fixed)
        verticalHeader.setDefaultSectionSize(20)


    def do_update(self):
        self.modelGrid.do_update()



class OGTSourceViewWidget( QtWidgets.QWidget ):
    """The SourceViewWidget info which in row 0 """

    def __init__( self, parent=None, ogtDoc=None):
        QtWidgets.QWidget.__init__( self, parent )


        self.ogtDoc = ogtDoc
        self.setObjectName("OGTSourceViewWidget")

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.mainLayout)

        self.headerWidget = ogtgui_widgets.HeaderBarWidget(title="Source Output", bg="#B2C3C3")
        self.mainLayout.addWidget(self.headerWidget, 0)

        self.mainLayout.addStretch(5)

        self.tabWidget = QtWidgets.QTabWidget()
        self.mainLayout.addWidget(self.tabWidget, 200)

        # Source View
        self.sourceView = xwidgets.XPlainTextEdit()
        self.tabWidget.addTab(self.sourceView, "Raw Text")

        # Grid view
        self.tableGrid = SourceGridTableWidget(ogtDoc=self.ogtDoc)
        self.tabWidget.addTab(self.tableGrid, "Grid View")


        self.tabWidget.setCurrentIndex(1)


    def do_update(self):


        txt, err = self.ogtDoc.to_ags4()
        self.sourceView.setPlainText(txt)

        self.tableGrid.do_update()


    def on_splitter_moved(self, i, pos):
        G.settings.save_splitter(self.splitter)

    def load_document(self, doco):

        self.sourceView.setText(doco.source)

        show_warn, show_err = self.errorsWidget.get_error_filters()
        self.tableWidget.setRowCount(len(doco.csv_rows))

        for ridx, row in enumerate(doco.csv_rows):

            # each csv_row is not the same, so extend here
            if self.tableWidget.columnCount() < len(row):
                self.tableWidget.setColumnCount(len(row))


            #errs = doco.error_cells.get(ridx)

            bg = None
            for cidx, cell in enumerate(row):

                #if cidx == 0:
                #    bg = bg_color(cell)
                item = xwidgets.XTableWidgetItem()
                item.setText( cell )
                item.set_bg("#EAFFE0")
                self.tableWidget.setItem(ridx, cidx, item)


                errs = doco.get_errors(lidx=ridx, cidx=cidx)
                if errs != None:

                    for er in errs:

                        if er.type:
                            item.setData(FILTER_ROLE.err, "1")
                        else:
                            item.setData(FILTER_ROLE.warn, "1")
                        """    
                        if er.cidx == cidx:
                            item.set_bg(er.bg)
                        """
                    self.set_item_bg(item, show_warn, show_err)
                ## color the row
                #item.setBackgroundColor(QtWidgets.QColor(bg))
            self.tableWidget.setRowHeight(ridx, 20)


        self.errorsWidget.load_document(doco)

    def set_item_bg(self, item, show_warn, show_err):
        has_warn = item.data(FILTER_ROLE.warn).toBool()
        has_err = item.data(FILTER_ROLE.err).toBool()
        item.set_bg("white")
        if show_warn and has_warn:
            item.set_bg(ERR_COLORS.warn_bg)
        if show_err and has_err:
            item.set_bg(ERR_COLORS.err_bg)


    def update_colours(self, show_warn, show_err):
        self.tableWidget.setUpdatesEnabled(False)
        for ridx in range(0, self.tableWidget.rowCount()):
            for cidx in range(0, self.tableWidget.columnCount()):
                item = self.tableWidget.item(ridx, cidx)
                if item:
                    self.set_item_bg(item, show_warn, show_err)
        self.tableWidget.setUpdatesEnabled(True)

    def select_cell(self, lidx, cidx):
        self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(self.tableWidget))
        self.tableWidget.setCurrentCell(lidx, cidx)
        item = self.tableWidget.currentItem()
        self.tableWidget.scrollToItem(item, QtWidgets.QAbstractItemView.PositionAtCenter)


    def on_select_changed(self):
        item = self.tableWidget.currentItem()
        if item == None:
            self.errorsWidget.select_items(None, None)
            return

        self.errorsWidget.select_items(item.row(), item.column())


    def on_row_clicked(self, ridx):
        pass

