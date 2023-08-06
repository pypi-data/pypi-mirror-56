# -*- coding: utf-8 -*-


from Qt import QtGui, QtWidgets, QtCore, Qt, pyqtSignal

from ogt import ags4

#import app_globals as G
from ogtgui.settings import Settings

from ogtgui.img import Ico
from ogtgui import xwidgets
from ogtgui.ags4_models import AgsData, CG, AGS4_COLORS, HeadingsModel, AbbrevItemsModel
from ogtgui import ags4_widgets



def get_edit_widget(data_type, value=None):

    dt = data_type.upper().strip()

    ## PickList
    if dt == "PA":
        w = QtWidgets.QComboBox()
        w.addItem("-", "")
        return w

    ## Yes No
    if dt == "YN":
        w = QtWidgets.QComboBox()
        w.addItem("-", "")
        w.addItem("Yes", "1")
        w.addItem("No", "0")
        return w

    ## time
    if dt == "T":
        w = QtWidgets.QLineEdit()
        w.setInputMask("00:00:00")
        return w

    ## Deg, Mins, Secs
    if dt == "DMS":
        w = QtWidgets.QLineEdit()
        w.setInputMask("000.00.00")
        return w

    ## Date Time
    if dt == "DT":
        w = QtWidgets.QDateTimeEdit()
        w.setDisplayFormat("dd-mm-yyyy HH:mm:ss")
        return w

    if dt.endswith("DP"):

        opts = ["0DP", '1DP', "2DP", "3DP", "4DP"]
        dp = opts.index(dt) # get sigIndex from array position
        if dp == 0:
            # No decimals so a spinbox
            w = QtWidgets.QSpinBox()
            return w

        w = QtWidgets.QDoubleSpinBox()
        w.setDecimals(dp)
        return w

    if dt.endswith("SF"):
        w = QtWidgets.QDoubleSpinBox()
        w.setDecimals(5)
        return w

    if dt in ["X", "U", "XN"]:
        w = QtWidgets.QLineEdit()
        return w


    return None

def show_group_dialog(parent, group_code):
    d = AGS4GroupViewDialog(parent=parent, group_code=group_code)
    d.exec_()

class AGS4DataDictBrowser( QtWidgets.QWidget ):

    def __init__( self, parent=None, mode=None ):
        QtWidgets.QWidget.__init__( self, parent )

        self.debug = False

        AgsData.load_init()

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.mainLayout)

        ##=============================================================
        self.tabWidget = QtWidgets.QTabWidget()
        self.mainLayout.addWidget(self.tabWidget)


        ##=============================================================
        self.agsGroupsWidget = AGS4GroupsBrowser(self)
        self.tabWidget.addTab(self.agsGroupsWidget, Ico.icon(Ico.AgsGroups), "Groups")

        self.unitsTypesWidget = AGS4UnitsTypesWidget(self)
        self.tabWidget.addTab(self.unitsTypesWidget, Ico.icon(Ico.AgsField), "Units && Types")

        ##=============================================================
        #self.agsAbbrevsWidget = AgsAbbrevsWidget.AgsAbbrevsWidget(self)
        #self.tabWidget.addTab(self.agsAbbrevsWidget,dIco.icon(dIco.AgsAbbrevs),  "Abbreviations / Pick lists")

        ##=============================================================
        #self.agsUnitsWidget = AgsUnitsWidget.AgsUnitsWidget(self)
        #self.tabWidget.addTab(self.agsUnitsWidget, dIco.icon(dIco.AgsUnits), "Units")



    def init_load(self):

        # load data dict
        #G.ags.init_load()
        #self.tabWidget.setCurrentIndex(1)

        self.agsGroupsWidget.set_focus()


