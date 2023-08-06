# -*- coding: utf-8 -*-


from Qt import QtGui, QtWidgets, QtCore, Qt, pyqtSignal

from ogt import ags4, CELL_COLORS

import app_globals as G
from img import Ico
import ags4_widgets
import xwidgets
#import ogtgui_widgets
import ogtgui_dialogs
import ogtgui_errors

from ogt.ogt_validate import OGTError

class HeadersListModel(QtCore.QAbstractTableModel):

    class C:
        #node = 0
        valid = 0
        head_code = 1
        unit = 2
        type = 3
        head_description = 4


    def __init__(self):
        QtCore.QAbstractTableModel.__init__(self)

        self.ogtGroup = None
        self._col_labels = ["Valid", "Heading", "Unit", "Type", "Descripton"]

    def set_group(self, ogtGroup):
        self.ogtGroup = ogtGroup

    def columnCount(self, foo):
        return len(self._col_labels)

    def rowCount(self, midx):

        if self.ogtGroup == None:
            return 0
        return self.ogtGroup.headings_count

    def data(self, midx, role=Qt.DisplayRole):
        """Returns the data at the given index"""
        row = midx.row()
        col = midx.column()

        if role == Qt.DisplayRole or role == Qt.EditRole:
            hd = self.ogtGroup.heading_by_index(row)

            if col == self.C.head_code:
                return hd.head_code

            if col == self.C.unit:
                return hd.unit_label

            if col == self.C.type:
                return hd.type_label

            if col == self.C.head_description:
                return hd.head_description

            if col == self.C.valid:
                return "TODO"

            return "?"

        if role == Qt.DecorationRole:
            if col == self.C.head_code:
                return Ico.icon(Ico.AgsHeading)

        if role == Qt.FontRole:
            if col == self.C.head_code:
                f = QtWidgets.QFont()
                f.setBold(True)
                return f

        if role == Qt.TextAlignmentRole:
            if col == 0:
                return Qt.AlignRight
            if col in [self.C.valid, self.C.unit, self.C.type]:
                return Qt.AlignCenter
            return Qt.AlignLeft

        if False and role == Qt.BackgroundColorRole:
            cell = self.ogtDoc.group_by_index(row)[col]
            #bg = cell.get_bg()
            if len(self.ogtGroup.data_cell(row, col).errors) > 0:
                pass
            return QtWidgets.QColor(bg)


        return QtCore.QVariant()


    def headerData(self, idx, orient, role=None):
        if role == Qt.DisplayRole and orient == Qt.Horizontal:
            return QtCore.QVariant(self._col_labels[idx])

        if role == Qt.TextAlignmentRole and orient == Qt.Horizontal:
            if  idx == 0:
                return Qt.AlignRight
            if idx in [self.C.valid, self.C.unit, self.C.type]:
                return Qt.AlignCenter
            return Qt.AlignLeft

        return QtCore.QVariant()

class HeadersListWidget( QtWidgets.QWidget ):


    #sigGoto = pyqtSignal(str)

    def __init__( self, parent=None):
        QtWidgets.QWidget.__init__( self, parent )

        self.debug = False
        self.ogtGroup = None

        self.mainLayout = xwidgets.vlayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(xwidgets.XLabel("Foooo"))

        self.tree = QtWidgets.QTreeView()
        self.tree.setRootIsDecorated(False)
        self.mainLayout.addWidget(self.tree, 0)


        self.model = HeadersListModel()
        self.tree.setModel(self.model)

        self.tree.setColumnWidth(HeadersListModel.C.head_code, 110)
        self.tree.setColumnWidth(HeadersListModel.C.valid, 50)
        self.tree.setColumnWidth(HeadersListModel.C.unit, 50)
        self.tree.setColumnWidth(HeadersListModel.C.type, 50)


    def set_group(self, ogtGrp):
        self.model.set_group(ogtGrp)


