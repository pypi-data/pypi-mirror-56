# -*- coding: utf-8 -*-

import os
from Qt import QtGui, QtWidgets, QtCore, Qt, pyqtSignal

import app_globals as G

from ogt import ags4, FORMATS

from img import Ico
import xwidgets
import ags4_models
import ogtgui_group




class AbbrPickDialog( QtWidgets.QDialog ):

    def __init__( self, parent=None, ogtHead=None, editCell=None):
        QtWidgets.QDialog.__init__( self, parent )

        self.ogtHead = ogtHead
        self.editCell = editCell

        self.selected = None


        self.mainLayout = xwidgets.vlayout(margin=0)
        self.setLayout(self.mainLayout)

        self.setWindowTitle("Picklist")
        self.setWindowIcon(Ico.icon(Ico.TypePicklist))

        topLay = xwidgets.hlayout(spacing=5)
        self.mainLayout.addLayout(topLay)

        sty = "background-color: #555555; color: #dddddd; padding: 4px;"
        self.lblTitle = xwidgets.XLabel(text="-", style=sty)
        topLay.addWidget(self.lblTitle)

        self.mainLayout.addSpacing(10)

        self.modelAbbrs = ags4_models.AbbrevItemsModel(ogtHead=self.ogtHead)
        #self.modelAbbrs.sigCheckedChanged.connect(self.on_checked_changed)

        #== tree
        self.tree = QtWidgets.QTreeView()
        self.mainLayout.addWidget(self.tree)
        self.tree.setModel(self.modelAbbrs)

        self.tree.setExpandsOnDoubleClick(False)
        self.tree.setRootIsDecorated(False)
        self.tree.setUniformRowHeights(True)
        self.tree.setAlternatingRowColors(True)
        self.tree.setMinimumHeight(700)
        self.tree.setMinimumWidth(500)

        #self.tree.setSelectionMode(QtWidgets.QAbstractItemView.SelectRows)
        #self.tree.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tree.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        #self.tree.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        CA = ags4_models.AbbrevItemsModel.CA

        self.tree.header().setSectionResizeMode(CA.description, QtWidgets.QHeaderView.Stretch)

        self.tree.setColumnWidth(CA.check, 15)
        self.tree.setColumnWidth(CA.code, 80)
        #self.tree.setColumnWidth(ags4_models.AbbrevItemsModel.CA.description, 200)

        self.statusBar = QtWidgets.QStatusBar()
        self.mainLayout.addWidget(self.statusBar)


        ## ================ Button BAr
        buttLay = xwidgets.hlayout(spacing=5, margin=5)
        self.mainLayout.addLayout(buttLay)

        self.buttCancel = xwidgets.XPushButton(callback=self.on_add, ico=Ico.Add, text="Add")
        buttLay.addWidget(self.buttCancel)


        lbl = xwidgets.XLabel(text="Right click to edit")
        buttLay.addWidget(lbl)
        buttLay.addStretch(3)

        self.buttCancel = xwidgets.CancelButton(callback=self.on_cancel)
        buttLay.addWidget(self.buttCancel)

        self.buttSave = xwidgets.SaveButton(callback=self.on_save, text="Select")
        buttLay.addWidget(self.buttSave)

        #self.modelAbbrs.set_checked(editCell.value)
        self.do_select_update()

    def on_checked_changed(self):
        self.update_statusBar()

    def on_add(self):
        self.show_edit_dialog(dict(code="", description="", list="custom"))

    def on_edit(self):
        pass

    def show_edit_dialog(self, rec):
        d = AbbrEditDialog(rec=rec)
        if d.exec_():
            self.ogtHead.parentGroup.parentDoc.add_abbr(self.ogtHead.head_code, d.rec)
            print(d.rec, self)
            self.modelAbbrs.load_data()
            self.modelAbbrs.set_checked(d.rec)

    def do_select_update(self):

        sels = []
        if self.ogtHead.parent_group.parentDoc.concat_char() in self.editCell.value:
            sels = self.editCell.value.split(self.ogtHead.parentGroup.parentDoc.concat_char())
        else:
            sels = self.editCell.value

        self.modelAbbrs.set_checked(sels)

        s = "<b>%s</b>: %s" % (self.ogtHead.head_code, self.ogtHead.head_description)
        self.lblTitle.setText(s)

        self.update_statusBar()

    def update_statusBar(self):
        codes = self.modelAbbrs.checked_codes()
        #lst = ["<b>%s</b>" % c for c in codes]
        sta = "%s - %s selected [%s]" % (self.modelAbbrs.rowCount(), len(codes), ",".join(codes) )
        self.statusBar.showMessage(sta)


    def on_cancel(self):
        self.reject()

    def on_save(self):

        rec = self.modelAbbrs.get_checked()
        if rec is not None:
            self.editCell.value = rec['code']
        self.ogtHead.emit()
        self.accept()



    # def sson_tree_clicked(self, midx):
    #     val = self.model.val_from_midx(midx)
    #     self.cell.value = val['code']
    #     self.accept()