class AGS4GroupsBrowser( QtWidgets.QWidget ):
    """The left panel with the classes, filter and groups table underneath"""

    sigGroupSelected = pyqtSignal(object)

    def __init__( self, parent=None):
        QtWidgets.QWidget.__init__( self, parent )

        self.debug = False
        self.setObjectName("AGS4GroupsBrowser")

        self.proxy = QtCore.QSortFilterProxyModel()
        self.proxy.setSourceModel(AgsData.modelGroups)
        self.proxy.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)


        ##===============================================
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.mainLayout)

        self.splitter = QtWidgets.QSplitter(self)
        self.splitter.setObjectName(self.objectName() + "groups_splitter")
        self.mainLayout.addWidget(self.splitter)

        ##############################################################################
        leftWidget = QtWidgets.QWidget()
        leftLayout = xwidgets.vlayout()
        leftWidget.setLayout(leftLayout)
        self.splitter.addWidget(leftWidget)


        self.tabFilter = QtWidgets.QTabWidget()
        leftLayout.addWidget(self.tabFilter)

        ##================================
        ## Filter
        grpFilter = xwidgets.GroupGridBox()
        mmm = 5
        grpFilter.setContentsMargins(mmm, mmm, mmm, mmm)
        self.tabFilter.addTab(grpFilter, "Filter")


        # filter radios
        self.buttGroupFilter = QtWidgets.QButtonGroup()
        self.buttGroupFilter.setExclusive(True)

        for ridx, s in enumerate(["Code", "Description", "Code + Description"]):
            rad = QtWidgets.QRadioButton()
            rad.setText(s)
            grpFilter.grid.addWidget(rad, ridx, 0, 1, 2)
            self.buttGroupFilter.addButton(rad, 3 if ridx == 2 else ridx)

        self.buttGroupFilter.button(0).setChecked(True)
        self.buttGroupFilter.buttonClicked.connect(self.on_filter_col)


        # clear button
        self.buttClear = xwidgets.ClearButton(self, callback=self.on_clear_filter)
        grpFilter.grid.addWidget(self.buttClear, 3, 0)

        ## filter text
        self.txtFilter = QtWidgets.QLineEdit()
        self.txtFilter.setMaximumWidth(100)
        grpFilter.grid.addWidget(self.txtFilter, 3, 1)
        self.txtFilter.textChanged.connect(self.on_txt_changed)


        grpFilter.grid.addWidget(QtWidgets.QLabel(), 4, 2)

        #grpFilter.layout.addStretch(3)
        grpFilter.grid.setColumnStretch(0, 0)
        grpFilter.grid.setColumnStretch(1, 10)

        ##================================
        ## Classification Tree
        topLayout = QtWidgets.QVBoxLayout()
        leftLayout.addLayout(topLayout, 0)

        self.treeClass = QtWidgets.QTreeView()
        self.tabFilter.addTab(self.treeClass, "By classification")
        self.treeClass.setModel(AgsData.modelClasses)
        self.treeClass.setRootIsDecorated(False)

        self.treeClass.setExpandsOnDoubleClick(False)

        self.treeClass.setFixedHeight(220)

        self.treeClass.selectionModel().selectionChanged.connect(self.on_class_tree_selected)




        ##== Groups Tree
        self.treeGroups = QtWidgets.QTreeView()
        leftLayout.addWidget(self.treeGroups, 10)
        self.treeGroups.setModel(self.proxy)


        self.treeGroups.setUniformRowHeights(True)
        self.treeGroups.setRootIsDecorated(False)
        self.treeGroups.setAlternatingRowColors(True)

        self.treeGroups.header().setStretchLastSection(True)
        self.treeGroups.setColumnHidden(CG.search, True)
        self.treeGroups.setColumnWidth(CG.code, 120)
        self.treeGroups.setColumnWidth(CG.description, 250)

        self.treeGroups.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeGroups.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeGroups.setItemsExpandable(False)
        self.treeGroups.setExpandsOnDoubleClick(False)

        self.treeGroups.setSortingEnabled(True)
        self.treeGroups.sortByColumn(CG.code, Qt.AscendingOrder)

        self.treeGroups.selectionModel().selectionChanged.connect(self.on_groups_tree_selected)

        self.agsGroupViewWidget = AGS4GroupViewWidget(self)
        self.splitter.addWidget(self.agsGroupViewWidget)

        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 5)
        Settings.restore_splitter(self.splitter)
        self.splitter.splitterMoved.connect(self.on_splitter_moved)

        #self.statusBar = QtWidgets.QStatusBar()
        #self.mainLayout.addWidget(self.statusBar, 0)


        ##############################################################################
        rightWidget = QtWidgets.QWidget()
        rightLayout = xwidgets.vlayout()
        rightWidget.setLayout(rightLayout)
        self.splitter.addWidget(rightWidget)


        #self.agsHeadingDetailWidget = AGS4HeadingDetailWidget()
        #rightLayout.addWidget(self.agsHeadingDetailWidget)

        #self.init_setup()
        AgsData.sigLoaded.connect(self.on_loaded)

        #self.txtFilter.setText("DETL")

    def on_splitter_moved(self, i, pos):
        Settings.save_splitter(self.splitter)

    def set_focus(self):
        self.txtFilter.setFocus()

    #=========================================
    def on_groups_tree_selected(self, sel=None, desel=None):

        if not self.treeGroups.selectionModel().hasSelection():
             self.agsGroupViewWidget.set_group( None )
             self.sigGroupSelected.emit( None )
             return

        tIdx = self.proxy.mapToSource( sel.indexes()[0] )
        grp_dic = self.proxy.sourceModel().rec_from_midx( tIdx )
        self.agsGroupViewWidget.set_group(grp_dic)
        self.sigGroupSelected.emit( grp_dic )


    def on_filter_col(self, idx):
        self.update_filter()
        self.txtFilter.setFocus()

    def on_txt_changed(self, x):
        self.update_filter()

    def update_filter(self):
        self.treeClass.blockSignals(True)
        self.treeClass.clearSelection()
        self.treeClass.blockSignals(False)

        cidx = self.buttGroupFilter.checkedId()
        self.proxy.setFilterKeyColumn(cidx)

        txt = str(self.txtFilter.text()).strip()
        if "_" in txt:
            grp_code, _ = txt.split("_")
        else:
            grp_code = txt
        self.proxy.setFilterFixedString(grp_code)

        if self.proxy.rowCount() == 1:

            # TODO
            # #self.tree.selectionModel().select(self.proxy.index(0,0))
            pass


    def on_clear_filter(self):
        self.txtFilter.setText("")
        self.txtFilter.setFocus()



    def on_class_tree_selected(self, selected, deselected):
        if not self.treeClass.selectionModel().hasSelection():
            self.txtFilter.setFocus()
            #self.on_group_tree_selected()
            return

        self.proxy.setFilterKeyColumn(CG.cls)

        item = self.treeClass.model().itemFromIndex(selected.indexes()[0])
        if item.text() == "All":
            self.proxy.setFilterFixedString("")
        else:
            self.proxy.setFilterFixedString(item.text())
        self.txtFilter.setFocus()


    def init_load(self):
        pass

    def on_loaded(self):

        ## expand first row
        self.treeClass.setExpanded( self.treeClass.model().item(0,0).index(), True)
        self.treeClass.sortByColumn(0, Qt.AscendingOrder)

        ## set sort orders
        self.treeGroups.sortByColumn(CG.code, Qt.AscendingOrder)
        self.treeGroups.resizeColumnToContents(CG.code)




