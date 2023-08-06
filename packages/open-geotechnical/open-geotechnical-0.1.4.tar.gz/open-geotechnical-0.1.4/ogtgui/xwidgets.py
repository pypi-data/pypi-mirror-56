# -*- coding: utf-8 -*-
"""
@author: Peter Morgan <pete@daffodil.uk.com>
"""
import os
from Qt import Qt, QtCore, QtGui, QtWidgets, pyqtSignal

from img import Ico

DEFAULT_SPACING = 0
DEFAULT_MARGIN = 0
DEFAULT_BUTTON_WIDTH = 80

#=====================================================
# Layouts

def hlayout(spacing=DEFAULT_SPACING, margin=DEFAULT_MARGIN):
    """Convenience function to create a QHBoxLayout"""
    lay = QtWidgets.QHBoxLayout()
    if isinstance(margin, bool):
        margin = DEFAULT_SPACING
    if isinstance(spacing, bool):
        spacing = DEFAULT_SPACING
    lay.setContentsMargins(margin, margin, margin, margin)
    lay.setSpacing(spacing)
    return lay

def vlayout(spacing=DEFAULT_SPACING, margin=DEFAULT_MARGIN):
    """Convenience function to create a QVBoxLayout"""
    lay = QtWidgets.QVBoxLayout()
    if isinstance(margin, bool):
        margin = DEFAULT_SPACING
    if isinstance(spacing, bool):
        spacing = DEFAULT_SPACING
    lay.setContentsMargins(margin, margin, margin, margin)
    lay.setSpacing(spacing)
    return lay


def file_exists_check(parent, file_path):
    if not os.path.exists(file_path):
        mess = QtWidgets.QMessageBox
        mess.critical(parent, "File not exist", file_path)
        return False
    return True

class XLabel(QtWidgets.QLabel):

    sigClicked = pyqtSignal()

    def __init__( self, parent=None, style=None,  align=None,
                 text=None,  tooltip=None, bold=False, width=None):
        QtWidgets.QLabel.__init__( self, parent )

        self.set_bold(bold)

        if text:
            self.setText(text)

        if tooltip:
            self.setToolTip(tooltip)

        if align != None:
            self.setAlignment(align)

        if style:
            self.setStyleSheet(style)

        if width != None:
            self.setFixedWidth(width)

    def set_bold(self, state):
        f = self.font()
        f.setBold(state)
        self.setFont(f)

    def mousePressEvent(self, ev):
        self.sigClicked.emit()
        QtWidgets.QLabel.mousePressEvent(self, ev)


class XToolButton(QtWidgets.QToolButton):
    def __init__( self, parent=None, both=True,  ico=None,
                  popup=False, autoRaise=True, menu=False, disabled=False,
                text=None,  tooltip=None, bold=False,
                  callback=None, toggledCallback=None,
                  checkable=None, checked=None,
                width=None):
        QtWidgets.QToolButton.__init__( self, parent )


        self.setAutoRaise(autoRaise)


        self.setDisabled(disabled)

        if width:
            self.setFixedWidth(width)

        if both:
            self.setToolButtonStyle( Qt.ToolButtonTextBesideIcon)
        else:
            self.setToolButtonStyle( Qt.ToolButtonIconOnly)

        if checkable != None:
            self.setCheckable(checkable)
        if checked != None:
            self.setChecked(checked)

        if callback:
            self.clicked.connect(callback)
        if toggledCallback:
            self.toggled.connect(toggledCallback)

        if tooltip:
            self.setToolTip(tooltip)

        if text:
            self.setText(text)

        if bold:
            self.setBold(True)

        if ico:
            self.setIco(ico)

        if popup:
            self.setPopupMode(QtWidgets.QToolButton.InstantPopup)

        if menu:
            self.setMenu(QtWidgets.QMenu())

    def setIco(self, ico):
        self.setIcon(Ico.icon(ico))

    def setBold(self, state=True):

        f = self.font()
        f.setBold(True)
        self.setFont(f)

    def set_bg(self, color):
        self.setStyleSheet("background-color: %s" % color)