class AbbrEditDialog( QtWidgets.QDialog ):

    def __init__( self, parent=None, rec=None):
        QtWidgets.QDialog.__init__( self, parent )

        self.rec = rec

        self.setWindowTitle("Edit Abbrev")
        self.setWindowIcon(Ico.icon(Ico.AgsAbbrevItem))
        self.setMinimumWidth(600)

        self.mainLayout = xwidgets.vlayout(margin=10, spacing=10)
        self.setLayout(self.mainLayout)


        self.grid = QtWidgets.QGridLayout()
        self.mainLayout.addLayout(self.grid)

        self.grid.addWidget(QtWidgets.QLabel("Code [ABBR_CODE]"), 0, 0)
        self.grid.addWidget(QtWidgets.QLabel("Description  [ABBR_DESC]"), 0, 1)
        self.grid.addWidget(QtWidgets.QLabel("List  [ABBR_LIST]"), 0, 2)

        self.txtCode = xwidgets.XLineEdit()
        self.grid.addWidget(self.txtCode, 1, 0)

        self.txtDesc = xwidgets.XLineEdit()
        self.grid.addWidget(self.txtDesc, 1, 1)

        self.txtlist = xwidgets.XLineEdit()
        self.grid.addWidget(self.txtlist, 1, 2)


        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 2)
        self.grid.setColumnStretch(2, 1)

        ## ================
        buttLay = xwidgets.hlayout()
        self.mainLayout.addLayout(buttLay)

        buttLay.addStretch(3)

        self.buttCancel = xwidgets.CancelButton(callback=self.on_cancel)
        buttLay.addWidget(self.buttCancel)

        self.buttSave = xwidgets.SaveButton(callback=self.on_save, text="Save")
        buttLay.addWidget(self.buttSave)

        self.txtCode.editingFinished.connect(self.on_code_edited)
        self.load_rec()


    def load_rec(self):
        if self.rec == None:
            return
        self.txtCode.setText(self.rec['code'])
        self.txtDesc.setText(self.rec['description'])
        self.txtlist.setText(self.rec['list'])

    def on_code_edited(self):
        self.txtCode.setText(self.txtCode.text().upper())

    def on_cancel(self):
        self.reject()

    def on_save(self):
        self.rec = dict(code=self.txtCode.s(), description=self.txtDesc.s(), list=self.txtlist.s())
        self.accept()



class DataTypeSelectDialog( QtWidgets.QDialog ):

    def __init__( self, parent, ogtHead):
        QtWidgets.QDialog.__init__( self, parent )

        self.ogtHead = ogtHead

        self.mainLayout = xwidgets.vlayout()
        self.setLayout(self.mainLayout)

        self.setWindowTitle("Select Type")
        self.setWindowIcon(Ico.icon(Ico.TypePicklist))


        self.tree = QtWidgets.QTreeView()
        self.tree.setRootIsDecorated(False)
        self.tree.setAlternatingRowColors(True)
        self.tree.setMinimumHeight(600)
        self.tree.setMinimumWidth(400)
        self.mainLayout.addWidget(self.tree)

        self.model = G.ags.modelDataTypes
        self.tree.setModel(self.model)
        self.tree.clicked.connect(self.on_tree_clicked)

        idx = self.model.midx_from_val(  self.ogtHead.data_type_cell.value  )
        if idx:
            self.tree.selectionModel().select(idx, QtCore.QItemSelectionModel.SelectCurrent|QtCore.QItemSelectionModel.Rows)

    def on_tree_clicked(self, midx):
        val = G.ags.modelDataTypes.val_from_midx(midx)
        self.ogtHead.data_type_cell.value = val['code']
        self.accept()