class AGS4GroupViewWidget( QtWidgets.QWidget ):
    """The GroupView contains the vertically the Group Label at top, headings and notes"""

    sigHeadingSelected = pyqtSignal(object)

    def __init__( self, parent=None, mode=None ):
        QtWidgets.QWidget.__init__( self, parent )

        self.group_code = None

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.mainLayout)

        self.topbar = xwidgets.hlayout()
        self.mainLayout.addLayout(self.topbar, 0)

        layInfo = xwidgets.vlayout()
        self.topbar.addLayout(layInfo, 100)

        layInfo2 = xwidgets.hlayout()
        layInfo.addLayout(layInfo2, 0)

        self.icoLabel = xwidgets.IconLabel(self, ico=Ico.AgsGroup)
        self.icoLabel.setStyleSheet("background-color: white; color: #444444;")
        layInfo2.addWidget(self.icoLabel)

        self.lblGroupCode = QtWidgets.QLabel(" ")
        self.lblGroupCode.setStyleSheet("background-color: white; color: %s; font-weight: bold; font-family: monospace; padding: 3px;" % AGS4_COLORS.group)
        self.lblGroupCode.setFixedWidth(50)
        layInfo2.addWidget(self.lblGroupCode)

        lblSpacer = QtWidgets.QLabel(" ")
        lblSpacer.setStyleSheet("background-color: white; color: %s; font-weight: bold; font-family: monospace; padding: 3px;" % AGS4_COLORS.group)
        #self.lblGroupRequired.setFixedWidth(50)
        layInfo2.addWidget(lblSpacer, 100)

        self.lblGroupRequired = QtWidgets.QLabel("Required")
        self.lblGroupRequired.setStyleSheet("background-color: #FFC0CB; color: #444444; font-weight: bold; font-family: monospace; padding: 3px;" )
        self.lblGroupRequired.setVisible(False)
        layInfo2.addWidget(self.lblGroupRequired, 1)

        self.lblDescription = QtWidgets.QLabel(" ")
        self.lblDescription.setStyleSheet("background-color: white; color: #444444; padding: 3px;")
        layInfo.addWidget(self.lblDescription)

        #layInfo.setColumnS

        ##== Parent Child Buttons
        self.buttGrpTB = QtWidgets.QButtonGroup()
        self.buttGrpTB.setExclusive(False)

        self.tbGroupParent = xwidgets.ToolBarGroup(title="Parent")
        self.tbGroupParent.setFixedWidth(70)
        self.topbar.addWidget(self.tbGroupParent, 0)
        self.buttParent = self.tbGroupParent.addButton(text="-", ico=Ico.BulletDown)


        self.tbGroupChildren = xwidgets.ToolBarGroup(title="Children")
        self.topbar.addWidget(self.tbGroupChildren, 0)

        for idx in range(0, 2):
            butt = self.tbGroupChildren.addButton(text="-", ico=Ico.BulletDown)
            butt.setFixedWidth(60)
            self.buttGrpTB.addButton(butt, idx)

        # added after children to make index easy
        self.buttGrpTB.addButton(self.buttParent)
        self.buttGrpTB.buttonClicked.connect(self.on_group_button_clicked)

        self.mainLayout.addSpacing(10)

        ## Headings Table
        self.agsHeadingsTable = AGS4HeadingsTable(self)
        self.mainLayout.addWidget(self.agsHeadingsTable, 10)



        ##== Bottom Splitter
        self.splitBott = QtWidgets.QSplitter()
        self.splitBott.setObjectName("ags_group_view_notes_picklist")
        self.mainLayout.addWidget(self.splitBott)

        ## Notes
        self.agsGroupNotesWidget = AGS4GroupNotesWidget(self)
        self.agsGroupNotesWidget.setFixedHeight(200)
        self.splitBott.addWidget(self.agsGroupNotesWidget)

        ## Abbrs Picklist
        self.agsAbbrevsWidget = AGS4AbbrevsWidget()
        self.splitBott.addWidget(self.agsAbbrevsWidget)


        ## setup splitter
        self.splitBott.setStretchFactor(0, 1)
        self.splitBott.setStretchFactor(1, 1)
        Settings.restore_splitter(self.splitBott)
        self.splitBott.splitterMoved.connect(self.on_splitter_bott_moved)

        self.agsHeadingsTable.sigHeadingSelected.connect(self.on_heading_selection_changed)
        self.agsGroupNotesWidget.sigWordClicked.connect(self.on_word_clicked)

        self.clear_parent_child_buttons()

    def on_group_button_clicked(self, butt):
        group_code = str(butt.text())
        ags4_widgets.show_group_dialog(self, group_code=group_code)

    def on_word_clicked(self, code):
        code = str(code) # WTF!, its a QString not str as sent !
        rec = ags4.DD.words.get(code)
        if rec:

            if rec['type'] == "heading":
                # its a heading, so select it if its in within this group eg SAMP_ID is almost everywhere
                found = self.agsHeadingsTable.select_heading(code)
                if not found:
                    # so its not in this group, so open other group
                    parts = code.split("_")
                    d = AGS4GroupViewDialog(group_code=parts[0], head_code=code)
                    d.exec_()

            if rec['type'] == "group":
                if code != self.group_code:
                    # Dialog only if its not this group
                    d = AGS4GroupViewDialog(group_code=self.group_code)
                    d.exec_()



    def on_splitter_bott_moved(self):
        G.settings.save_splitter(self.splitBott)

    def on_heading_selection_changed(self, head_code):
        self.sigHeadingSelected.emit(head_code)
        self.agsAbbrevsWidget.set_heading(head_code)

    def select_heading(self, head_code):
        self.agsHeadingsTable.select_heading(head_code)
    #
    #
    # def clear(self):
    #     am_i_called___()
    #     self.lblGroupCode.setText("")
    #     self.lblDescription.setText("")
    #     self.agsGroupNotesTable.clear()
    #     self.agsAbbrevsWidget.clear()

    def clear_parent_child_buttons(self):

        for butt in self.buttGrpTB.buttons():
            butt.setIcon(Ico.icon(Ico.BulletBlack))
            butt.setText("")
            butt.setDisabled(True)

    def set_group(self, grp):

        ## load subwidgets, even if grp==None
        self.agsHeadingsTable.set_group(grp)
        self.agsGroupNotesWidget.set_group(grp)
        self.agsAbbrevsWidget.set_heading(None)

        self.clear_parent_child_buttons()
        self.lblGroupRequired.setVisible(False)

        if grp == None:
            self.group_code = None
            self.lblGroupCode.setText("")
            self.lblDescription.setText("")
            return

        self.group_code = grp['group_code']
        self.lblGroupCode.setText(grp['group_code'])
        self.lblDescription.setText(grp['group_description'])


        self.lblGroupRequired.setVisible( grp['group_required'] if grp['group_required'] else False )


        if grp['parent']:
            self.buttParent.setIcon(Ico.icon(Ico.AgsGroup))
            self.buttParent.setText(grp['parent'])
            self.buttParent.setDisabled(False)


        if grp['children']:
            for idx, kid in enumerate(grp['children']):
                butt = self. buttGrpTB.button(idx)
                butt.setIcon(Ico.icon(Ico.AgsGroup))
                butt.setText(kid)
                butt.setDisabled(False)