class XPushButton(QtWidgets.QPushButton):
    def __init__( self, parent=None,  ico=None,
                 disabled=False,
                text=None,  tooltip=None, bold=False,
                  callback=None,       width=None):
        QtWidgets.QPushButton.__init__( self, parent )


        self.setDisabled(disabled)

        if width:
            self.setFixedWidth(width)



        if callback:
            self.clicked.connect(callback)

        if tooltip:
            self.setToolTip(tooltip)

        if text:
            self.setText(text)

        if bold:
            self.setBold(True)

        if ico:
            self.set_ico(ico)

    def set_ico(self, ico):
        self.setIcon(Ico.icon(ico))

    def setBold(self, state=True):

        f = self.font()
        f.setBold(True)
        self.setFont(f)

    def set_bg(self, color):
        self.setStyleSheet("background-color: %s" % color)

class XTableWidgetItem(QtWidgets.QTableWidgetItem):
    """Extended QTableWidgetItem with convenience functions"""
    def __init__(self):
        QtWidgets.QTableWidgetItem.__init__(self)



    def set(self, text=None, bold=False, bg=None, fg=None, align=None, check=None):

        if text:
            self.setText(text)

        if bold:
            self.set_bold(True)

        if bg:
            self.set_bg(bg)
        if fg:
            self.set_bg(fg)

        if align:
            self.setTextAlignment(align)

        if check != None:
            self.setCheckState(check)


    def set_bold(self, state):
        f = self.font()
        f.setBold(state)
        self.setFont(f)

    def set_bg(self, bg_color):
        colo = QtWidgets.QColor()
        colo.setNamedColor(bg_color)
        self.setBackgroundColor(colo)

    def set_fg(self, bg_color):
        colo = QtWidgets.QColor()
        colo.setNamedColor(bg_color)
        self.setForeground(colo)


class XTreeWidgetItem(QtWidgets.QTreeWidgetItem):
    """Extended QTableWidgetItem with convenience functions"""
    def __init__(self):
        QtWidgets.QTreeWidgetItem.__init__(self)


    def set(self, cidx, text=None, bold=False, bg=None, fg=None, align=None, check=None, ico=None):

        if text:
            self.setText(cidx, str(text))

        if bold:
            self.set_bold(cidx, True)

        if bg:
            self.set_bg(cidx, bg)
        if fg:
            self.set_fg(cidx, fg)

        if align:
            self.setTextAlignment(cidx, align)

        if check != None:
            self.setCheckState(cidx, check)

        if ico:
            self.set_ico(cidx, ico)


    def set_bold(self, cidx, state):
        f = self.font(cidx)
        f.setBold(state)
        self.setFont(cidx, f)

    def set_bg(self,cidx,  bg_color):
        colo = QtWidgets.QColor()
        colo.setNamedColor(bg_color)
        self.setBackgroundColor(cidx, colo)

    def set_fg(self, cidx,  bg_color):
        colo = QtWidgets.QColor()
        colo.setNamedColor(bg_color)
        self.setForeground(cidx, colo)

    def set_ico(self, cidx, ico):
        self.setIcon(cidx, Ico.icon(ico))

    def i(self, cidx):
        try:
            return int(str(self.text(cidx)))
        except:
            return None

class GroupHBox(QtWidgets.QGroupBox):


    def __init__(self, parent=None):
        QtWidgets.QGroupBox.__init__(self, parent)


        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

    def setContentsMargins(self, a,b,c,d):
        self.layout.setContentsMargins(a,b,c,d)

    def addWidget(self, widget, stretch=0):
        self.layout.addWidget(widget, stretch)

    def addLayout(self, widget, stretch=0):
        self.layout.addLayout(widget, stretch)

    def addStretch(self, stretch):
        self.layout.addStretch(stretch)



