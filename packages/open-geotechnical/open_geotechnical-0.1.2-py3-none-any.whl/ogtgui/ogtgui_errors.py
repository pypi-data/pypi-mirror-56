# -*- coding: utf-8 -*-



from Qt import QtGui, QtWidgets, QtCore, Qt, pyqtSignal

import xwidgets
from ogt.ogt_validate import OGTError

class ErrorsListModel(QtCore.QAbstractTableModel):

    class C:
        lidx = 0
        cidx = 1
        rule = 2
        err_type = 3
        description = 4
        group_code = 5
        head_code = 6

    COL_LABELS = ["Line", "Col", "Rule", " ", "Description", "Group", "Heading"]

    def __init__(self, mode, ogtDoc=None, ogtGroup=None):
        QtCore.QAbstractTableModel.__init__(self)


        self.mode = mode
        self.ogtDoc = ogtDoc
        self.ogtGroup = ogtGroup

        self.hi_cell = None

    def columnCount(self, midx=None):
        return len(self.COL_LABELS)

    def rowCount(self, midx):

        if self.mode == VIEW_ERR_MODE.document:
            return self.ogtDoc.errors_warnings_count

        if self.mode == VIEW_ERR_MODE.group:
            return self.ogtGroup.errors_warnings_count

    def get_error(self, midx):
        errors = self._get_errors()
        return errors[ midx.row() ]

    def _get_errors(self):
        if self.mode == VIEW_ERR_MODE.document:
            return self.ogtDoc.errors_list()

        elif self.mode == VIEW_ERR_MODE.group:
            return self.ogtGroup.errors_list()

    def data(self, midx, role=Qt.DisplayRole):

        ridx = midx.row()
        cidx = midx.column()

        #errors = self._get_errors()
        #err = errors[ridx]
        err = self._get_errors()[ridx]

        if role == Qt.DisplayRole:

            if cidx == self.C.err_type:
                return "E" if err.err_type == OGTError.ERR else "W"

            if cidx == self.C.description:
                #print "m-=", err.message
                return err.message if err.message else "MISS"

            if cidx == self.C.rule:
                return err.rule if err.rule else "-"

            if cidx == self.C.lidx:
                return err.cell.lidx + 1

            if cidx == self.C.cidx:
                return err.cell.cidx + 1

            if cidx == self.C.group_code:
                return err.group_code

            if cidx == self.C.head_code:
                return err.head_code
            #if col == self.C.data_count:
            #    return grp.data_rows_count()
            return "?%s/%s?" % (ridx, cidx)

        if False and role == Qt.DecorationRole:
            if cidx == self.C.group_code:
                return Ico.icon(Ico.Group)

        if False and role == Qt.FontRole:
            if cidx == self.C.group_code:
                f = QtWidgets.QFont()
                f.setBold(True)
                return f

        if role == Qt.TextAlignmentRole:
            if cidx in [self.C.description,self.C.group_code, self.C.head_code]:
                return Qt.AlignLeft
            return Qt.AlignCenter

        if role == Qt.BackgroundColorRole:

            ## highlight line and col if highlight
            if self.hi_cell and cidx in [self.C.lidx, self.C.cidx]:
                if self.hi_cell.lidx == err.cell.lidx and self.hi_cell.cidx == err.cell.cidx:
                    return QtWidgets.QColor("#EBE267")

            if cidx == self.C.err_type:
                return QtGui.QColor(err.bg)
            #return QtWidgets.QColor()


        return None # QtCore.QVariant()


    def headerData(self, idx, orient, role=None):
        if role == Qt.DisplayRole and orient == Qt.Horizontal:
            return QtCore.QVariant(self.COL_LABELS[idx])

        if role == Qt.TextAlignmentRole and orient == Qt.Horizontal:
            if idx in [self.C.description, self.C.group_code, self.C.head_code]:
                return Qt.AlignLeft
            return Qt.AlignCenter

        return QtCore.QVariant()

    def set_highlight(self, cell):

        self.hi_cell = cell
        self.reset()



class VIEW_ERR_MODE:
    document = "document"
    group = "group"
    #heading = "heading"