class AGS4GroupViewDialog(QtWidgets.QDialog):


    def __init__(self, parent=None, group_code=None, head_code=None):
        QtWidgets.QDialog.__init__(self, parent)

        self.setWindowTitle(group_code)
        self.setWindowIcon(Ico.icon(Ico.Ags4))

        self.setMinimumWidth(1100)
        self.setMinimumHeight(500)


        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setSpacing(0)
        margarine = 0
        self.mainLayout.setContentsMargins(margarine, margarine, margarine, margarine)
        self.setLayout(self.mainLayout)



        self.groupViewWidget = AGS4GroupViewWidget(self)
        self.mainLayout.addWidget(self.groupViewWidget)

        grp = ags4.DD.group(group_code)
        self.groupViewWidget.set_group(grp)
        if head_code:
            self.groupViewWidget.select_heading(head_code)



class AGS4HeadingsTable( QtWidgets.QWidget ):

    sigHeadingSelected = pyqtSignal(object)

    def __init__( self, parent ):
        QtWidgets.QWidget.__init__( self, parent )

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.mainLayout)


        ##===============================================================
        self.tree = QtWidgets.QTreeView(self)
        self.mainLayout.addWidget(self.tree)
        self.tree.setUniformRowHeights(True)
        self.tree.setRootIsDecorated(False)
        self.tree.setAlternatingRowColors(True)

        self.model = HeadingsModel(self)
        self.tree.setModel(self.model)

        CH = HeadingsModel.CH
        self.tree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        self.tree.setColumnWidth(CH.strip, 5)

        self.tree.setColumnWidth(CH.head_code, 100)
        self.tree.setColumnWidth(CH.description, 250)
        self.tree.setColumnWidth(CH.unit, 50)
        self.tree.setColumnWidth(CH.key, 30)
        self.tree.setColumnWidth(CH.required, 30)
        self.tree.setColumnWidth(CH.data_type, 60)
        self.tree.setColumnWidth(CH.sort_order, 20)
        self.tree.header().setStretchLastSection(True)

        self.tree.setSortingEnabled(False)

        self.tree.setContextMenuPolicy( Qt.CustomContextMenu )
        self.tree.customContextMenuRequested.connect(self.on_tree_context_menu )
        self.tree.selectionModel().selectionChanged.connect(self.on_tree_selected)
        self.tree.doubleClicked.connect(self.on_tree_double_clicked)

        self.popMenu = QtWidgets.QMenu()
        self.actOpenGroup = self.popMenu.addAction(Ico.icon(Ico.AgsGroup), "CODEEEEE", self.on_act_open_group)

    def on_tree_context_menu(self, qPoint):
        idx = self.tree.indexAt(qPoint)

        rec = self.model.rec_from_midx(idx)
        gc = rec['head_code'].split("_")[0]
        self.actOpenGroup.setDisabled(gc == self.model.grpDD['group_code'])
        self.actOpenGroup.setText("Open: %s" % gc)
        self.popMenu.exec_(self.tree.mapToGlobal(qPoint))

    def on_act_open_group(self):
        selidx = self.tree.selectionModel().selectedIndexes()
        rec = self.model.rec_from_midx(selidx[0])
        hc = rec.get("head_code")
        gc = hc.split("_")[0]
        d = AGS4GroupViewDialog(self, group_code=gc, head_code=hc)
        d.exec_()


    def set_group(self, grp):
        self.model.set_group(grp)

    def on_tree_double_clicked(self):
        pass

    def on_tree_selected(self, sel, desel):

        if not self.tree.selectionModel().hasSelection():
             self.sigHeadingSelected.emit( None )
             return

        rec = self.model.rec_from_midx( sel.indexes()[0] )
        self.sigHeadingSelected.emit(rec)


    def select_heading(self, head_code):

        midx = self.model.get_heading_index(head_code)
        if midx != None:
            self.tree.selectionModel().setCurrentIndex(midx,
                                                   QtWidgets.QItemSelectionModel.SelectCurrent|QtWidgets.QItemSelectionModel.Rows)