class HeadCodeWidget( QtWidgets.QWidget ):
    """The info in tableWidget """

    #sigGoto = pyqtSignal(str)

    def __init__( self, parent=None, ogtDoc=None):
        QtWidgets.QWidget.__init__( self, parent )

        self.ogtDoc = ogtDoc
        self.ogtHeading = None

        self.debug = False
        self.setAutoFillBackground(True)

        self.mainLayout = xwidgets.vlayout()
        self.setLayout(self.mainLayout)


        ## So splits up tthe header into parts..
        #self.headerWidget = QtWidgets.QWidget()
        self.headerCodeLay = xwidgets.hlayout()
        #self.headerWidget.setLayout(self.headerGridLay)
        self.mainLayout.addLayout(self.headerCodeLay)

        self.lblHeadCode = xwidgets.XLabel("-", bold=True)
        self.headerCodeLay.addWidget(self.lblHeadCode, 10)

        #self.buttGroup = xwidgets.XToolButton(self, text="group")
        #self.headerGridLay.addWidget(self.buttGroup)

        self.buttHeadCode = xwidgets.XToolButton(self, ico=Ico.BulletDown,  bold=True, popup=True, menu=True)
        self.buttHeadCode.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.headerCodeLay.addWidget(self.buttHeadCode, 0)

        self.buttHeadCode.menu().addAction("Open Group TODO")
        self.buttHeadCode.menu().addAction("Select another heading TODO")

        #sp = self.buttHeadCode.sizePolicy()
        #sp.setHorizontalPolicy(QtWidgets.QSizePolicy.Expanding)
        #self.buttHeadCode.setSizePolicy(sp)
        """
        sty = "background-color: #dddddd; color: black; padding: 3px; font-size: 8pt;"

        # description
        self.lblHeadDescription = QtWidgets.QLabel()
        self.lblHeadDescription.setStyleSheet(sty)
        self.lblHeadDescription.setFixedHeight(60)
        self.lblHeadDescription.setWordWrap(True)
        self.lblHeadDescription.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        self.mainLayout.addWidget(self.lblHeadDescription)
        """

    def set_head_code(self, x):
        self.lblHeadCode.setText(x)


class TableHeaderWidget( QtWidgets.QWidget ):
    """The HEADER info in tableWidget """

    sigGoto = pyqtSignal(str)

    def __init__( self, parent=None, ogtDoc=None):
        QtWidgets.QWidget.__init__( self, parent )

        self.ogtDoc = ogtDoc
        self.ogtHeading = None

        self.debug = False


        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.mainLayout)

        row = 0
        ## So splits up tthe header into parts..
        #self.headerWidget = QtWidgets.QWidget()
        self.headerGridLay = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.headerGridLay, row, 0, 1, 3)

        self.lblHeadCode = xwidgets.XLabel("-", bold=True)
        self.headerGridLay.addWidget(self.lblHeadCode, 10)


        self.buttHeadCode = xwidgets.XToolButton(self, ico=Ico.BulletDown,  bold=True, popup=True, menu=True)
        self.buttHeadCode.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.headerGridLay.addWidget(self.buttHeadCode, 0)

        self.buttHeadCode.menu().addAction("Open Group TODO")
        self.buttHeadCode.menu().addAction("Select another heading TODO")


        sty = "background-color: #dddddd; color: black; padding: 3px; font-size: 8pt;"

        # description
        row += 1
        self.lblHeadDescription = QtWidgets.QLabel()
        self.lblHeadDescription.setStyleSheet(sty)
        self.lblHeadDescription.setFixedHeight(60)
        self.lblHeadDescription.setWordWrap(True)
        self.lblHeadDescription.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        self.mainLayout.addWidget(self.lblHeadDescription, row, 0, 1, 3)


        # unit
        row += 1
        lbl = xwidgets.XLabel("Unit:", align=Qt.AlignRight, style=sty)
        self.mainLayout.addWidget(lbl, row, 0)

        self.lblUnit = xwidgets.XLabel("-", bold=True, style=sty + "color: #000099;")
        self.mainLayout.addWidget(self.lblUnit, row, 1, 1, 2)

        # Type
        row += 1
        lbl = xwidgets.XLabel("Type:", align=Qt.AlignRight, style=sty )
        self.mainLayout.addWidget(lbl, row, 0)

        self.lblType = xwidgets.XLabel("-", bold=True, style=sty + "color: #000099;" )
        self.mainLayout.addWidget(self.lblType, row, 1)

        self.buttLink = QtWidgets.QToolButton()
        #self.buttLink.setAutoRaise(True)
        self.buttLink.setText("Goto")
        self.mainLayout.addWidget(self.buttLink, row, 2)
        self.buttLink.setVisible(False)
        self.buttLink.clicked.connect(self.on_goto)

        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.setColumnStretch(1, 5)

    def set_link(self, state):
        self.buttLink.setVisible(state)

    def set_heading(self, ogtHeading):

        self.ogtHeading = ogtHeading

        descr = self.ogtHeading.head_description
        t = "-" if descr == None else descr
        para = '<p style="line-height: 80%">' + t + '</p>'
        self.lblHeadDescription.setText(para)

        self.lblHeadCode.setText(ogtHeading.head_code)

        self.lblUnit.setText(self.ogtHeading.unit_label)
        #typ = "<a href="""
        self.lblType.setText(self.ogtHeading.type_label)
        #self.lblType.setToolTip(hrec['type'])

        typ = ags4.AGS4.type(self.ogtHeading.type)
        if typ:
            self.lblType.setToolTip(typ['description'])
        else:
            self.lblType.setToolTip(self.ogtHeading.type_label)

    def on_goto(self):
        self.sigGoto.emit(self.ogtHeading.head_code)




