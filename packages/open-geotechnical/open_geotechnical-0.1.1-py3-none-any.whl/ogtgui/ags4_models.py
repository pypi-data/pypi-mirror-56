# -*- coding: utf-8 -*-


from Qt import QtGui, QtCore, Qt, pyqtSignal

from ogt import ags4

from ogtgui.img  import Ico
from ogtgui import xobjects




class AGS4_TYPE:
    abbrev = "ABBR"
    abbrev_item = "ABBR_ITEM"
    group = "GROUP"
    heading = "HEADING"
    note = "NOTE"


class AGS4_COLORS:
    group = "#286225"
    abbrev = "#496FA3"


SHOW_NONE = "##__NONE__##"
"""Used to filter for nothing"""

def data_type_ico(ags_type):
    """Returns an icon filename for the data type"""
    v = ags_type.upper()

    # Date time
    if v in ["DT"]:
        return Ico.TypeDate

    # decimal places
    if v.endswith("DP"):
        return  Ico.TypeDecimal

    # UID
    # TODO: (is this realy UID in doucment ?? aslks pete)
    if v == "ID":
        return  Ico.TypeID

    # Picklists
    if v in ["PA", "PU", "PT"]:
        return  Ico.TypePicklist

    # Scientific stuff
    if v.endswith("SCI"):
        return  Ico.TypeSci

    # Boolean yes/no, false, true, not false
    if v == "YN":
        return  Ico.TypeCheckBox

    # text and text in general
    if v in ["X"]:
        return  Ico.TypeText

    # oopps
    return Ico.TypeUnknown

def data_type_qicon(ags_type):
    """Return a QIcon for and ags.data_type"""
    return Ico.icon(data_type_ico(ags_type))

##===================================================================
## Main
##===================================================================
class Ags4Object(QtCore.QObject):

    sigLoaded = pyqtSignal()

    def __init__( self, parent=None):
        super(QtCore.QObject, self).__init__(parent)

        self.modelUnits = UnitsModel(self)
        self.modelDataTypes = DataTypesModel(self)

        self.modelClasses = ClassesModel(self)

        self.modelGroups = GroupsModel(self)

        self.modelHeadings = HeadingsModel(self)

    def init(self):
        #self.modelNotes = NotesModel()
        self.units = UnitsModel(self)
        self.dataTypes = DataTypesModel(self)

        self.classes = ClassesModel(self)

        self.headings = HeadingsModel(self)

        #self.modelAbbrevClasses = ClassesModel(self)
        #self.modelAbbrevs = AbbrevsModel(self)

        #self.modelAbbrItems = AbbrevItemsModel(self)

        #self.modelGroups.sigClasses.connect(self.modelClasses.load_classes)

        #self.connect(self.modelAbbrevs, QtCore.SIGNAL("classes"), self.modelAbbrevClasses.load_classes)


    def load_init(self):
        #err = ags4.DD.setup_initialise()
        #if err:
        #    panicssss

        self.modelClasses.set_ags4dd(ags4.DD)
        self.modelGroups.set_ags4dd(ags4.DD)

        self.modelUnits.set_ags4dd(ags4.DD)
        #self.modelDataTypes.set_ags4dd(ags4.DD)

        #self.modelNotes.init_words()

        self.sigLoaded.emit()



    def get_group(self, code):
        return self.modelGroups.get_group(code)


    def get_notes(self, group_code):
        return self.modelNotes.get_notes(group_code)

    def get_heading(self, head_code):
        return self.modelHeadings.get_heading(head_code)

    def DEADget_picklist(self, abbrev):

        return self.modelAbbrevItems.get_picklist(abbrev)

class CG:
    code = 0
    description = 1
    cls = 2
    search = 3
    _col_count = 4