class AGS4GroupNotesWidget( QtWidgets.QWidget ):

    sigWordClicked = pyqtSignal(str)

    def __init__( self, parent=None ):
        QtWidgets.QWidget.__init__( self, parent )


        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.mainLayout)


        ##==============================
        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        self.mainLayout.addWidget(scrollArea, 100)

        self.scrollWidget = QtWidgets.QWidget()
        scrollArea.setWidget(self.scrollWidget)

        self.scrollLayout = QtWidgets.QVBoxLayout()
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollLayout.setSpacing(0)
        self.scrollWidget.setLayout(self.scrollLayout)



    def clear(self):
        """Removes all entries"""

        ## pain.. all this shite just to nuke a list
        self.setUpdatesEnabled(False)
        while self.scrollLayout.count() > 0:
            vari = self.scrollLayout.itemAt(0)
            w = vari.widget()
            if w:
                self.scrollLayout.removeWidget( w )
                w.setParent(None)
                w = None
            else:
                self.scrollLayout.removeItem( vari )

        self.setUpdatesEnabled(True)
        self.update()

    def set_group(self, grp):

        self.clear()
        if grp == None:
            return

        notes = grp.get("notes")
        if notes == None:
            return

        self.setUpdatesEnabled(False)
        lookup = ags4.DD.words

        for note in notes:

            w = widget = QtWidgets.QLabel()

            words = note.split(" ")
            res = []
            for word in words:
                if word in lookup:
                    res.append("<a href='#%s-%s'>%s</a>" % (lookup[word]['type'], word, word))
                else:
                    res.append(word)

            widget.setText(" ".join(res))
            widget.setTextFormat(QtCore.Qt.RichText)
            widget.setWordWrap(True)
            widget.setMargin(0)
            sty = "background-color: #EEF1F8; padding: 2px; margin:0; border-bottom:1px solid #dddddd;"
            widget.setStyleSheet(sty)
            widget.setAlignment(QtCore.Qt.AlignTop)

            self.scrollLayout.addWidget(w, 0)

            widget.linkActivated.connect(self.on_link_activated)


        self.scrollLayout.addStretch(10)
        self.setUpdatesEnabled(True)


    def on_link_activated(self, lnkq):
        lnk = str(lnkq)
        parts = lnk[1:].split("-", 1 )
        self.sigWordClicked.emit( parts[1] )



