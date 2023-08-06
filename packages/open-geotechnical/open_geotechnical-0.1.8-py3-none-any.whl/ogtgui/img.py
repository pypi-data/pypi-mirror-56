# -*- coding: utf-8 -*-



import os

from Qt import QtGui, QtCore

from ogtgui import ICONS_PATH


class Ico(QtGui.QIcon):
    """Icons Definition and Loader

      - All icons used are listed as class constants.
      - Static methods create icons loaded from the file system

      .. todo:: try and intercept __getattr__ to return qIcon
    """

    def __init__(self, file_name=None):



        super().__init__(file_name)

    @staticmethod
    def get_icon_path(file_name):
        """
        Args:
            file_name (str): Icon filename
        Returns:
            str: Icons full path
        """
        return os.path.join(ICONS_PATH, file_name)

    @staticmethod
    def icon( file_name, pixmap=False, size=None):
        """Return a `QIcon`

        Args:
            file_name (str): Icon filename to load
            pixmap (bool): Return a pixmap instead of QIcon object
            size (int): Default size
        Returns:
            QIcon: new icon or pixmap
        """
        #print(Ico.get_icon_path(file_name))
        if file_name == None:
            qicon = QtGui.QIcon()
        else:
            qicon = QtGui.QIcon( Ico.get_icon_path(file_name) )

        if pixmap:
            return qicon.pixmap( QtCore.QSize( 16, 16 ) )

        if size:
            pass #icon2 = QtGui.QIcon( icon.pixmap( QtCore.QSize(size, size) ) )
            #return icon2

        return qicon

    Add = "add.png"

    Ags3 = "ags3.svg.png"
    Ags4 = "ags4.svg.png"

    AgsAbbrev = "font.png"
    AgsAbbrevItem = "textfield_rename.png"

    AgsField = "textfield.png"

    AgsGroup = "layout.png"
    AgsGroups = "layers.png"
    AgsHeading = "layout_header.png"
    AgsNotes = "note.png"

    Busy = "arrow_in.png"
    BulletDown = "bullet_arrow_down.png"
    BulletBlack = "bullet_black.png"

    Cancel = "bullet_black.png"
    Clear = "control.png"


    Document = "blue-folder-open-document.png"

    Export = "fill.png"
    Excel = "document-excel.png"

    FavIcon = "logo.png"

    FilterOn = "bullet_yellow.png"
    FilterOff = "bullet_blue.png"

    Folder = 'folder.png'
    FolderAdd = 'folder_add.png'
    FolderCopy = 'folder_page.png'
    FolderDelete = 'folder_delete.png'
    FolderOpen = 'folder_go.png'
    FolderRename = 'folder_edit.png'

    Groups = "tables-stacks.png"
    Group = "table.png"

    KeyField = "key.png"

    Import = "arrow-join-270.png"

    Project = "blue-document-list.png"
    Plus = "plus-small-white.png"

    Map = "map.png"
    Minus = "minus-small.png"

    Quit = 'control_eject.png'

    Refresh = "arrow_refresh.png"

    Save = "tick.png"
    Samples = "tag_yellow.png"
    Schedule = "table-heatmap.png"
    Source = "document-text.png"
    Summary = "page_white_swoosh.png"

    TestPoint = "bullet_purple.png"

    TypeCheckBox = "ui-checkbox.png"
    TypeDate = "ui-combo-box-calendar.png"
    TypeDecimal = "ui-text-field-password-green.png"
    TypeID = "type_id.svg.png"
    TypePicklist = "ui-combo-box-blue.png"
    TypeSci = "ui-text-field-password-yellow.png"
    TypeStandard = "ui-.png"
    TypeText = "ui-text-field.png"
    TypeUnknown = "ui-text-field-hidden.png"


    TickOn = "tick.png"
    TickOff = "bullet_black.png"

    Zip = "compress.png"