class GroupVBox(QtWidgets.QGroupBox):

    def __init__(self, parent=None, bold=False):
        QtWidgets.QGroupBox.__init__(self, parent)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

    def setContentsMargins(self, a,b,c,d):
        self.layout.setContentsMargins(a,b,c,d)

    def addLabel(self, txt):
        lbl = QtWidgets.QLabel()
        lbl.setText(txt)
        lbl.setStyleSheet("font-family: monospace; font-size: 8pt; color: #666666; background-color: #efefef; padding: 3px;")
        self.layout.addWidget(lbl)


    def addWidget(self, widget, stretch=0):
        self.layout.addWidget(widget, stretch)

    def addLayout(self, widget, stretch=0):
        self.layout.addLayout(widget, stretch)

    def addSpacing(self, s):
        self.layout.addSpacing( s)

    def addStretch(self, stretch):
        self.layout.addStretch(stretch)


    def setSpacing(self, x):
        self.layout.setSpacing(x)

class GroupGridBox(QtWidgets.QGroupBox):


    def __init__(self, parent=None):
        QtWidgets.QGroupBox.__init__(self, parent)


        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)



class XStandardItem( QtGui.QStandardItem ):

    def __init__( self):
        QtGui.QStandardItem.__init__( self )
        #super(QtWidgets.QStandardItem, self).__init__()

        self.setEditable(False)

    def set_bg(self, color):
        self.setBackground(  G.colors.to_object( color ) )

    def set_fg(self, color):
        self.setForeground(  G.colors.to_object( color ) )

    def set_bold( self, bold):
        font = self.font()
        font.setBold( bold )
        self.setFont( font )

    def set_font_size( self, size):
        font = self.font()
        font.setPointSize(size)
        self.setFont( font )

    def setIco(self, ico):
        self.setIcon(Ico.icon(ico))

    def setText(self, txt, align=None, ico=None, icon=None, bold=False):
        self.set(txt, align=align, ico=ico, icon=icon, bold=bold)

    def set(self, txt, align=None, ico=None, icon=None, bold=False, font=None, bg=None):

        QtGui.QStandardItem.setText(self, str(txt))
        if align:
            self.setTextAlignment( align)
        if ico:
            self.setIco(ico)
        if icon:
            self.setIcon(icon)

        self.set_bold(bold)

        if font:
            self.set_font_family(font)
        if bg:
            self.set_bg(bg)

    def set_font_family( self, fam):
        font = self.font( )
        font.setFamily( fam )
        self.setFont( font )

    def s(self):
        return str(self.text())

    def i(self):
        x, ok = self.text().toInt()
        if not ok:
            return None
        return x


    def b(self):
        return  str(self.text()) == "1"

    def ds(self):
        return str(self.data().toString())

    def lbl_checked(self,  val, bg_color=None ):
        self.setTextAlignment( QtCore.Qt.AlignCenter)
        if bg_color == None:
            bg_color = "#FFECAA"
        if bool(val):
            self.setText( "Yes")
            self.setData("1")
            self.set_bg( bg_color )
        else:
            self.setText( "-")
            self.setData("")
            self.set_bg( "#efefef")

class ClearButton( QtWidgets.QToolButton ):
    def __init__( self, parent, callback=None ):
        QtWidgets.QToolButton.__init__( self )
        self.setIcon( Ico.icon( Ico.Clear ) )
        self.setToolTip("Clear")
        self.setToolButtonStyle( QtCore.Qt.ToolButtonIconOnly )
        self.setAutoRaise(True)
        self.setFixedWidth(16)

        if callback:
            self.clicked.connect(callback)

class CancelButton( QtWidgets.QPushButton ):
    def __init__( self, parent=None, callback=None ):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setIcon( Ico.icon( Ico.Cancel ) )
        self.setText("Cancel")
        if callback:
            self.clicked.connect(callback)
        else:
            self.clicked.connect(parent.on_reject)