class HeadingsModel(QtCore.QAbstractTableModel):
    """Model for group headings"""
    sigChanged = pyqtSignal()

    class R:
        head_code = 0
        head_description = 1
        unit = 2
        data_type = 3
        _row_count = 4

    def __init__(self, parent=None, ogtGroup=None):
        QtCore.QAbstractTableModel.__init__(self, parent)

        self.ogtGroup = ogtGroup


    def columnCount(self, parent=None):
        return self.ogtGroup.headings_count

    def rowCount(self, parent=None):
        return self.R._row_count


    def data(self, index, role=Qt.DisplayRole):
        """Returns the data at the given index"""
        row = index.row()
        col = index.column()
        head = self.ogtGroup.heading_from_index(col)

        if role == Qt.DisplayRole:

            if row == self.R.head_code:
                return None # head.head_code #- now a widget

            if row == self.R.head_description:
                return head.head_description

            if row == self.R.unit:
                return head.unit_cell.value

            if row == self.R.data_type:
                return head.data_type_cell.value

            return "_NOCELL_"

        if role == Qt.BackgroundColorRole:
            #cell = self.ogtGroup.raw_cell(row, col)
            if row == self.R.head_code:
                return QtGui.QColor(head.head_cell.background())

            if row == self.R.unit:
                return QtGui.QColor(head.unit_cell.background())

            if row == self.R.data_type:
                return QtGui.QColor(head.data_type_cell.background())

            return QtGui.QColor("white")


        if role == Qt.TextAlignmentRole:
            if row == self.R.head_description:
                return Qt.AlignTop

        return None

    def headerData(self, idx, orientation, role=Qt.DisplayRole):
        """Returns the headers to display"""

        if role == Qt.DisplayRole and orientation == Qt.Horizontal:

            return "" #self.ogtGroup.heading_from_index(idx).head_code

        if role == Qt.DisplayRole and orientation == Qt.Vertical:

            if idx == self.R.head_code:
                return "Code"

            if idx == self.R.head_description:
                return "Desc"

            if idx == self.R.unit:
                return "Unit"

            if idx == self.R.data_type:
                return "Type"

            return " "

        if role == Qt.TextAlignmentRole and orientation == Qt.Vertical:
                return Qt.AlignRight

        return None

    def setData(self, index, value, role=None):
        """Updates DATA when modified in the view"""
        if role == Qt.EditRole:
            success = self.ogtGroup.set_data_cell_value(index.row(), index.column(), value)
            self.layoutChanged.emit()
            return success
            #self.dataChanged.emit(index, index)
            #return True
        return False

    def flags(self, index):
        """Returns the flags of the model"""
        flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled # | Qt.ItemIsEditable
        return flags


