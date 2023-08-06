# -*- coding: utf-8 -*-


from Qt import QtGui, QtWidgets, QtCore, Qt, pyqtSignal



from img import Ico
import xwidgets



class GroupListModel(QtCore.QAbstractItemModel):

    class C:
        data_count = 0
        group_code = 1
        group_description = 2

    def __init__(self, parent=None, ogtDoc=None):
        QtCore.QAbstractItemModel.__init__(self)

        self.ogtDoc = ogtDoc

        self._col_labels = ["Data", "Group Code", "Descripton"]

    def index(self, row, col, parent=None):
        return self.createIndex(row, col)

    def parent(self, pidx=None):
        return QtCore.QModelIndex()


    def columnCount(self, foo):
        return 3

    def rowCount(self, midx):
        return self.ogtDoc.groups_count

    def data(self, midx, role=Qt.DisplayRole):
        """Returns the data at the given index"""
        row = midx.row()
        col = midx.column()

        if role == Qt.DisplayRole or role == Qt.EditRole:
            grp = self.ogtDoc.group_from_index(row)

            if col == self.C.group_code:
                return grp.group_code

            if col == self.C.group_description:
                return grp.group_description

            if col == self.C.data_count:
                return grp.data_rows_count

            return "?"


        if role == Qt.DecorationRole:
            if col == self.C.group_code:
                return Ico.icon(Ico.Group)

        if role == Qt.FontRole:
            if col == self.C.group_code:
                f = QtGui.QFont()
                f.setBold(True)
                f.setFamily("monospace")
                return f

        if role == Qt.TextAlignmentRole:
            return Qt.AlignRight if col == 0 else Qt.AlignLeft

        if False and role == Qt.BackgroundColorRole:
            cell = self.ogtDoc.group_from_index(row)[col]
            bg = cell.get_bg()
            if len(self.ogtGroup.data_cell(row, col).errors) > 0:
                pass
            return QtWidgets.QColor(bg)


        return QtCore.QVariant()


    def headerData(self, idx, orient, role=None):
        if role == Qt.DisplayRole and orient == Qt.Horizontal:
            return QtCore.QVariant(self._col_labels[idx])

        if role == Qt.TextAlignmentRole and orient == Qt.Horizontal:
            return Qt.AlignRight if idx == 0 else Qt.AlignLeft

        return QtCore.QVariant()


class GroupsListWidget( QtWidgets.QWidget ):

    def __init__( self, parent=None, ogtDoc=None):
        QtWidgets.QWidget.__init__( self, parent )

        self.debug = False

        self.setMinimumWidth(300)

        self.mainLayout = xwidgets.vlayout()
        self.setLayout(self.mainLayout)


        self.tree = QtWidgets.QTreeView()
        self.mainLayout.addWidget(self.tree)

        self.model = GroupListModel(ogtDoc=ogtDoc)
        self.tree.setModel(self.model)

        self.tree.setMinimumWidth(300)
        self.tree.setRootIsDecorated(False)
        self.tree.setExpandsOnDoubleClick(False)
        self.tree.header().setStretchLastSection(True)

        self.tree.setColumnWidth(GroupListModel.C.data_count, 40)


    def do_update(self):
        self.model.layoutChanged.emit()



    def DEADload_projects(self, sub_dir=None):
        return
        files_list, err = ags4.examples_list()
        if err:
            pass #TODO
        self.tree.clear()

        for fd in files_list:
            file_name = fd["file_name"]
            item = QtWidgets.QTreeWidgetItem()
            item.setText(C_EG.file_name, file_name)
            item.setIcon(C_EG.file_name, Ico.icon(Ico.Ags4))
            f = item.font(C_EG.file_name)
            f.setBold(True)
            item.setFont(C_EG.file_name, f)
            self.tree.addTopLevelItem(item)



    def deadon_tree_item_clicked(self, item, col):

        file_name = str(item.text(C_EG.file_name))
        self.sigFileSelected.emit(file_name)