class SaveButton(QtWidgets.QPushButton):
    def __init__(self, parent=None, callback=None, text="Save"):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setIcon(Ico.icon(Ico.Save))
        self.setText(text)
        if callback:
            self.clicked.connect(callback)
        else:
            self.clicked.connect(parent.on_accept)

class IconLabel(QtWidgets.QLabel):

    def __init__( self, parent=None, ico=None):
        QtWidgets.QLabel.__init__( self, parent)

        self.setContentsMargins(5,0,0,0)
        #img_file_path = G.settings.image_path( "/missc/arrow_left_down.gif" )
        icon = Ico.icon(ico)
        self.setPixmap( icon.pixmap(QtCore.QSize( 16, 16 )) )
        self.setFixedWidth(20)




class LNTextEdit(QtWidgets.QFrame):
    """Text widget with support for line numbers
    https://nachtimwald.com/2009/08/19/better-qplaintextedit-with-line-numbers/
    """
    class NumberBar(QtWidgets.QWidget):

        def __init__(self, edit):
            QtWidgets.QWidget.__init__(self, edit)

            self.edit = edit
            self.adjustWidth(1)

        def paintEvent(self, event):
            self.edit.numberbarPaint(self, event)
            QtWidgets.QWidget.paintEvent(self, event)

        def adjustWidth(self, count):
            width = self.fontMetrics().width(unicode(count))
            if self.width() != width:
                self.setFixedWidth(width)

        def updateContents(self, rect, scroll):
            if scroll:
                self.scroll(0, scroll)
            else:
                # It would be nice to do
                # self.update(0, rect.y(), self.width(), rect.height())
                # But we can't because it will not remove the bold on the
                # current line if word wrap is enabled and a new block is
                # selected.
                self.update()

class XPlainTextEdit(QtWidgets.QPlainTextEdit):

    def __init__(self, *args):
        QtWidgets.QPlainTextEdit.__init__(self, *args)

        # self.setFrameStyle(QFrame.NoFrame)

        self.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.highlight()
        # self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.setStyleSheet("font-family: monospace")

        self.cursorPositionChanged.connect(self.highlight)

    def highlight(self):
        hi_selection = QtWidgets.QTextEdit.ExtraSelection()

        hi_selection.format.setBackground(self.palette().alternateBase())
        hi_selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, QtCore.QVariant(True))
        hi_selection.cursor = self.textCursor()
        hi_selection.cursor.clearSelection()

        self.setExtraSelections([hi_selection])

    def numberbarPaint(self, number_bar, event):
        font_metrics = self.fontMetrics()
        current_line = self.document().findBlock(self.textCursor().position()).blockNumber() + 1

        block = self.firstVisibleBlock()
        line_count = block.blockNumber()
        painter = QtWidgets.QPainter(number_bar)
        painter.fillRect(event.rect(), self.palette().base())

        # Iterate over all visible text blocks in the document.
        while block.isValid():
            line_count += 1
            block_top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()

            # Check if the position of the block is out side of the visible
            # area.
            if not block.isVisible() or block_top >= event.rect().bottom():
                break

            # We want the line number for the selected line to be bold.
            if line_count == current_line:
                font = painter.font()
                font.setBold(True)
                painter.setFont(font)
            else:
                font = painter.font()
                font.setBold(False)
                painter.setFont(font)

            # Draw the line number right justified at the position of the line.
            paint_rect = QtCore.QRect(0, block_top, number_bar.width(), font_metrics.height())
            painter.drawText(paint_rect, Qt.AlignRight, unicode(line_count))

            block = block.next()

        painter.end()


class XLineEdit(QtWidgets.QLineEdit):

    def __init__(self, parent=None):
        QtWidgets.QLineEdit.__init__(self)

    def s(self):
        """return python string"""
        return str(self.text()).strip()