##===================================================================
## Groups
##===================================================================
class GroupsModel(QtCore.QAbstractItemModel):

    def __init__( self, parent=None):
        QtCore.QAbstractItemModel.__init__( self, parent)
        self.ags4dd = None

    def set_ags4dd(self, ags4dd):
        self.ags4dd = ags4dd
        #self.reset()

    def columnCount(self, midx):
        return CG._col_count

    def rowCount(self, midx):
        if self.ags4dd == None:
            return 0
        return self.ags4dd.groups_count()

    def index(self, row, col, parent=None):
        return self.createIndex(row, col)

    def parent(self, pidx=None):
        return QtCore.QModelIndex()

    def data(self, midxx, role):

        col = midxx.column()

        if role == Qt.DisplayRole:
            # the the ags grp
            grp = self.ags4dd.group_by_index(midxx.row())

            if col == CG.code:
                return grp['group_code']
            if col == CG.description:
                return grp['group_description']
            if col == CG.cls:
                return grp['class']
            if col == CG.search:
                return (grp['group_code'] + grp['group_description']).replace(" ", "")

        if role == Qt.DecorationRole:
            if col == CG.code:
                return Ico.icon(Ico.AgsGroup)

        if role == Qt.ForegroundRole:
            if col == CG.code:
                grp = self.ags4dd.group_by_index(midxx.row())
                return QtGui.QColor("#990000" if grp['group_required'] else "#000000")

        if role == Qt.FontRole:
            if col == CG.code:
                f = QtGui.QFont()
                f.setBold(True)
                f.setFamily("monospace")
                return f

        return None

    def rec_from_midx(self, midx):
        return self.ags4dd.group_by_index(midx.row())

    def headerData(self, p_int, orient, role=None):

        if orient == Qt.Horizontal and role == Qt.DisplayRole:
            heads = ["Code", "Description", "Classification", "Search"]
            return heads[p_int]


    def get_group(self, code):
        items = self.findItems(code, Qt.MatchExactly, CG.code)
        if len(items) == 0:
            # not in ags data dict
            return None
        ridx = items[0].index().row()
        return dict(	group_code=self.item(ridx, CG.code).s(),
                        group_description=self.item(ridx, CG.description).s(),
                        cls=self.item(ridx, CG.cls).s())

    def get_words(self):

        lst = []
        for ridx in range(0, self.rowCount()):
            lst.append( dict(type=AGS4_TYPE.group, description=self.item(ridx, CG.description).s(),
                            code=self.item(ridx, CG.code).s()))
        return lst


##===================================================================
## Headings
##===================================================================

class HeadingsModel(QtCore.QAbstractTableModel):

    class CH:
        """Columns NO's for the ;class:`~ogtgui.ags_models.HeadingsModel`"""
        action = 0
        head_code = 1
        description = 2
        unit = 3
        data_type = 4
        key = 5
        required = 6
        sort_order = 7
        example = 8
        _col_count = 9

    def __init__( self, parent):
        QtCore.QAbstractTableModel.__init__(self, parent)

        self.grpDD = None


    def index(self, row, col, parent=None):
        return self.createIndex(row, col)

    def set_group(self, grpdd):

        self.grpDD = grpdd

        self.modelReset.emit()

    def columnCount(self, midx=None):
        return self.CH._col_count

    def rowCount(self, midx=None):
        if self.grpDD == None:
            return 0
        return len(self.grpDD.get("headings_index"))

    def index(self, row, col, parent=None):
        return self.createIndex(row, col)

    def parent(self, pidx=None):
        return QtCore.QModelIndex()

    def data(self, midxx, role):

        col = midxx.column()

        if role == Qt.FontRole:
            if col == self.CH.head_code:
                f = QtGui.QFont()
                f.setBold(True)
                f.setFamily("monospace")
                return f


        if role == Qt.DisplayRole:

            rec = self.rec_from_midx(midxx)

            if col == self.CH.head_code:
                return rec['head_code']

            if col == self.CH.description:
                return rec['head_description']

            if col == self.CH.data_type:
                return rec['data_type']

            if col == self.CH.unit:
                return rec['unit']

            #if col == self.CH.key:
            #    return "KEY" if rec['key'] else ""

            if col == self.CH.required:
                return "Req" if rec['required'] else ""

            if col == self.CH.example:
                return rec['example']

            if col == self.CH.sort_order:
                return midxx.row() #rec['sort_order']

            return None

        if role == Qt.DecorationRole:
            if col == self.CH.data_type:
                rec = self.rec_from_midx(midxx)
                return data_type_qicon( rec['data_type'] )#

            if col == self.CH.key:
                rec = self.rec_from_midx(midxx)
                if rec['key']:
                    return Ico.icon(Ico.KeyField)

        if role == Qt.BackgroundRole:
            if col == self.CH.head_code:
                rec = self.rec_from_midx(midxx)
                if rec['head_code'].split("_")[0] == self.grpDD['group_code']:
                    return QtGui.QColor("#D2FBC4")
                #return QtGui.QColor("#efefef")

            if col == self.CH.required:
                rec = self.rec_from_midx(midxx)
                if rec['required']:
                    return QtGui.QColor("pink")
                #return QtGui.QColor("transparent")

        return None

    def get_rec(self, idx):
       return self.grpDD["headings"][ self.grpDD.get("headings_index")[idx] ]

    def get_heading_index(self, code):
        for ridx, rec in enumerate(self.grpDD["headings"]):
            if rec['head_code'] == code:
                return self.index(ridx, 0)
        return None

    def rec_from_midx(self, midx):
        return self.grpDD["headings"][ midx.row() ]

    def headerData(self, p_int, orient, role=None):

        if orient == Qt.Horizontal and role == Qt.DisplayRole:
            heads = ["", "", "Heading", "Description", "Unit", "Type", "Key","Req", "Srt", "Example"]
            return heads[p_int]


