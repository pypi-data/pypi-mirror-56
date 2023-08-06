# -*- coding: utf-8 -*-


from Qt import QtGui, QtWidgets, QtCore, Qt, pyqtSignal
from ogt import CELL_COLORS
import app_globals as G

import ogtgui_group
import ogtgui_widgets
import ags4_widgets
import xwidgets
from img import Ico


class OGTDocumentWidget( QtWidgets.QWidget ):

    sigUpdatedXX = pyqtSignal(object)
    #sigChanged = pyqtSignal()


    def __init__( self, parent=None, ogtDoc=None):
        QtWidgets.QWidget.__init__( self, parent )

        self.ogtDoc = ogtDoc

        self.show_data_count = False
        self.show_description = False
        self._tab_widgets = [] # dodgy

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.mainLayout)

        self.headerWidget = ogtgui_widgets.HeaderBarWidget(title="Groups", bg="#88EEFF")
        self.mainLayout.addWidget(self.headerWidget, 0)

        # == View Mode
        self.tbgView = xwidgets.ToolBarGroup(title="Groups Sort",
                                             is_group=True, toggle_icons=True,
                                             toggle_callback=self.on_butt_sort)
        self.headerWidget.addWidget(self.tbgView)

        for idx, optt in enumerate([[self.ogtDoc.SORT.recommended, "Recommended"],
                                    [self.ogtDoc.SORT.a2z, "Alphabetic"],
                                    [self.ogtDoc.SORT.source, "Sources"]]):
            #buttSort = xwidgets.XToolButton(text=optt[1], checkable=True, checked=idx == 0)

            self.tbgView.addButton(text=optt[1], idx=optt[0], checkable=True, checked=idx == 0)

        self.chkShowDescription = QtWidgets.QCheckBox()
        self.chkShowDescription.setText("Show Description")
        self.chkShowDescription.setChecked(True)
        self.headerWidget.addWidget(self.chkShowDescription)
        self.chkShowDescription.toggled.connect(self.set_show_description)


        ##== Scroll aread
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFixedHeight(70)
        self.mainLayout.addWidget(self.scrollArea, 0)

        self.scrollWidget = QtWidgets.QWidget()
        #self.scrollWidget.setFixedHeight(80)
        self.scrollArea.setWidget(self.scrollWidget)

        self.scrollLayout = QtWidgets.QHBoxLayout()
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollLayout.setSpacing(0)
        self.scrollWidget.setLayout(self.scrollLayout)
        self.scrollLayout.addStretch(100)

        self.stackWidget = QtWidgets.QStackedWidget()
        self.mainLayout.addWidget(self.stackWidget)

        self.scrollArea.horizontalScrollBar().rangeChanged.connect(self.on_detect_scroll)


    def init_load(self):
        pass


    def do_update(self):

        for grpOb in self.ogtDoc.groups_list:
            widget = self.add_set_group( grpOb )


        for idx in range(0, self.stackWidget.count()):
            self.stackWidget.widget(idx).do_update()

        self.update_group_tabs()
        print("so_iupdate", self)


        self.on_detect_scroll()

        cidx = self.stackWidget.currentIndex()
        if cidx == -1:
            return
        gc = self.stackWidget.currentWidget().ogtGroup.group_code
        self.select_group(gc)

        #if G.args.dev:
        #    self.select_group("LOCA")



    def on_butt_sort(self, sort_id):
        self.ogtDoc.set_sort_mode(sort_id)
        print("on_butt_sort", sort_id, self)
        self.do_update()

    def on_detect_scroll(self):
        viz = self.scrollArea.horizontalScrollBar().isVisible()
        self.scrollArea.setFixedHeight(90 if viz else 70)
        # self.scrollWidget.update()

    def set_show_description(self, xstate=None):
        state = self.chkShowDescription.isChecked()
        for idx in range(0, self.stackWidget.count()):
            self.stackWidget.widget(idx).set_show_description(state)

    def add_set_group(self, ogtGroup):

        # first check this not already there
        for idx in range(0, self.stackWidget.count()):
            if self.stackWidget.widget(idx).ogtGroup.group_code == ogtGroup.group_code:
                return self.stackWidget.widget(idx)


        grpViewWidget = ogtgui_group.GroupViewWidget(ogtGroup=ogtGroup)
        grpViewWidget.do_update()
        idx = self.stackWidget.addWidget(grpViewWidget)

        grpViewWidget.sigGoto.connect(self.on_goto)
        #self.ogtDoc.sigChanged.connect(self.on_changed)
        #grpViewWidget.sigChanged.connect(self.on_changed)

        return grpViewWidget

    def update_group_tabs(self):


        curr_grp_code = None
        if self.stackWidget.currentWidget():
            curr_grp_code = self.stackWidget.currentWidget().ogtGroup.group_code



        ## nuke existsing buttons
        while self.scrollLayout.count() > 0:
            w = self.scrollLayout.takeAt(0)
            w = None


        self._tab_widgets = []

        for idx, ogtGroup in enumerate(self.ogtDoc.groups_list):

            gWid = XTabWidget(ogtGroup)
            gWid.setFixedWidth(55)
            self.scrollLayout.addWidget(gWid)
            self._tab_widgets.append(gWid)
            gWid.sigSelected.connect(self.on_grp_tab_clicked)

        self.scrollLayout.addStretch(10)

        self.select_group(curr_grp_code)


    #
    # def on_changed_DEAD(self):
    #     print("on_changed", self)
    #     self.sigChanged.emit()


    def select_group(self, group_code):

        if self.stackWidget.currentWidget():
            if group_code != self.stackWidget.currentWidget().ogtGroup.group_code:
                for i in range(0, self.stackWidget.count()):
                    if self.stackWidget.widget(i).ogtGroup.group_code == group_code:
                        self.stackWidget.setCurrentIndex(i)
                        break

        for tw in self._tab_widgets:
            tw.set_selected(tw.ogtGroup.group_code == group_code)





    def on_goto(self, xcode):
        if "_" in xcode:
            grp_code = xcode.split("_")[0]
        else:
            grp_code = xcode
        self.select_group(grp_code)


    def on_grp_tab_clicked(self, grp_code):
        self.select_group(grp_code)