class UnitSelectDialog( QtWidgets.QDialog ):


    def __init__( self, parent, ogtHead):
        QtWidgets.QDialog.__init__( self, parent )

        self.ogtHead = ogtHead

        self.mainLayout = xwidgets.vlayout()
        self.setLayout(self.mainLayout)

        self.setWindowTitle("Select Unit")
        self.setWindowIcon(Ico.icon(Ico.TypePicklist))


        self.tree = QtWidgets.QTreeView()
        self.tree.setRootIsDecorated(False)
        self.tree.setAlternatingRowColors(True)
        self.tree.setMinimumHeight(600)
        self.mainLayout.addWidget(self.tree)

        self.tree.setModel(G.ags.modelUnits)
        self.tree.clicked.connect(self.on_tree_clicked)

        idx = G.ags.modelUnits.midx_from_val(  self.ogtHead.unit_cell.value  )
        if idx:
            self.tree.selectionModel().select(idx, QtWidgets.QItemSelectionModel.SelectCurrent|QtWidgets.QItemSelectionModel.Rows)

    def on_tree_clicked(self, midx):
        val = G.ags.modelUnits.val_from_midx(midx)
        self.ogtHead.unit_cell.value = val['unit']
        self.accept()



class PickIDDialog( QtWidgets.QDialog ):

    def __init__( self, parent, ogtGroup, ogtHead, cell):
        QtWidgets.QDialog.__init__( self, parent )

        self.ogtGroup = ogtGroup
        self.ogtHead = ogtHead
        self.cell = cell


        self.mainLayout = xwidgets.vlayout()
        self.setLayout(self.mainLayout)

        self.setWindowTitle("Pick ID")
        self.setWindowIcon(Ico.icon(Ico.TypePicklist))


        self.tree = QtWidgets.QTreeView()
        self.mainLayout.addWidget(self.tree)


        self.tree.setRootIsDecorated(False)
        self.tree.setUniformRowHeights(True)
        self.tree.setAlternatingRowColors(True)
        self.tree.setMinimumHeight(700)
        self.tree.setMinimumWidth(900)

        self.tree.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tree.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.model = ogtgui_group.GroupDataModel(self, self.ogtGroup)
        self.tree.setModel(self.model)

        self.tree.clicked.connect(self.on_tree_clicked)

        self.do_select()

    def do_select(self):
        cidx = self.ogtGroup.index_of_heading(self.ogtHead.head_code)
        if self.ogtGroup.ogtDoc.concat_char in self.cell.value:
            dsa

        idx = self.model.midx_from_val(cidx, self.cell.value)
        if idx:
            self.tree.selectionModel().select(idx,
                                              QtWidgets.QItemSelectionModel.SelectCurrent | QtWidgets.QItemSelectionModel.Rows)


    def on_tree_clicked(self, midx):
        xcell = self.model.val_from_midx(midx)
        self.cell.value = xcell.value
        self.accept()