##===================================================================
## Abbrev Values
##===================================================================

class AbbrevItemsModel(QtCore.QAbstractItemModel):

    class MODE:
        doc = 0
        ags = 1


    class CA:
        """Columns no's for the :class:`~ogtgui.ags4_models.AbbrevItemsModel` """
        check = 0
        code = 1
        description = 2
        list = 3
        _col_count = 4

    CHK_KI = "__CHECKED__"

    sigCheckedChanged = pyqtSignal()

    def __init__( self, parent=None, ogtHead=None):
        QtCore.QAbstractItemModel.__init__(self, parent)

        self.ogtHead = ogtHead
        self.recs = None

        self.load_data()

    def load_data(self):
        if self.ogtHead == None:
            self.layoutChanged.emit()
            return

        self.recs = self.ogtHead.abbrs()
        #print(self.recs)
        self.modelReset.emit()

    def set_ags_heading(self, head):

        self.recs = None
        if head:
            abbrs = ags4.DD.abbrs_dict.get(head['head_code'])
            if abbrs:
                self.recs = abbrs
        self.modelReset.emit()

    def set_checked(self, selected):

        sel_code = selected['code'] if isinstance(selected, dict) else selected

        for i in range(0, self.rowCount()):
            rec = self.recs[i]
            rec[self.CHK_KI] = rec['code'] == sel_code

        self.layoutChanged.emit()

    def get_checked(self):
        for rec in self.recs:
            if rec.get(self.CHK_KI) == Qt.Checked:
                return rec
        return None

    def flags(self, midx):
        if midx.column() == self.CA.check:
            return Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def index(self, row, col, parent=None):
        return self.createIndex(row, col)

    def parent(self, pidx=None):
        return QtCore.QModelIndex()

    def columnCount(self, midx=None):
        return self.CA._col_count

    def rowCount(self, midx=None):
        if self.recs == None:
            return 0
        return len(self.recs)

    def headerData(self, p_int, orient, role=None):
        if orient == Qt.Horizontal and role == Qt.DisplayRole:
            heads = ["", "Code", "Description", "List"]
            return heads[p_int]

    def data(self, midxx, role):

        col = midxx.column()

        if role == Qt.DisplayRole:
            rec = self.recs[midxx.row()]

            #if col == self.CA.check:
            #    return rec['code']

            if col == self.CA.code:
                return rec['code']

            if col == self.CA.description:
                return rec['description']

            if col == self.CA.list:
                return rec['list']


        # checked
        if col == self.CA.check and role == Qt.CheckStateRole:
            return Qt.Checked if self.recs[midxx.row()].get(self.CHK_KI) else Qt.Unchecked

        # Background color
        if role == Qt.BackgroundRole:
            rec = self.recs[midxx.row()]
            if col == self.CA.list and rec["list"] != "AGS4":
                return QtGui.QColor("#FFCF9A")

            if rec.get(self.CHK_KI):
                if col == self.CA.check:
                    return QtGui.QColor("darkgreen")
                return QtGui.QColor("#FCFF94")
            return QtGui.QColor("transparent")

        # Make code font monospaced out man
        if col == self.CA.code and role == Qt.FontRole:
            f = QtGui.QFont()
            f.setBold(True)
            f.setFamily("monospace")
            return f

        return None

    def checked_count(self):
        return len(self.checked_codes())

    def checked_codes(self):
        lst = []
        for rec in self.recs:
            if rec[self.CHK_KI] and not rec['code'] in lst:
                lst.append(rec['code'])
        return sorted(lst)

    def midx_from_val(self, v):

        for ridx, rec in enumerate(self.recs):
            if rec['code'] == v:
                return self.index(ridx, 0)
        return None

    def val_from_midx(self, midx):
        return self.recs[midx.row()]


    def setData(self, midx, vv, role):

        if role == Qt.CheckStateRole and midx.column() == self.CA.check:

            # clear existing checked
            for rec in self.recs:
                rec[self.CHK_KI] = Qt.Unchecked

            rec = self.recs[midx.row()]
            rec[self.CHK_KI] = vv
            self.sigCheckedChanged.emit()
        self.layoutChanged.emit()
        return True

    def set_save_cell(self):
        #lst = []
        #for rec in self.recs:
        #    if rec.get(self.CHK_KI) and not rec['code'] in lst:
        #        lst.append(rec['code'])
        #
        cc = self.ogtHead.parentGroup.parentDoc.concat_char
        return cc.join( sorted(self.checked_codes()) )


