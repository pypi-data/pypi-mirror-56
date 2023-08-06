# -*- coding: utf-8 -*-

import os
import sys

from ogt import ags4

from Qt import Qt, QtGui, QtCore, QtWidgets

import app_globals as G
from settings import Settings

import ags4_widgets
import ags4_models
import www_client
import ogtgui_widgets
import ogtgui_project
import ogtgui_projects
import ogtgui_excel

from img import Ico
import xwidgets

APP_TITLE = "ogt-py"


class MainWindow(QtWidgets.QMainWindow):

    def on_after(self):
        """This is called after __init__, a few moment later"""

        # self.on_browse_ags4()


        if G.args.dev:
            # fn = "/home/ogt/AGS4-example-wrd.ags"
            # fn = "/home/ogt/ags-play/example_files/pete_stuff/simple.ags"
            # fn = "/home/geo2lab/z_drive/jobs/40101-40200/40153/AGS/PT 1.ags"
            fn = "/home/ogt/ags-play/example_files/pete_stuff/example_schedule.ags"
            #fn = "/home/ogt/ogt-py/etc/simple.ags"
            #self.load_ags4_file(fn)
            pass

    def on_open_excel(self):

        filePath, _filter = QtWidgets.QFileDialog.getOpenFileName(self, "Select Excel", "", "Excel(*.xlsx)")
        if filePath:
            self.load_excel(filePath)

    def load_excel(self, file_path):

            w = ogtgui_excel.ExcelBrowserDialog(parent=self, file_path=file_path)
            w.setWindowState(Qt.WindowMaximized)
            w.exec_()


    def __init__( self, args ):
        super().__init__()

        # ===========================================
        # Bit hacky, but sticking stuff in Globals :ref:`app_globals`
        # and initialising stuff
        G.mainWindow = self
        G.args = args # command args

        #G.settings = settings.XSettings(self)

        self.server = www_client.ServerConnection( self )
        self.server.response.connect( self.on_www_request_finished )
        G.server = self.server

        G.ags = ags4_models.Ags4Object()


        ##===============================================
        # Main window stuff
        self.setObjectName("OGTMainWindow")
        QtWidgets.QApplication.setStyle( QtWidgets.QStyleFactory.create( 'Cleanlooks' ) )
        self.setWindowTitle("%s - %s" % (APP_TITLE,G.version))
        self.setWindowIcon(Ico.icon(Ico.FavIcon))


        ##=================================================
        ## Menus - or a welsh meniw ;-)

        #=======
        ## File
        self.menuFile = self.menuBar().addMenu("File")

        self.actionOpen = self.menuFile.addAction("Open Ags4 File", self.on_open_ags_file)
        self.actionRecent = self.menuFile.addAction("Recent")
        self.actionRecent.setMenu(QtWidgets.QMenu())
        self.actionRecent.menu().triggered.connect(self.on_open_recent)
        self.menuFile.addSeparator()
        self.actionOpenExcel = self.menuFile.addAction("Open Excel", self.on_open_excel)


        self.actionQuit = self.menuFile.addAction(Ico.icon(Ico.Quit), "Quit", self.on_quit)

        #=======
        ## Projects
        self.menuProjects = self.menuBar().addMenu("Projects")

        self.widgetProjects = QtWidgets.QWidgetAction(self.menuProjects)
        self.projectsWidget = ogtgui_projects.OgtProjectsWidget(self)
        self.widgetProjects.setDefaultWidget(self.projectsWidget)

        self.actionProjects = self.menuProjects.addAction(self.widgetProjects)

        self.actionNewProject = self.menuProjects.addAction(Ico.icon(Ico.Add), "New Project", self.on_new_project)
        self.menuProjects.addSeparator()

        #=======
        ## View
        self.menuViews = self.menuBar().addMenu("View")
        self.actionAgs4Browse = self.menuViews.addAction(Ico.icon(Ico.Ags4), "AGS4", self.on_browse_ags4)
        self.actionAgs4Browse.setCheckable(True)

        #=======
        ## Examples - its an example widget within
        self.menuExamples = self.menuBar().addMenu("Examples")

        self.widgetActionExamples = QtWidgets.QWidgetAction(self.menuExamples)
        self.examplesWidget = ogtgui_widgets.ExamplesWidget(self)
        self.examplesWidget.setMinimumHeight(600)
        self.widgetActionExamples.setDefaultWidget(self.examplesWidget)
        self.examplesWidget.sigFileSelected.connect(self.load_ags4_example)

        self.actionExamples = self.menuExamples.addAction(self.widgetActionExamples)

        # help meniw (meniw = woman in welsh, eg a cafe.. U want the menu?  no food first ;-))
        self.menuHelp = self.menuBar().addMenu("Help")

        self.menuHelp.addAction("ogt-py")

        ##===========================
        ## Top Bar
        self.toolBar = QtWidgets.QToolBar()
        self.toolBar.setContentsMargins(0, 0, 0, 0)
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolBar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.actionAgs4Browse)

        self.toolBar.addSeparator()

        ### add a Banner and logo
        logoWidget = QtWidgets.QWidget()
        lwLay = xwidgets.hlayout(margin=0)
        logoWidget.setLayout(lwLay)
        self.toolBar.addWidget(logoWidget)

        self.lblBanner = QtWidgets.QLabel()
        self.lblBanner.setText(APP_TITLE)
        self.lblBanner.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.lblBanner.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Minimum)

        final_color = "#9E5015"
        sty = "font-style:italic; font-weight: bold;  color: #dddddd; margin: 0; font-size: 12pt; font-family: arial;"
        sty += "padding: 2px;"
        if True:
            sty += "background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, "
            sty += "stop: 0 transparent "
            sty += ", stop: 0.1 #efefef "
            sty += "stop: 1 %s" % final_color
            sty += ");"
        self.lblBanner.setStyleSheet(sty)
        lwLay.addWidget(self.lblBanner)

        iconLabel = QtWidgets.QLabel()
        iconLabel.setStyleSheet("padding: 4px; background-color: %s" % final_color)
        icon = Ico.icon(Ico.FavIcon)
        iconLabel.setPixmap(icon.pixmap(QtCore.QSize( 25, 25 )))
        lwLay.addWidget(iconLabel)


        ##===============================================
        ## Central widget contains  tabBar and a stack
        centralWidget = QtWidgets.QWidget()
        centralLayout = QtWidgets.QVBoxLayout()
        centralLayout.setContentsMargins(0, 0, 0, 0)
        centralLayout.setSpacing(0)
        centralWidget.setLayout(centralLayout)
        self.setCentralWidget(centralWidget)

        tabContainer = xwidgets.hlayout()
        centralLayout.addLayout(tabContainer)

        self.tabBar = QtWidgets.QTabBar()
        self.tabBar.setMovable(False)
        self.tabBar.setTabsClosable(True)
        tabContainer.addWidget(self.tabBar)
        self.tabBar.currentChanged.connect(self.on_tab_changed)
        self.tabBar.tabCloseRequested.connect(self.on_tab_close_requested)
        tabContainer.addStretch(10)


        self.stackWidget = QtWidgets.QStackedWidget()
        centralLayout.addWidget(self.stackWidget)

        # create a progress dialog and hide
        self.progressDialog = None
        # self.progressDialog = QtWidgets.QProgressDialog(self)
        # self.progressDialog.setMinimumWidth(300)
        # self.progressDialog.setWindowIcon(Ico.icon(Ico.Busy))
        # self.progressDialog.setRange(0, 0)
        # self.progressDialog.setCancelButton(None)
        # self.progressDialog.setModal(True)
        # self.progressDialog.hide()

        #=========================================
        # Seutp basic window dims, and restore
        self.setMinimumWidth(800)
        self.setMinimumHeight(800)
        Settings.restore_window( self )
        self.load_recent()

        ## run some stuff a few moments after window shown
        QtCore.QTimer.singleShot(200, self.on_after)

    def show_progress(self):
        self.progressDialog = QtWidgets.QProgressDialog(self)
        self.progressDialog.setMinimumWidth(300)
        self.progressDialog.setWindowIcon(Ico.icon(Ico.Busy))
        self.progressDialog.setRange(0, 0)
        self.progressDialog.setCancelButton(None)
        self.progressDialog.setModal(True)
        self.progressDialog.show()

    def hide_progress(self):
        todo()

    def add_widget(self, widget, label, ico=None):

        idx = self.tabBar.addTab(label)
        self.stackWidget.addWidget(widget)
        self.tabBar.setTabIcon(idx, Ico.icon(ico))

        self.tabBar.setCurrentIndex(self.tabBar.count() - 1)
        self.stackWidget.setCurrentIndex(self.stackWidget.count() - 1)

        widget.init_load()

    def on_www_request_finished(self, xreply):

        ## we loop though all the widgets and load_reply
        ## More than one widget may be interested in data
        for i in range(0, self.stackWidget.count()):
            self.stackWidget.widget(i).load_reply(xreply)

    def closeEvent( self, event ):
        Settings.save_window( self )

    def on_quit(self):
        ret = QtWidgets.QMessageBox.warning( self, "Desktop", "Sure you want to Quit ?", QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes )
        if ret == QtWidgets.QMessageBox.Yes:
            G.settings.save_window(  self )
            sys.exit( 0 )

    def on_show_examples(self):
        chk = self.buttExamples.isChecked()
        self.dockExamples.setVisible(chk)

    def load_ags4_example(self, file_name):

        self.menuExamples.close()

        data, err = ags4.example(file_name)
        if err:
            pass

        proj = ogtgui_project.OGTProjectWidget()
        proj.ogtDoc.add_ags4_string(data['contents'], file_name)

        self.add_widget(proj, file_name, ico=Ico.Project)



    def on_new_project(self):

        projWidget = ogtgui_project.OGTProjectWidget()
        self.add_widget(projWidget, "New Project", ico=Ico.Project)

    def load_ags4_file(self, file_path):

        if xwidgets.file_exists_check(self, file_path) == False:
            return

        # first check its not open
        for idx in range(0, self.stackWidget.count()):
            continue
            if isinstance(self.stackWidget.widget(idx), ogtgui_project.OGTProjectWidget):

                if self.stackWidget.widget(idx).ogtDoc.source_file_path == file_path:
                    self.tabBar.setCurrentIndex(idx)
                    return

        if False:
            self.progressDialog.setWindowTitle("Loading...")
            self.progressDialog.setLabelText(file_path)
            self.progressDialog.show()

            self.add_history(file_path)

        ## ======================
        proj = ogtgui_project.OGTProjectWidget()

        self.add_widget(proj, os.path.basename(file_path), ico=Ico.Project)

        proj.add_ags4_file(file_path)

        if False:
            self.progressDialog.hide()

    def add_history(self, file_path):
        history = G.settings.get_list("history")

        if file_path in history:
            # remove if in history, so insert at top
            history.remove(file_path)
        history.insert(0, file_path)
        if len(history) > 20:
            history = history[0:20]
        Settings.save_list("history", history)
        self.load_recent()

    def load_recent(self):
        files = Settings.get_list("history")
        menu = self.actionRecent.menu()
        menu.clear()
        for f in files:
            menu.addAction(f)

    def on_open_recent(self, act):
        fn =  str(act.text())
        self.load_ags4_file(fn)

    def on_tab_changed(self, idx):
        self.stackWidget.setCurrentIndex(idx)

    def set_action_checked(self, act, state):
        act.blockSignals(True)
        act.setChecked(state)
        act.blockSignals(False)

    def on_tab_close_requested(self, idx):

        widget = self.stackWidget.widget(idx)

        if isinstance(widget, ags4_widgets.AGS4DataDictBrowser):
            self.set_action_checked(self.actionAgs4Browse, False)

        self.tabBar.removeTab(idx)
        self.stackWidget.removeWidget( widget )

    def on_browse_ags4(self):
        """Opens or switches to the :ref:`ags4_data_dict`"""

        ## Check it not already there
        for idx in range(0, self.stackWidget.count()):
            if isinstance(self.stackWidget.widget(idx), ags4_widgets.AGS4DataDictBrowser):
                ## its there so switch to
                self.stackWidget.setCurrentIndex(idx)
                self.tabBar.setCurrentIndex(idx)
                self.set_action_checked(self.actionAgs4Browse, True)
                return

        # create new instance
        browseWidget = ags4_widgets.AGS4DataDictBrowser()
        self.add_widget(browseWidget, "AGS4 Data Dict", ico=Ico.Ags4)
        ## set the menu/tbar actions checked
        self.set_action_checked(self.actionAgs4Browse, True)



    def on_open_ags_file(self):

        dial = QtWidgets.QFileDialog(self, "Select AGS File")
        dial.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        #dial.setFilter(QtCore.QDir.Files)
        dial.setNameFilters(["Ags Files (*.ags *.ags4)"])

        if dial.exec_():
            fn = str(dial.selectedFiles()[0])
            self.load_ags4_file(fn)



    @staticmethod
    def show_splash():

        splashImage = QtGui.QPixmap( "../images/splash.png" )
        splashScreen = QtWidgets.QSplashScreen( splashImage )
        splashScreen.showMessage( "  Loading . . ." )
        splashScreen.show()
        return splashScreen