class AGS4AbbrevsWidget( QtWidgets.QWidget ):
    """Shows pickist and abbrevs etc"""

    def __init__( self, parent=None):
        QtWidgets.QWidget.__init__( self, parent )


        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.mainLayout)


        self.toolbar = xwidgets.hlayout()
        self.mainLayout.addLayout(self.toolbar, 0)

        self.icoLabel = xwidgets.IconLabel(self, ico=Ico.AgsGroup)
        self.icoLabel.setStyleSheet("background-color: white; color: #444444;")
        self.toolbar.addWidget(self.icoLabel, 0)

        self.lblAbbrCode = QtWidgets.QLabel(" ")
        self.lblAbbrCode.setStyleSheet("background-color: white; color: %s; font-weight: bold; font-family: monospace; padding: 3px;" % AGS4_COLORS.group)
        self.toolbar.addWidget(self.lblAbbrCode, 20)


        ##=== Tree
        self.tree = QtWidgets.QTreeView()
        self.mainLayout.addWidget(self.tree)
        self.tree.setUniformRowHeights(True)
        self.tree.setRootIsDecorated(False)
        self.tree.setAlternatingRowColors(True)
        self.tree.setSortingEnabled(False)

        self.model = AbbrevItemsModel(self)
        self.tree.setModel(self.model)

        CA = AbbrevItemsModel.CA

        self.tree.setColumnWidth(CA.code, 80)
        self.tree.setColumnWidth(CA.list, 50)

        self.tree.setColumnHidden(CA.check, True)

        self.tree.header().setStretchLastSection(True)

        # TODO fix sort to ags
        self.tree.setSortingEnabled(True)

        self.set_heading(None)


    def set_heading(self, heading):
        self.model.set_ags_heading(heading)
        s = ""
        if heading and heading["data_type"] == "PA":
            s = "%s" % (heading['head_description'])
        self.lblAbbrCode.setText(s)



