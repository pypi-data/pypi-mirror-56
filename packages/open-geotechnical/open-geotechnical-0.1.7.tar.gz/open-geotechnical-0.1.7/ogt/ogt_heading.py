#!/usr/bin/env python3
# coding: utf-8

from ogt.ags4 import DD


class OGTHeading:
    """"""
    def __init__(self, parent_group, hcell):

        self.parent_group = parent_group
        """parent group this heading belongs to

        :type: OGTGroup
        """

        self.head_cell = hcell
        """The HEADING cell

        :type: OGTCell
        """

        self.unit_cell = None
        """The UNIT cell

        :type: OGTCell
        """

        self.data_type_cell = None
        """The TYPE cell

        :type: OGTCell
        """

    def emit(self):
        """"""
        self.parent_group.emit()

    def __repr__(self):
        return "<Heading `%s`>" % self.head_code

    @property
    def head_code(self):
        """"""
        return self.head_cell.value

    @property
    def head_description(self):
        """"""
        data_dict = self.parent_group.data_dict()
        if data_dict and self.head_code in data_dict['headings_index']:
            idx = data_dict['headings_index'].index(self.head_code)
            return data_dict['headings'][idx]["head_description"]

        return "?"

    @property
    def required(self):
        """"""
        data_dict = self.parent_group.data_dict()
        if data_dict and self.head_code in data_dict['headings']:
            return data_dict['headings'][self.head_code]["required"]

        return None

    @property
    def key(self):
        """"""
        data_dict = self.parent_group.data_dict()
        if data_dict and self.head_code in data_dict['headings']:
            return data_dict['headings'][self.head_code]["key"]

        return None

    def set_unit(self, cell):
        """"""
        # TODO Check valid
        # dscell.value, errs = ags4.validate_clean_str(cell.value, upper=True)
        # self.ogtGroup.add_errors(errs)
        self.unit_cell = cell

    @property
    def unit(self):
        """"""
        return self.unit_cell.value

    @property
    def unit_label(self):
        """"""
        if self.unit:
            return self.unit
        return ""

    def set_data_type(self, cell):
        """"""
        self.data_type_cell = cell

    @property
    def data_type(self):
        """"""
        return self.data_type_cell.value

    @property
    def type_label(self):
        """"""
        if self.data_type:
            return self.data_type
        return ""

    def errors_count(self):
        """"""
        error_count = 0
        for cell in [self.head_cell, self.unit_cell, self.data_type_cell]:
            if cell is not None:
                error_count += cell.errors_count()

        return error_count

    def abbrs_picklist(self, ags=True, custom=True):
        """The piclist is ags and custom to this document

        :return: Abbrs for this heading
        """
        if self.data_type != "PA":
            return None

        return self.parent_group.parentDoc.abbrs(self.head_code)
        # FIXME is any of the code after this line used?
        drecs = {}
        if custom:
            grp = self.parent_group.parentDoc.group_from_code("ABBR")
            if grp:
                for cells_dic in grp.data:
                    cell_h = cells_dic.get("ABBR_HDNG")
                    if cell_h and cell_h.value == self.head_code:
                        dic = dict(code=cells_dic.get("ABBR_CODE").value,
                                   description=cells_dic.get("ABBR_DESC").value,
                                   list=cells_dic.get("ABBR_LIST").value,
                                   custom=True)
                        drecs[cells_dic.get("ABBR_CODE").value] = dic

        if ags:
            arecs = list(DD.abbrs_dict.get(self.head_code))
            for rec in arecs:
                drecs[rec['code']] = rec

        return [drecs[ki] for ki in sorted(drecs)]