class ToolBarGroup(QtWidgets.QWidget):
    def __init__(self, parent=None, title=None, width=None, hide_labels=False, bg='#999999',
                 is_group=False, toggle_icons=False, toggle_callback=None):
        QtWidgets.QWidget.__init__(self, parent)

        if width:
            self.setFixedWidth(width)

        self.icon_on = Ico.FilterOn
        self.icon_off = Ico.FilterOff
        self.toggle_icons = toggle_icons
        self.toggle_callback = toggle_callback
        self.hide_labels = hide_labels

        self.buttonGroup = None
        self.is_group = is_group
        if self.is_group:
            self.buttonGroup = QtWidgets.QButtonGroup()
            self.buttonGroup.setExclusive(True)
            if self.toggle_callback:
                self.buttonGroup.buttonClicked.connect(self.on_button_clicked)

        self.group_var = None
        self.callback = None
        self.show_icons = True
        self.icon_size = 12
        self.bg_color = bg

        ## Main Layout
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        self.setLayout(mainLayout)

        ## Label
        self.label = QtWidgets.QLabel()
        #bg = "#8F8F8F"  ##eeeeee"
        fg = "#eeeeee"  ##333333"
        lbl_sty = "background: %s; " % self.bg_color  # qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #fefefe, stop: 1 #CECECE);"
        lbl_sty += " color: %s; font-size: 8pt; padding: 1px;" % fg  # border: 1px outset #cccccc;"
        self.label.setStyleSheet(lbl_sty)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setFixedHeight(20)
        mainLayout.addWidget(self.label)

        ## Toolbar
        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolbar.setFixedHeight(30)

        mainLayout.addWidget(self.toolbar)

        if title:
            self.set_title(title)

    def set_title(self, title):
        self.label.setText("%s" % title)

    def addWidget(self, widget):
        self.toolbar.addWidget(widget)
        return widget

    def addAction(self, act):
        self.toolbar.addAction(act)

    def addButton(self, ico=None, text=None, callback=None, idx=None, toggle_callback=None, tooltip=None,
                  ki=None, bold=False, checkable=False, checked=None, width=None, return_action=False):

        butt = XToolButton()

        if self.is_group:
            if idx != None:
                self.buttonGroup.addButton(butt, idx)
            else:
                self.buttonGroup.addButton(butt)
        if self.hide_labels == False:
            if text != None:
                butt.setText(text)
        if text == None:
            butt.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        else:
            butt.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        if tooltip:
            butt.setToolTip(tooltip)
        if self.toggle_icons:
            butt.setIconSize(QtCore.QSize(10, 10))
            butt.setIcon(Ico.icon(self.icon_off))
        if ico:
            butt.setIcon(Ico.icon(ico))
            butt.setIconSize(QtCore.QSize(10, 10))

        butt.setCheckable(checkable)
        if checked != None:
            butt.setChecked(checked)


        butt.setProperty("ki", ki)
        nuAct = self.toolbar.addWidget(butt)
        if callback:
            self.connect(butt, QtCore.SIGNAL("clicked()"), callback)
        #if toggle_callback:
        #   self.connect(butt, QtCore.SIGNAL("toggled(bool)"), toggle_callback)
        if bold:
            self.set_bold(butt)
        if width:
            butt.setFixedWidth(width)

        self.on_button_clicked(block=True)

        if return_action:
            return nuAct
        return butt

    def set_bold(self, w):
        f = w.font()
        f.setBold(True)
        w.setFont(f)

    def on_button_clicked(self, butt=None, block=False):
        if self.is_group:
            for b in self.buttonGroup.buttons():
                b.setIcon( Ico.icon(self.icon_on if b.isChecked() else self.icon_off) )

                if block == False and b.isChecked():
                    if self.toggle_callback:
                        self.toggle_callback(self.buttonGroup.id(b))

    def get_id(self):
        id = self.buttonGroup.checkedId()
        if id == -1:
            return None
        return id