class XTabWidget(QtWidgets.QWidget):

    sigSelected = pyqtSignal(str)

    def __init__(self, ogtGroup):
        QtWidgets.QWidget.__init__(self)

        self.ogtGroup = ogtGroup

        self.selected = False

        self.W = 2

        m = 0
        lay = QtWidgets.QVBoxLayout()
        lay.setContentsMargins(m,m,m,m)
        lay.setSpacing(0)
        self.setLayout(lay)

        ## Coloured red when required
        self.lblBarTop = QtWidgets.QLabel()
        self.lblBarTop.setFixedHeight(4)
        lay.addWidget(self.lblBarTop)

        ## Group code label
        self.lblGroupCode = xwidgets.XLabel(bold=True)
        self.lblGroupCode.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.lblGroupCode)
        self.lblGroupCode.sigClicked.connect(self.on_lbl_clicked)

        # Errors Count label
        self.lblErrorCount = xwidgets.XLabel()
        self.lblErrorCount.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.lblErrorCount)
        self.lblErrorCount.sigClicked.connect(self.on_lbl_clicked)

        # data count label
        self.lblDataRowsCount = xwidgets.XLabel()
        self.lblDataRowsCount.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.lblDataRowsCount)
        self.lblDataRowsCount.sigClicked.connect(self.on_lbl_clicked)


        self.lblBarB = xwidgets.XLabel()
        self.lblBarB.setFixedHeight(self.W)
        lay.addWidget(self.lblBarB, 3)
        self.lblBarB.sigClicked.connect(self.on_lbl_clicked)


        self.up_widgets()
        
    def on_lbl_clicked(self):
        self.sigSelected.emit(self.ogtGroup.group_code)

    def set_selected(self, state):
        self.selected = state
        self.up_widgets()

    def up_widgets(self):

        self.lblGroupCode.setText(self.ogtGroup.group_code)
        self.lblDataRowsCount.setText("%s" % self.ogtGroup.data_rows_count)
        self.lblErrorCount.setText("%s" % self.ogtGroup.errors_warnings_count if self.ogtGroup.errors_warnings_count else "-")

        self._up_style()

    def _up_style(self):

        bg = "#444444" if self.selected else "#999999"
        px = 2
        borders =  "border-left: %spx solid %s; " % (px, bg)
        borders += "border-right: %spx solid %s; " % (px, bg)


        #= Top bar is special if group is required
        if self.ogtGroup.group_required:
            col = "#990000" #required color always red
        else:
            col = bg
        s = "background-color: %s;" % (col)
        self.lblBarTop.setStyleSheet(s)

        #= group lbl color
        fg = "#dddddd" if self.selected else "#444444"
        gbg = "#555555" if self.selected else bg
        s = "background-color: %s;" % gbg
        s += "color: %s;" % fg
        s += borders
        self.lblGroupCode.setStyleSheet(s)

        #= Errors count
        c = "transparent" if self.ogtGroup.errors_warnings_count == 0 else CELL_COLORS.err_bg
        s = "background-color: %s;" % c
        s += borders
        self.lblErrorCount.setStyleSheet(s)

        s = "background-color: #E8E8E8;"
        s += borders
        self.lblDataRowsCount.setStyleSheet(s)


        ##  bottom
        s = "background-color: %s;" % bg
        self.lblBarB.setStyleSheet(s)


    def on_ags_info(self):
        ags4_widgets.show_group_dialog(self, group_code=self.ogtGroup.group_code)