class ErrorsWidget( QtWidgets.QWidget ):

    sigGotoError = pyqtSignal(object)
    #sigGotoSource = pyqtSignal(int, int)
    sigErrorsFilter = pyqtSignal(bool, bool)




    def __init__( self, parent=None, mode=None, ogtGroup=None, ogtDoc=None):
        QtWidgets.QWidget.__init__( self, parent )

        self.debug = False
        self.mode = mode
        if self.mode == None:
            freak_out()

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.mainLayout)

        lbl = QtWidgets.QLabel()
        lbl.setText("Errors and Warnings")
        lbl.setStyleSheet("font-weight: bold; padding: 3px; background-color: #eeeeee;")
        self.mainLayout.addWidget(lbl)

        self.toolBar = QtWidgets.QToolBar()
        self.mainLayout.addWidget(self.toolBar)




        self.buttGroupFilters = QtWidgets.QButtonGroup(self)
        self.buttGroupFilters.setExclusive(False)

        self.buttWarnings = xwidgets.XToolButton(text="Show Warnings", checkable=True, checked=True)
        self.buttGroupFilters.addButton(self.buttWarnings)

        self.buttErrors = xwidgets.XToolButton(text="Show Errors", checkable=True, checked=True)
        self.buttGroupFilters.addButton(self.buttErrors)

        self.buttGroupFilters.buttonClicked.connect(self.on_update_filter)

        self.toolBar.addWidget(self.buttWarnings)
        self.toolBar.addWidget(self.buttErrors)

        #=============================
        ## Set up tree
        self.tree = QtWidgets.QTreeView()
        self.mainLayout.addWidget(self.tree, 30)

        self.model = ErrorsListModel(mode=self.mode, ogtGroup=ogtGroup, ogtDoc=ogtDoc)

        #self.proxy = ErrorsListSortFilterModel()
        #self.proxy.setSourceModel(self.model)
        self.tree.setModel(self.model)



        self.tree.setRootIsDecorated(False)
        self.tree.setExpandsOnDoubleClick(False)
        self.tree.header().setStretchLastSection(True)
        #self.tree.setSortingEnabled(True)


        #self.tree.setColumnHidden(C_ERR.err, True)
        C = ErrorsListModel.C
        #self.tree.setColumnHidden(C.search, True)
        self.tree.setColumnWidth(C.err_type, 30)
        self.tree.setColumnWidth(C.lidx, 40)
        self.tree.setColumnWidth(C.cidx, 40)
        self.tree.setColumnWidth(C.rule, 50)
        #self.tree.setColumnWidth(C.highlight, 8)

        #self.tree.itemClicked.connect(self.on_tree_item_clicked)
        self.tree.selectionModel().selectionChanged.connect(self.on_tree_selection)

    def clear(self):
        pass #print "clear"
        #self #self.tree.clear()


    def do_update(self):
        self.model.layoutChanged.emit()

    def on_tree_selection(self):

        if not self.tree.selectionModel().hasSelection():
            return

        midx = self.tree.selectionModel().selectedRows()[0]
        err = self.model.get_error(midx)
        self.sigGotoError.emit(err)



    def on_update_filter(self):
        return
        self.on_show_warnings()
        self.on_show_errors()
        self.emit_filters_sig()


    def emit_filters_sig(self):
        self.sigErrorsFilter.emit(self.buttWarnings.isChecked(), self.buttErrors.isChecked())

    def get_error_filters(self):
        return self.buttWarnings.isChecked(), self.buttErrors.isChecked()

    def select_from_cell(self, cell):

        self.model.set_highlight( cell )


    def deadselect_from_cell(self, cell):
        self.tree.blockSignals(True)

        # clear selection and  hightlight colors
        self.tree.clearSelection()
        root = self.tree.invisibleRootItem()
        for i in range(0, root.childCount()):
            root.child(i).set_bg(C_ERR.highlight, "white")

        if ridx != None and cidx != None:
            # search and hightlight row/col if any
            search = "%s-%s" % (ridx, cidx)
            items = self.tree.findItems(search, Qt.MatchExactly, C_ERR.search)
            if len(items) > 0:
                for item in items:
                    item.set_bg(C_ERR.highlight, "purple")
        self.tree.blockSignals(False)