class TopStatusBar(QtWidgets.QWidget):
    """A QWidget with many embedded widgets for StatusBar"""

    sigRefresh = pyqtSignal()

    def __init__(self, parent=None, refresh=True, statusLabel=False,
                 pager=False, modeLabel=True):
        QtWidgets.QWidget.__init__(self, parent)


        self.refresh = refresh
        self.includeStatusLabel = statusLabel

        self.mainLayout = QtWidgets.QHBoxLayout()
        m = 0
        self.mainLayout.setContentsMargins(m, m, m, m)
        self.setLayout(self.mainLayout)

        ##== Status Bar
        self.statusBar = QtWidgets.QStatusBar()
        self.statusBar.setSizeGripEnabled(False)
        self.showMessage(" ")
        self.mainLayout.addWidget(self.statusBar, 1)


        ##== Progress Bar
        progressWidget = QtWidgets.QWidget()
        progressWidget.setMinimumWidth(40)
        progressWidget.setMaximumWidth(200)
        self.mainLayout.addWidget(progressWidget)

        progressLayout = QtWidgets.QHBoxLayout()
        m = 0
        progressLayout.setContentsMargins(m, m, m, m)
        progressWidget.setLayout(progressLayout)

        self.progress = QtWidgets.QProgressBar(self)
        # self.progress.setFixedWidth( 40 )
        # self.progress.setFixedHeight( 10 )
        self.setContentsMargins(m, m, m, m)
        self.progress.setMinimum(0)
        self.progress.setMaximum(1)
        self.progress.setInvertedAppearance(False)
        self.progress.setTextVisible(False)
        self.progress.setVisible(False)
        # self.connect( self.progress, QtCore.SIGNAL('valueChanged(int)'), self.on_progress_value_changed)
        progressLayout.addWidget(self.progress, 1)

        ################################################################
        ### Status Label
        if self.includeStatusLabel:
            wid = 40
            self.lblStatus = QtWidgets.QLabel("Status:Label")
            self.lblStatus.setMinimumWidth(wid)
            self.lblStatus.setMaximumWidth(wid)
            self.lblStatus.setStyleSheet("font-size: 8pt")
            self.mainLayout.addWidget(self.lblStatus, 1)


        ################################################################
        ## Refrehsing Button
        """
        if self.refresh:
            self.buttRefresh = QtWidgets.QToolButton()
            self.mainLayout.addWidget(self.buttRefresh)

            self.buttRefresh.setIcon(Ico.icon(Ico.Refresh))
            # self.buttRefresh.setFlat(True)
            self.buttRefresh.setAutoRaise(True)
            self.buttRefresh.setIconSize(QtCore.QSize(16, 16))
            self.buttRefresh.setStyleSheet("padding: 0px;")
            self.connect(self.buttRefresh, QtCore.SIGNAL("clicked()"), self.on_refresh)
            if hasattr(parent, "on_refresh"):
                self.connect(self.buttRefresh, QtCore.SIGNAL("clicked()"), parent.on_refresh)

            # self.buttRefresh.setFixedWidth(40)

            self.popMenu = QtWidgets.QMenu()
            self.actionDebug = self.popMenu.addAction("Debug", self.on_server_debug_button)
            self.actionDebug.setIcon(dIco.icon(dIco.Dev))
            self.actionDebug.setIconVisibleInMenu(True)
            self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.connect(self, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.on_menu)
        else:
            self.popMenu = None
        """

    def showMessage( self, mess, timeout=None, warn=None, info=None ):
        if warn:
            self.statusBar.setStyleSheet("color: #990000;")
        elif info:
            self.statusBar.setStyleSheet("color: #3361C2;")
        else:
            self.statusBar.setStyleSheet("")

        if timeout == None:
            self.statusBar.showMessage( mess )
        else:
            self.statusBar.showMessage( mess, timeout )