class DataModel(QtCore.QAbstractTableModel):
    """Model for group data
    """

    #sigChanged = pyqtSignal()

    def __init__(self, parent, ogtGroup):
        QtCore.QAbstractTableModel.__init__(self, parent)

        self.ogtGroup = ogtGroup

    def columnCount(self, parent=None):
        return self.ogtGroup.headings_count

    def rowCount(self, parent=None):
        return self.ogtGroup.data_rows_count


    def data(self, index, role=Qt.DisplayRole):
        """Returns the data at the given index"""
        row = index.row()
        col = index.column()

        if role == Qt.DisplayRole or role == Qt.EditRole:
            cell = self.ogtGroup.data_cell(row, col)
            if cell:
                return cell.value
            return None

        if role == Qt.BackgroundColorRole:
            cell = self.ogtGroup.data_cell(row, col)
            if cell:
                return QtGui.QColor(cell.background())
            return QtGui.QColor("#dddddd")

        if False and role == Qt.BackgroundColorRole:
            cell = self.ogtGroup.data_cell(row, col)
            bg = cell.get_bg()
            if len(self.ogtGroup.data_cell(row, col).errors) > 0:
                pass
            return QtGui.QColor(bg)



    def headerData(self, idx, orientation, role=Qt.DisplayRole):

        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.ogtGroup.heading_from_index(idx).head_code

        if role == Qt.DisplayRole and orientation == Qt.Vertical:
            return str(idx + 1)

        if role == Qt.TextAlignmentRole and orientation == Qt.Vertical:
                return Qt.AlignRight

        return None

    def setData(self, index, value, role=None):
        """Updates DATA when modified in the view"""
        if role == Qt.EditRole:
            cell = self.ogtGroup.data_cell(index.row(), index.column())
            cell.value = value.strip()
            self.ogtGroup.emit()
            #success = self.ogtGroup.set_data_cell_value(index.row(), index.column(), value)
            #self.layoutChanged.emit()
            #self.modelReset.emit()
            #self.sigChanged.emit()
            return True
            #self.dataChanged.emit(index, index)
            #return True
        return False

    def flags(self, idx):

        head = self.ogtGroup.heading_from_index(idx.column())
        dt = head.data_type
        if dt == "PA": # or dt == "ID"
            flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled
        else:
            flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        #if index.column() != 0:
        #    flags |= Qt.ItemIsEditable
        return flags

    def midx_from_val(self, cidx, v):
        for ridx in range(0, self.ogtGroup.data_rows_count):
            dcell = self.ogtGroup.data_cell(ridx, cidx)
            if dcell and dcell.value == v:
                return self.index(ridx, cidx)
        return None

    def val_from_midx(self, midx):
        return self.ogtGroup.data_cell( midx.row(), midx.column() )

    def midx_from_cell(self, srcCell):
        for ridx in range(0, self.ogtGroup.data_rows_count):
            cells = self.ogtGroup.data[ridx]
            for ki, cell in cells.items():
                if cell == srcCell:
                    return self.index(ridx, self.ogtGroup.index_of_heading(ki))
        return None



T_STYLE = """
QTableView
{
       
}
QTableView::item
{
  
}
QTableView::item:selected {
    border: 1px solid black;
}

"""
class XTableKeysHeadingView(QtWidgets.QTableView):
    """Catches the Down button in the headings view, fires sigDown to move to table below"""
    sigMoveDown = pyqtSignal(int)

    def __init__(self, parent=None):
        QtWidgets.QTableView.__init__(self, parent)


    def keyPressEvent(self,  ev):
        indexes = self.selectionModel().selectedIndexes()
        if len(indexes) == 1 and ev.key() == Qt.Key_Down and indexes[0].row() == 3:
            self.sigMoveDown.emit(indexes[0].column())
            return
        QtWidgets.QTableView.keyPressEvent(self, ev)


class XTableKeysDataView(QtWidgets.QTableView):
    """Catched the UP button in the data view, fires sigUp to move to table above"""
    sigMoveUp = pyqtSignal(int)

    def __init__(self, parent=None):
        QtWidgets.QTableView.__init__(self, parent)

    def keyPressEvent(self,  ev):
        indexes = self.selectionModel().selectedIndexes()
        if len(indexes) == 1 and ev.key() == Qt.Key_Up and indexes[0].row() == 0:
            self.sigMoveUp.emit(indexes[0].column())
            return
        QtWidgets.QTableView.keyPressEvent(self, ev)