class DecimalEditDelegate(QtWidgets.QItemDelegate):
    """Number editor to n decimal places"""
    def __init__(self, parent, heading):
        QtWidgets.QItemDelegate.__init__(self, parent)

        self.ogtHeading = heading

        ##self.data_type = heading['type']
        #self.data_type = heading['type']
        self.dp = None
        if self.ogtHeading.data_type.endswith("DP"):
            self.dp = int(self.ogtHeading.data_type[:-2])

    def createEditor(self, parent, option, index):

        editor = QtWidgets.QLineEdit(parent)
        if self.ogtHeading.type.endswith("DP"):
            validator = QtWidgets.QDoubleValidator()
            validator.setDecimals(self.dp)
            editor.setValidator(validator)

        return editor

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        curr = index.model().data(index) #.toString()
        editor.setText(curr)
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        no = float(editor.text())
        f = "%01."
        f += "%sf" % self.dp
        txt = f % (no,)
        model.setData(index, txt)

class IDComboDelegate(QtWidgets.QItemDelegate):
    """A combobox for the ID"""
    def __init__(self, parent, heading, options):
        QtWidgets.QItemDelegate.__init__(self, parent)

        self.ogtHeading = heading
        self.options = options

    def createEditor(self, parent, option, index):

        editor = QtWidgets.QComboBox(parent)
        editor.addItem("--unknown--", "")

        # populate combobox from abbreviations
        for v in self.options:
            editor.addItem( "%s" % v, "%s" % v)

        return editor

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        curr = index.model().data(index).toString()
        idx = editor.findData(curr)
        if idx != -1:
            editor.setCurrentIndex(idx)
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        txt = editor.itemData(editor.currentIndex()).toString()
        model.setData(index, txt)

class AGS4UnitsTypesWidget( QtWidgets.QWidget ):
    """The Units and Types tab"""

    def __init__( self, parent=None):
        QtWidgets.QWidget.__init__( self, parent )

        self.debug = False
        self.setObjectName("AGS4UnitTypesWidget")


        self.proxyUnits = QtCore.QSortFilterProxyModel()
        self.proxyUnits.setSourceModel(AgsData.modelUnits)
        self.proxyUnits.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.proxyUnits.setSortCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self.proxyTypes = QtCore.QSortFilterProxyModel()
        self.proxyTypes.setSourceModel(AgsData.modelDataTypes)
        self.proxyTypes.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.proxyTypes.setSortCaseSensitivity(QtCore.Qt.CaseInsensitive)

        ##===============================================
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.mainLayout)

        self.splitter = QtWidgets.QSplitter()
        self.mainLayout.addWidget(self.splitter)

        self.treeUnits = self.make_tree(self.proxyUnits, "Unit", "Description")
        self.splitter.addWidget(self.treeUnits)

        self.treeTypes = self.make_tree(self.proxyTypes, "Type", "Description")
        self.splitter.addWidget(self.treeTypes)


    def make_tree(self, model, tit1, tit2):
        tree = QtWidgets.QTreeView()
        tree.setRootIsDecorated(False)
        tree.setSortingEnabled(True)
        tree.setModel(model)
        return tree
        hi = tree.headerItem()
        hi.setText(0, tit1)
        hi.setText(1, tit2)
        return tree