class HeadingsSelectDialog( QtWidgets.QDialog ):


    def __init__( self, parent, ogtGroup):
        QtWidgets.QDialog.__init__( self, parent )

        self.ogtGroup = ogtGroup

        self.mainLayout = xwidgets.vlayout()
        self.setLayout(self.mainLayout)

        self.setWindowTitle("Select Headings")
        self.setWindowIcon(Ico.icon(Ico.TypePicklist))
        self.setMinimumWidth(700)
        self.setMinimumHeight(700)

        self.model = ags4_models.HeadingsModel(self)


        self.tree = QtWidgets.QTreeView()
        self.tree.setModel(self.model)
        self.mainLayout.addWidget(self.tree)

        self.tree.setRootIsDecorated(False)
        self.tree.setAlternatingRowColors(True)
        self.tree.setMinimumHeight(600)

        self.tree.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        self.tree.clicked.connect(self.on_tree_clicked)

        self.model.set_group(ags4.DD.group(self.ogtGroup.group_code))


        self.buttGroup = QtWidgets.QButtonGroup()
        self.buttGroup.setExclusive(False)
        self.buttGroup.buttonClicked.connect(self.on_add_button)

        self.setup_buttons()
        self.update_buttons()

        self.tree.update()

    def setup_buttons(self):

        for ridx in range(0, self.model.rowCount()):
            midx = self.model.index(ridx, 0)
            butt = xwidgets.XToolButton()
            self.tree.setIndexWidget(midx, butt)
            self.buttGroup.addButton(butt, ridx)

    def update_buttons(self):

        for ridx in range(0, self.model.rowCount()):

            midx = self.model.index(ridx, 0)
            butt = self.tree.indexWidget(midx)

            heading = self.model.data(self.model.index(ridx, ags4_models.HeadingsModel.CH.head_code), Qt.DisplayRole)
            exists = heading in self.ogtGroup.headings_index

            if exists:
                butt.setText("Remove")
                butt.setIco(Ico.Minus)
                butt.setVisible(False)
            else:
                butt.setText("Add")
                butt.setIco(Ico.Plus)
                butt.show()
                butt.setVisible(True)




    def on_add_button(self, butt):
        ridx = self.buttGroup.id(butt)

        midx = self.model.index(ridx, ags4_models.HeadingsModel.CH.head_code)
        rec = self.model.rec_from_midx(midx)

        ogtHead = self.ogtGroup.add_heading(rec)
        print("on_add", ogtHead, self)
        self.update_buttons()


    def on_tree_clicked(self, midx):
        print(midx)

        return
        val = G.ags.modelUnits.val_from_midx(midx)
        self.ogtHead.unit_cell.value = val['unit']
        self.accept()


class EXT:
    ags = ["ags", "ags4"]
    excel = ["xlsx"]
    zip = ["zip"]
    all = ags + excel + zip

class XFileSystemModel(QtWidgets.QFileSystemModel):

    def __init__( self, parent=None):
        QtWidgets.QFileSystemModel.__init__( self, parent )

    def _get_ext(self, midx):
        return QtCore.QFileInfo( self.data(midx, Qt.DisplayRole).lower() ).suffix()

    def data(self, midx, role ):

        if midx.column() == 0:
            if role == Qt.DecorationRole:

                ext = self._get_ext(midx)

                if not self.isDir(midx):


                    if ext in EXT.ags:
                        return Ico.icon(Ico.Ags4)

                    if ext in EXT.excel:
                        return Ico.icon(Ico.Excel)

                    #if ext in EXT.zip:
                    #    return Ico.icon(Ico.Zip)

            if role == Qt.FontRole:

                if self._get_ext(midx) in EXT.all:
                    f = QtGui.QFont()
                    f.setBold(True)
                    return f


        return QtWidgets.QFileSystemModel.data(self, midx, role)

class FileSelectDialog( QtWidgets.QDialog ):

    def __init__( self, parent, multi=False, root=None):
        QtWidgets.QDialog.__init__( self, parent )

        self.multi = multi

        self.file_path = None

        self.mainLayout = xwidgets.vlayout()
        self.setLayout(self.mainLayout)

        self.setWindowTitle("Select Files")
        self.setWindowIcon(Ico.icon(Ico.TypePicklist))

        ##= Model
        #ROOT_PATH = "/home/ogt"
        self.model = XFileSystemModel()



        ##= Tree
        self.tree = QtWidgets.QTreeView()
        self.tree.setModel(self.model)
        self.mainLayout.addWidget(self.tree)


        #self.tree.setRootIsDecorated(False)
        self.tree.setUniformRowHeights(True)
        self.tree.setAlternatingRowColors(True)
        self.tree.setMinimumHeight(700)
        self.tree.setMinimumWidth(900)

        self.tree.setColumnWidth(0, 250)


        self.tree.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection if multi else QtWidgets.QAbstractItemView.SingleSelection)
        self.tree.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.tree.clicked.connect(self.on_tree_clicked)

        buttlay = xwidgets.hlayout(margin=3)
        self.mainLayout.addLayout(buttlay)
        buttlay.addStretch(12)

        self.buttCancel = xwidgets.CancelButton(self)
        buttlay.addWidget(self.buttCancel)

        self.buttSave = xwidgets.SaveButton(self, text="Open")
        buttlay.addWidget(self.buttSave)

        self.set_root(root)

    def set_root(self, root):
        if root == None:
            #root = self.model.myComputer()
            root = os.path.expanduser("~")
        self.model.setRootPath(root)
        self.tree.setRootIndex(self.model.index(root))


    def on_reject(self):
        self.reject()

    def on_accept(self):

        midx = self.tree.selectedIndexes()[0]
        self.file_path = self.model.data(midx, QtWidgets.QFileSystemModel.FilePathRole)

        self.accept()



    def on_tree_clicked(self, midx):
        pass