class GroupTableWidget( QtWidgets.QWidget ):
    """The Group Table..... consists of two tables.. and two models
        - the headings model + tableHeaders
        - the data model + tableData
    """

    sigGoto = pyqtSignal(str)


    def __init__( self, parent=None, ogtGroup=None):
        QtWidgets.QWidget.__init__( self, parent )

        self.ogtGroup = ogtGroup


        self.mainLayout = xwidgets.vlayout()
        self.setLayout(self.mainLayout)

        #== Headings table and model ====
        self.modelHeadings = HeadingsModel(ogtGroup=ogtGroup)

        self.tableHeadings = XTableKeysHeadingView()
        self.mainLayout.addWidget(self.tableHeadings, 0)
        self.tableHeadings.setModel(self.modelHeadings)

        self.tableHeadings.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tableHeadings.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableHeadings.horizontalHeader().setFixedHeight(15)
        self.tableHeadings.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableHeadings.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.tableHeadings.doubleClicked.connect(self.on_table_headings_dbl_clicked)
        self.tableHeadings.selectionModel().selectionChanged.connect(self.on_table_headings_selection_changed)
        self.tableHeadings.sigMoveDown.connect(self.on_table_headings_move_down)
        self.tableHeadings.horizontalScrollBar().valueChanged.connect(self.on_table_headings_h_scroll)
        self.tableHeadings.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableHeadings.customContextMenuRequested.connect(self.on_table_headings_context)
        self.tableHeadings.horizontalHeader().sectionResized.connect(self.on_col_resize)

        #= Popup menu for tableheader
        self.popHead = QtWidgets.QMenu()
        wi = QtWidgets.QWidgetAction(self.popHead)
        self.popHeadLbl = QtWidgets.QLabel()
        self.popHeadLbl.setText("-")
        self.popHeadLbl.setStyleSheet("background-color: #666666; color: #eeeeee; padding: 4px;")
        wi.setDefaultWidget(self.popHeadLbl)
        self.popHead.addAction(wi)

        #self.popHead.addAction(Ico.icon(Ico.Add), "Add Heading...", self.on_add_heading)
        self.popHead.addSeparator()
        self.popHead.addAction(Ico.icon(Ico.Ags4), "Open AGS spec")



        #== Data
        self.modelData =  DataModel(self, ogtGroup)


        self.tableData = XTableKeysDataView()
        self.mainLayout.addWidget(self.tableData, 200)#
        self.tableData.setStyleSheet(T_STYLE)


        self.tableData.setModel(self.modelData)

        self.tableData.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tableData.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableData.horizontalHeader().hide()
        self.tableData.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.tableData.horizontalScrollBar().valueChanged.connect(self.on_table_data_h_scroll)

        self.tableData.verticalHeader().setFixedWidth(self.tableHeadings.verticalHeader().width())

        self.tableData.doubleClicked.connect(self.on_table_data_dbl_clicked)

        self.tableData.selectionModel().selectionChanged.connect(self.on_table_data_selection_changed)
        self.tableData.sigMoveUp.connect(self.on_table_data_move_up)



        self.set_heading_height()

    def do_update(self):
        self.modelHeadings.modelReset.emit()
        self.modelData.modelReset.emit()

        self.update_table_heading_widgets()

    def update_table_heading_widgets(self):

        for cidx in range(0, self.modelHeadings.columnCount()):
            # first row is HEAD_CODE
            hidx = self.modelHeadings.index(0, cidx)
            widget = self.tableHeadings.indexWidget(hidx)
            oHead = self.ogtGroup.heading_from_index(cidx)
            if widget == None:

                widget = HeaderCellWidget(ogtHead=oHead)
                self.tableHeadings.setIndexWidget(hidx, widget)
            #head_code = self.ogtGroup.headings_index[cidx]
            #widget.set_label(head_code)
            widget.parentheading = oHead
            widget.do_update()


    def set_heading_height(self):
        HEADER_HEIGHT = 134
        DESC_HEIGHT = 60
        self.tableHeadings.setRowHeight(1, DESC_HEIGHT)

        h = HEADER_HEIGHT + 35
        if self.tableHeadings.isRowHidden(1):
            h = h - DESC_HEIGHT
        self.tableHeadings.setFixedHeight(h)


    def on_col_resize(self, idx):
        self.tableData.setColumnWidth(idx, self.tableHeadings.columnWidth(idx))


    def on_table_headings_context(self, qPoint):

        clickIdx = self.tableHeadings.indexAt(qPoint)
        #headcodeIdx = self.modelHeadings.index(0, clickIdx.column())

        head_code = self.ogtGroup.heading_from_index(clickIdx.column()).head_code
        self.popHeadLbl.setText(head_code)

        self.popHead.exec_(self.tableHeadings.mapToGlobal(qPoint) )

    def on_table_headings_dbl_clicked(self, midx):

        row = midx.row()
        col = midx.column()
        R = HeadingsModel.R

        if row == R.unit:
            v = self.ogtGroup.heading_from_index(col)
            if v:
                dial = ogtgui_dialogs.UnitSelectDialog(self, v)
                dial.exec_()


        if row == R.data_type:
            ogtHead = self.ogtGroup.heading_from_index(col)
            if ogtHead:
                dial = ogtgui_dialogs.DataTypeSelectDialog(self, ogtHead)
                dial.exec_()



    def on_table_data_dbl_clicked(self, midx):
        row = midx.row()
        col = midx.column()

        headOb = self.ogtGroup.heading_from_index(col)

        if headOb.data_type == "PA":
            ## Its a picklist
            cell = self.ogtGroup.data_cell(row, col)
            dial = ogtgui_dialogs.AbbrPickDialog(self, ogtHead=headOb, editCell=cell)
            resp = dial.exec_()
            return


    def on_table_data_h_scroll(self, x):
        self.tableHeadings.horizontalScrollBar().setValue(x)

    def on_table_headings_h_scroll(self, x):
        self.tableData.horizontalScrollBar().setValue(x)


    def on_goto(self, code):
        self.sigGoto.emit(code)

    def set_show_description(self, state):
        self.tableHeadings.setRowHidden(1, not state)
        self.set_heading_height()

    def select_error(self, ogtErr):

        midx = self.modelData.midx_from_cell(ogtErr.cell)
        if midx:
            self.tableData.selectionModel().select(midx, QtCore.QItemSelectionModel.SelectCurrent)
            self.tableData.scrollTo(midx)


    def on_table_headings_selection_changed(self, sel, desel):
        if sel.count() == self.tableData.selectionModel().hasSelection():
            self.tableData.blockSignals(True)
            self.tableData.selectionModel().clearSelection()
            self.tableData.blockSignals(False)

    def on_table_data_selection_changed(self, sel, desel):
        if sel.count() == self.tableHeadings.selectionModel().hasSelection():
            self.tableHeadings.blockSignals(True)
            self.tableHeadings.selectionModel().clearSelection()
            self.tableHeadings.blockSignals(False)


    def on_table_data_move_up(self, cidx):
        self.tableData.blockSignals(True)
        self.tableData.selectionModel().clearSelection()
        self.tableData.blockSignals(False)
        midx = self.modelHeadings.index(3, cidx)
        self.tableHeadings.selectionModel().select(midx, QtCore.QItemSelectionModel.SelectCurrent)
        self.tableHeadings.setCurrentIndex(midx)
        self.tableHeadings.setFocus()

    def on_table_headings_move_down(self, cidx):
        self.tableHeadings.blockSignals(True)
        self.tableHeadings.selectionModel().clearSelection()
        self.tableHeadings.blockSignals(False)
        midx = self.modelData.index(0, cidx)
        self.tableData.selectionModel().select(midx, QtWidgets.QItemSelectionModel.SelectCurrent)
        self.tableData.setCurrentIndex(midx)
        self.tableData.setFocus()