##===================================================================
## Classes
##===================================================================
class ClassesModel(xobjects.XStandardItemModel):

    def __init__( self, parent=None):
        super(xobjects.XStandardItemModel, self).__init__(parent)

        self.ags4dd = None



    def set_ags4dd(self, ags4dd):
        self.ags4dd = ags4dd

        self.set_header(0, "Class")

        ## make root node,
        # all "class label" are kidz.
        items = self.make_blank_row()
        items[0].set("All", ico=Ico.Folder)
        self.appendRow(items)

        ## get unique list of classes by walking groups
        classes = []
        for g in self.ags4dd.groups_list():
            if not g['class'] in classes:
                classes.append(g['class'])
        classes.sort()

        rootItem = self.item(0, 0)  # 'All' parent

        ## remove existing nodes
        while rootItem.hasChildren():
            rootItem.removeRow(0)

        ## add items
        for r in classes:
            citems = self.make_blank_row()
            citems[0].set(r)
            rootItem.appendRow(citems)


##===================================================================
## Units + Types
##===================================================================

class UnitsModel(QtCore.QAbstractItemModel):

    class CU:
        unit = 0
        description = 1

    def __init__( self, parent=None):
        super(QtCore.QAbstractItemModel, self).__init__(parent)

        self.ags4dd = None

    def set_ags4dd(self, ags4dd):
        self.ags4dd = ags4dd
        self.layoutChanged.emit()

    def index(self, row, col, parent=None):
        return self.createIndex(row, col)

    def parent(self, pidx=None):
        return QtCore.QModelIndex()

    def columnCount(self, midx=None):
        return 2

    def rowCount(self, midx=None):
        if self.ags4dd == None:
            return 0
        return len(self.ags4dd.units_list)

    def headerData(self, p_int, orient, role=None):
        if orient == Qt.Horizontal and role == Qt.DisplayRole:
            heads = ["Type", "Description"]
            return heads[p_int]

    def data(self, midxx, role):

        col = midxx.column()

        if role == Qt.DisplayRole:
            # the the ags grp
            rec = self.ags4dd.units_list[midxx.row()]
            if col == self.CU.unit:
                return rec['code']
            if col == self.CU.description:
                return rec['description']

        if role == Qt.FontRole:
            if col == self.CU.unit:
                f = QtGui.QFont()
                f.setBold(True)
                f.setFamily("monospace")
                return f

        return None

    def midx_from_val(self, v):

        for ridx, rec in enumerate(self.ags4dd.units_list):
            if rec['code'] == v:
                return self.index(ridx, 0)
        return None

    def val_from_midx(self, midx):
        return self.ags4dd.units_list[midx.row()]


class DataTypesModel(QtCore.QAbstractItemModel):

    class CT:
        data_type = 0
        description = 1
        _col_count = 2



    def __init__( self, parent=None):
        super().__init__(parent)




    def midx_from_val(self, v):

        for ridx, rec in enumerate(ags4.DD.data_types):
            if rec['code'] == v:
                return self.index(ridx, 0)
        return None

    def val_from_midx(self, midx):
        return ags4.DD.data_types[midx.row()]

    def index(self, row, col, parent=None):
        return self.createIndex(row, col)

    def parent(self, pidx=None):
        return QtCore.QModelIndex()

    def columnCount(self, midx=None):
        return self.CT._col_count

    def rowCount(self, midx=None):
        if ags4.DD.data_types_list == None:
            return 0
        return len(ags4.DD.data_types_list)

    def headerData(self, p_int, orient, role=None):
        if orient == Qt.Horizontal and role == Qt.DisplayRole:
            heads = ["Type", "Description"]
            return heads[p_int]

    def data(self, midxx, role):

        col = midxx.column()

        if role == Qt.DisplayRole:
            rec = ags4.DD.data_types[midxx.row()]
            if col == self.CT.data_type:
                return rec['code']
            if col == self.CT.description:
                return rec['description']

        # if role == Qt.DecorationRole:
        #     if col == 0:
        #         return Ico.icon(Ico.AgsHeading)

        if role == Qt.FontRole:
            if col == 0:
                f = QtGui.QFont()
                f.setBold(True)
                f.setFamily("monospace")
                return f

        return None



AgsData = Ags4Object()