class SaveExportDialog( QtWidgets.QDialog ):

    def __init__( self, parent, ogtDoc):
        QtWidgets.QDialog.__init__( self, parent )

        self.ogtDoc = ogtDoc

        self.setWindowTitle("Save & Export Files")
        self.setWindowIcon(Ico.icon(Ico.Export))#
        self.setMinimumWidth(700)
        self.setMinimumHeight(600)

        self.mainLayout = xwidgets.vlayout(margin=10)
        self.setLayout(self.mainLayout)

        self.buttGroup = QtWidgets.QButtonGroup()
        self.buttGroup.setExclusive(False)
        self.buttGroup.buttonClicked.connect(self.on_button)

        self.buttGroupFormat = QtWidgets.QButtonGroup()
        self.buttGroupFormat.setExclusive(True)
        self.buttGroupFormat.buttonClicked.connect(self.on_button_preview_format)

        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(5)
        self.mainLayout.addLayout(self.grid)

        sty = "background-color: white; padding: 3px;"
        row = 0
        self.grid.addWidget(xwidgets.XLabel(text="File Path:"), row, 0, 1, 1, Qt.AlignRight)
        self.lblFilePath = xwidgets.XLabel(text=os.path.dirname(self.ogtDoc.source_file_path),
                                           style=sty)
        self.grid.addWidget(self.lblFilePath, row, 1)

        row += 1
        self.grid.addWidget(xwidgets.XLabel(text="File Name:"), row, 0, 1, 1, Qt.AlignRight)
        self.lblFileName = xwidgets.XLabel(text=os.path.basename(self.ogtDoc.source_file_path),
                                           style=sty)
        self.grid.addWidget(self.lblFileName, row, 1)

        row += 1
        self.grid.addWidget(xwidgets.XLabel(text="Format:"), row, 0, 1, 1, Qt.AlignRight|Qt.AlignTop)

        self.lbls = []
        radLay = QtWidgets.QGridLayout()
        radLay.setSpacing(5)
        self.grid.addLayout(radLay, row, 1)
        for xidx, ext in enumerate(["json", "yaml", "xlsx", "ags4"]):
            butt = QtWidgets.QCheckBox()
            butt.setText(ext)
            radLay.addWidget(butt, xidx, 0)
            self.buttGroup.addButton(butt, xidx)

            bn = os.path.basename(self.ogtDoc.source_file_path) + "." + ext
            lbl = xwidgets.XLabel(text=bn)
            radLay.addWidget(lbl, xidx, 1)
            lbl.hide()
            self.lbls.append(lbl)
        radLay.setColumnStretch(0, 1)
        radLay.setColumnStretch(1, 4)

        row += 1
        self.grid.addWidget(xwidgets.XLabel(text="Extended:"), row, 0, 1, 1, Qt.AlignRight | Qt.AlignTop)
        self.chkExtended = QtWidgets.QCheckBox()
        self.chkExtended.setText("include descriptions etc")
        self.grid.addWidget(self.chkExtended, row, 1)
        self.buttGroup.addButton(self.chkExtended)

        row += 1
        self.grid.addWidget(xwidgets.XLabel(text="Minify:"), row, 0, 1, 1, Qt.AlignRight | Qt.AlignTop)
        self.chkMinify = QtWidgets.QCheckBox()
        self.chkMinify.setText("Removed whitespace (json only)")
        self.grid.addWidget(self.chkMinify, row, 1)
        self.buttGroup.addButton(self.chkMinify)

        row += 1
        self.grid.addWidget(xwidgets.XLabel(text="Overwrite:"), row, 0, 1, 1, Qt.AlignRight | Qt.AlignTop)
        self.chkOverwrite = QtWidgets.QCheckBox()
        self.chkOverwrite.setText("Overwrite existing files")
        self.grid.addWidget(self.chkOverwrite, row, 1)


        row += 1
        #self.grid.addWidget(xwidgets.XLabel(text="Preview:"), row, 0, Qt.AlignRight | Qt.AlignTop)

        radLay = xwidgets.hlayout(spacing=5)
        radLay.addWidget(xwidgets.XLabel(text="Preview:"), 0)

        self.grid.addLayout(radLay, row, 0, 1, 2,  Qt.AlignLeft)
        for idx, ext in enumerate(["json", "yaml", "ags4"]):
            butt = QtWidgets.QRadioButton()
            butt.setText(ext)
            radLay.addWidget(butt, 0)
            if idx == 0:
                butt.setChecked(True)
            self.buttGroupFormat.addButton(butt, idx)
        radLay.addStretch(10)

        row += 1
        self.txtPreview = QtWidgets.QTextEdit()
        self.txtPreview.setStyleSheet("font-size: 8pt; font-family: monospace;")
        self.txtPreview.setMinimumHeight(300)
        self.grid.addWidget(self.txtPreview, row, 0, 1, 2)

        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 3)

        self.mainLayout.addSpacing(10)

        self.botLay = xwidgets.hlayout()
        self.mainLayout.addLayout(self.botLay)

        self.botLay.addStretch(10)

        self.statusBar = QtWidgets.QStatusBar()
        self.botLay.addWidget(self.statusBar, 10)
        #self.buttCancel = xwidgets.CancelButton(self)
        #self.botLay.addWidget(self.buttCancel)

        self.buttSave = xwidgets.XPushButton(text="Write Files", ico=Ico.Export, callback=self.on_accept)

        self.botLay.addWidget(self.buttSave)
        self.buttSave.setEnabled(False)

        self.update_preview()

    def on_button(self, butt=None):

        can_save = False
        for id in range(0, 4):
            butt = self.buttGroup.button(id)
            #print(butt.text(), butt.isChecked())
            self.lbls[id].setVisible(butt.isChecked())
            if butt.isChecked():
                can_save = True

        self.buttSave.setEnabled(can_save)
        self.update_preview()

    def on_button_preview_format(self):
        self.update_preview()

    def update_preview(self):

        self.ogtDoc.opts.minify = self.chkMinify.isChecked()
        self.ogtDoc.opts.extended = self.chkExtended.isChecked()

        if self.buttGroupFormat.checkedId() == 0:
            s, err = self.ogtDoc.to_json()

        elif self.buttGroupFormat.checkedId() == 1:
            s, err = self.ogtDoc.to_yaml()
        else:
            s, err = self.ogtDoc.to_ags4()
        self.txtPreview.setText(s)

    def on_reject(self):
        self.reject()

    def on_accept(self):

        over = True
        sty_green = "color: green;"
        ## json
        if self.buttGroup.button(0).isChecked():
            #fp = self.ogtDoc.source_file_path + ".json"
            mess, err = self.ogtDoc.write(ext="json", beside=True, overwrite=over, file_path=None)
            print(mess, err)
            if err is None:
                self.lbls[0].setStyleSheet(sty_green)


        ## yaml
        if self.buttGroup.button(1).isChecked():
            #fp = self.ogtDoc.source_file_path + ".yaml"
            mess, err = self.ogtDoc.write(ext="yaml", beside=True, overwrite=over, file_path=None)
            print(mess, err)
            if err is None:
                self.lbls[1].setStyleSheet(sty_green)

        ## xlsx
        if self.buttGroup.button(2).isChecked():
            #fp = self.ogtDoc.source_file_path + ".xlsx"
            mess, err = self.ogtDoc.write(ext="xlsx", beside=True, overwrite=over, file_path=None)
            print(mess, err)
            if err is None:
                self.lbls[2].setStyleSheet(sty_green)

        self.statusBar.showMessage("Saved", 2000)