class GroupViewWidget( QtWidgets.QWidget ):

    sigGoto = pyqtSignal(str)
    #sigChanged = pyqtSignal()

    def __init__( self, parent=None, ogtGroup=None):
        QtWidgets.QWidget.__init__( self, parent )

        self.ogtGroup = ogtGroup

        self.mainLayout = xwidgets.vlayout()
        self.setLayout(self.mainLayout)

        ##=== title and toolbar at top =========
        m = 3
        topLay = xwidgets.hlayout(margin=m, spacing=1)
        self.mainLayout.addLayout(topLay, 0)

        #== description
        sty = " color: #444444; padding: 2px; font-size: 14pt;"
        self.lblGroupDescription = QtWidgets.QLabel()
        self.lblGroupDescription.setText("-- empty --")
        self.lblGroupDescription.setStyleSheet(sty + "")
        topLay.addWidget(self.lblGroupDescription, 100)

        # == Actions
        self.tbgActions = xwidgets.ToolBarGroup(title="Actions", width=120)
        topLay.addWidget(self.tbgActions, 0)
        # The AGS group data
        self.buttAddHeading = xwidgets.XToolButton(text="Add Heading", ico=Ico.Add, callback=self.on_add_heading)
        self.tbgActions.addWidget(self.buttAddHeading)
       # self.buttAddHeading.clicked.connect(self.on_butt_ags_group_code)


        # == Group Info button
        self.tbgInfo = xwidgets.ToolBarGroup(title="Info", width=80)
        topLay.addWidget(self.tbgInfo, 0)
        # The AGS group data
        self.buttAgsGroupCode = xwidgets.XToolButton(text="-", ico=Ico.Ags4, tooltip="View AGS data Dict")
        self.tbgInfo.addWidget(self.buttAgsGroupCode)
        self.buttAgsGroupCode.clicked.connect(self.on_butt_ags_group_code)


        #== Parent + kids ----
        ## button group for convenience in disabling etc
        self.buttGroupReleations = QtWidgets.QButtonGroup()
        self.buttGroupReleations.setExclusive(False)

        #= Parent
        self.tbgParent = xwidgets.ToolBarGroup(title="Parent", width=80  )
        topLay.addWidget(self.tbgParent, 0)
        self.buttParent = xwidgets.XToolButton(text="", ico=Ico.BulletBlack)
        self.tbgParent.addWidget(self.buttParent)

        #= Children
        self.tbgChildren = xwidgets.ToolBarGroup(title="Children")
        topLay.addWidget(self.tbgChildren, 0)
        for i in range(0, 2):
            butt = xwidgets.XToolButton(text="", ico=Ico.BulletBlack)
            butt.setFixedWidth(60)
            self.tbgChildren.addWidget(butt)
            self.buttGroupReleations.addButton(butt, 0)

        self.buttGroupReleations.addButton(self.buttParent, 2) # adding parent at end for access
        self.buttGroupReleations.buttonClicked.connect(self.on_butt_parent_child)


        #== View Mode
        self.tbgView = xwidgets.ToolBarGroup(title="View", is_group=True, toggle_icons=True, toggle_callback=self.on_view_change )
        topLay.addWidget(self.tbgView)

        self.tbgView.addButton(text="Data", idx=0, checkable=True)
        self.tbgView.addButton(text="Source", idx=1, checkable=True, checked=True)





        # ============ mid splitter with stack widget
        self.splitter = QtWidgets.QSplitter()
        self.mainLayout.addWidget(self.splitter, 100)


        #== Left layout
        self.leftWidget = QtWidgets.QWidget()
        self.leftLay = xwidgets.vlayout()
        self.leftWidget.setLayout(self.leftLay)
        self.splitter.addWidget(self.leftWidget)

        self.groupDataTableWidget = GroupTableWidget(ogtGroup=self.ogtGroup)
        self.leftLay.addWidget(self.groupDataTableWidget)

        #self.sourceCellsTableWidget = SourceCellsTableWidget(self, self.ogtGroup)
        #self.leftLay.addWidget(self.sourceCellsTableWidget)
        #self.sourceCellsTableWidget.sigSelect.connect(self.on_source_table_select)

        #== Right layout
        self.rightWidget = QtWidgets.QWidget()
        self.rightLay = xwidgets.vlayout()
        self.rightWidget.setLayout(self.rightLay)
        self.splitter.addWidget(self.rightWidget)

        self.errorsWidget = ogtgui_errors.ErrorsWidget(self, ogtgui_errors.VIEW_ERR_MODE.group, ogtGroup=self.ogtGroup)
        self.rightLay.addWidget(self.errorsWidget, 1)
        self.errorsWidget.sigGotoError.connect(self.on_goto_error)


        self.headersListWidget = HeadersListWidget()
        self.headersListWidget.setMinimumWidth(300)
        self.rightLay.addWidget(self.headersListWidget, 1)



        self.splitter.setStretchFactor(0, 10)
        self.splitter.setStretchFactor(1, 4)
        # TODO restore
        #G.settings.restore_splitter(self.splitter)


        self.groupDataTableWidget.modelHeadings.sigChanged.connect(self.on_changed)
        #self.groupDataTableWidget.modelData.sigChanged.connect(self.on_changed)

        self.ogtGroup.parentDoc.sig_changed.connect(self.on_data_changed)
        #self.on_data_changed()

    def on_butt_parent_child(self, butt):
        group_code = str(butt.text())
        self.sigGoto.emit(group_code)

    def set_show_description(self, state):
        self.groupDataTableWidget.set_show_description(state)

    def on_source_table_select(self, cell):
        self.errorsWidget.select_from_cell(cell)

    def on_headings_data_changed(self):
        print( "on_headings_data_changed", self)

    def on_changed(self):
        self.sigChanged.emit()


    def do_update(self):
        """Updates all widgets and tables etc"""


        for model in [  #self.groupDataTableWidget.headingsModel,
                        #self.groupDataTableWidget.dataModel,
                        self.errorsWidget.model]:
            model.modelReset.emit()

        self.groupDataTableWidget.do_update()

        #==================================
        #= update toolbar labels and butts
        self.lblGroupDescription.setText(self.ogtGroup.group_description)
        self.buttAgsGroupCode.setText(self.ogtGroup.group_code)

        self.clear_relation_buttons()
        if self.ogtGroup.parent:
            self.set_relation_butt(self.buttParent, self.ogtGroup.parent)
        if self.ogtGroup.children:
            for idx, kid in enumerate(self.ogtGroup.children):
                butt = self.buttGroupReleations.button(idx)
                self.set_relation_butt(butt, kid)

    def clear_relation_buttons(self):
        for butt in self.buttGroupReleations.buttons():
            butt.setIcon(Ico.icon(Ico.BulletBlack))
            butt.setText("")
            butt.setDisabled(True)

    def set_relation_butt(self, butt, grp_code):
        butt.setIcon(Ico.icon(Ico.AgsGroup))
        butt.setText(grp_code)
        butt.setEnabled(True)

    def on_data_changed(self):

        #return
        #rub()
        for model in [
                    #self.groupSourceTableWidget.model,
                    self.groupDataTableWidget.headingsModel,
                    self.groupDataTableWidget.dataModel    ]:
            if model == self.sender():
                pass
            else:
                model.modelReset.emit()

        self.headersListWidget.model.layoutChanged.emit()
        self.errorsWidget.model.layoutChanged.emit()

        self.groupDataTableWidget.update_headings()


    def deadupdate_group(self, ogtGroup):

        self.ogtGroup = ogtGroup
        ## Set the labels
    def deadupdate_widgets(self):
        deaddd()
        self.buttGroupCode.setText( self.ogtGroup.group_code  )
        self.lblGroupDescription.setText( "-" if self.ogtGroup.group_description == None else self.ogtGroup.group_description )

        return
        # load into widgets

        self.groupDataTableWidget.set_group(ogtGroup)
        self.groupSourceTableWidget.set_group(ogtGroup)
        self.headersListWidget.set_group(ogtGroup)
        self.errorsWidget.set_group(ogtGroup)
        return


    def deadon_goto(self, code):
        self.sigGoto.emit(code)

    def on_goto_error(self, ogtErr):

        #self.sourceCellsTableWidget.select(ogtErr)
        self.groupDataTableWidget.select_error(ogtErr)

    def on_butt_ags_group_code(self):
        ags4_widgets.show_group_dialog(self, group_code=self.ogtGroup.group_code)


    def on_view_change(self, idx):
        return
        self.stackWidget.setCurrentIndex(idx)

    def on_add_heading(self):
        d = ogtgui_dialogs.HeadingsSelectDialog(self, self.ogtGroup)
        d.exec_()


class HeaderCellWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, ogtHead=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.ogtHead = ogtHead

        m = 1
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(m,m,m,m)
        self.setLayout(self.mainLayout)

        self.lblCode = xwidgets.XLabel()
        self.mainLayout.addWidget(self.lblCode, 10)


        ww = 10
        self.lblKey = xwidgets.XLabel(width=ww, align=Qt.AlignCenter, text="K", style="background-color: yellow;")
        self.mainLayout.addWidget(self.lblKey, 0)
        self.lblKey.setToolTip("Key Field")

        self.lblReq = xwidgets.XLabel(width=ww, align=Qt.AlignCenter, text="R", style="background-color: #F0DAED;")
        self.mainLayout.addWidget(self.lblReq, 0)
        self.lblReq.setToolTip("Required")


    def set_label(self, head_code):
        self.lblCode.setText(head_code)

        #self.do_update()

    def do_update(self):

        self.lblCode.setText(self.ogtHead.head_code)

        self.lblKey.setVisible(self.ogtHead.key == True)
        self.lblReq.setVisible(self.ogtHead.required == True)

