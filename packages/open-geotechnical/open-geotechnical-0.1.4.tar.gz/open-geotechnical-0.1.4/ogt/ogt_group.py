# coding: utf-8

from ogt.ogt_heading import OGTHeading
from ogt import ags4
from ogt import ogt_validate
from ogt import ogt_cell


class OGTGroup:
    """Represents :term:`GROUP` with its headings and data"""

    def __init__(self, parentDoc=None,  group_code_cell=None, src_ref=None):
        """
        :param parentDoc: The document object this group is within
        :type parentDoc: OGTDocument
        :param group_code_cell: The cell containing the group code
        :type group_code_cell: OGTCell
        """

        assert parentDoc != None
        self.parentDoc = parentDoc
        """Pointer to parent document instance

        :type: OGTDocument
        """

        self.group_code_cell = group_code_cell
        """The four character group code"""

        self.headings_index = []
        self.headings_dict = {}
        """A `list` of head_code > ogtHeadings"""

        self.lost_idxs = []

        self._errors_cache = None

        self.data = []

    def __repr__(self):
        return "<Group '%s'>" % self.group_code

    @property
    def group_code(self):
        return self.group_code_cell.value

    @property
    def group_description(self):
        if self.data_dict():
            return self.data_dict()['group_description']
        return None

    @property
    def group_required(self):
        if self.data_dict():
            return bool(self.data_dict()['group_required'])
        return None

    @property
    def parent(self):
        if self.data_dict():
            return self.data_dict()['parent']
        return None

    @property
    def children(self):
        if self.data_dict():
            return self.data_dict()['children']
        return None

    def add_get_headings_row(self, row_cells, src_ref=None):

        # TODO src_ref

        ret_idx = []

        for cidx, hcell in enumerate(row_cells):
            # validate the headings string
            head_code = hcell.value
            # check heading not exists already
            oHead = self.heading_from_code(head_code)
            if oHead is None:
                # add to dic
                ogtHead = OGTHeading(self, hcell)
                hcell.parentHeading = ogtHead
                self.headings_dict[head_code] = ogtHead

                # TODO this needs to be inserted in correct plage
                self.headings_index.append(head_code)
            # add to list of headings used in the group/import
            ret_idx.append(head_code)

        return ret_idx

    def add_heading(self, rec):

        # check its there already
        head_code = rec['head_code']
        ogtHead = self.heading_from_code(head_code)
        if ogtHead:
            return ogtHead

        # get a list of dd heading for ordering
        head_order = ags4.DD.group(self.group_code)['headings_index']

        # get current heading
        curr_heads = list(self.headings_index)
        curr_heads.append(head_code)

        # make required sort order
        req_order = []
        for gc in head_order:
            if gc in curr_heads:
                req_order.append(gc)
                curr_heads.remove(gc)
        req_order.extend(curr_heads)

        insert_idx = req_order.index(head_code)

        hcell = ogt_cell.OGTCell(raw=head_code)
        ogtHead = OGTHeading(self, hcell)
        hcell.parentHeading = ogtHead
        self.headings_index.insert(insert_idx, head_code)
        self.headings_dict[head_code] = ogtHead

        print(self.headings_index)

        unitCell = ogt_cell.OGTCell(raw=rec['unit'], parent_heading=ogtHead)
        ogtHead.set_unit(unitCell)

        dataTypeCell = ogt_cell.OGTCell(raw=rec['data_type'], parent_heading=ogtHead)
        ogtHead.set_data_type(dataTypeCell)

        for dic in self.data:
            dic[head_code] = ogt_cell.OGTCell(raw="", parent_heading=ogtHead)

        self.emit()
        return ogtHead

    def heading_from_code(self, head_code):
        return self.headings_dict.get(head_code)

    def deadhas_heading(self, head_code):
        return head_code in self.headings_dict

    # def headings_sort(self):
    #     return self.headings_index
    #     # TODO
    #     if self._headings_sort is None:
    #         dd = self.data_dict()
    #         if dd is None:
    #             return []
    #         self._headings_sort = []
    #         if dd.headings_sort() is None:
    #             return self.headings.keys()
    #         else:
    #             for head_code in dd.headings_sort():
    #                 if head_code in self.headings:
    #                     self._headings_sort.append(head_code)

        return self._headings_sort

    @property
    def headings_list(self):
        """Return a list of heading """
        lst = []
        for hcode in self.headings_index:
            lst.append(self.headings_dict[hcode])
        return lst

    def heading_from_index(self, idx):
        # print(self.headings_index, idx)
        return self.headings_dict.get(self.headings_index[idx])

    def index_of_heading(self, head_code):
        for cidx, hc in enumerate(self.headings_index):
            if hc == head_code:
                return cidx
        return None

    @property
    def headings_count(self):
        """ no of headings in this group """
        return len(self.headings_index)

    def add_data_row(self, row_cells):
        self.data.append(row_cells)

    def insert_data_row(self, ridx, row_cells):
        self.data.insert(ridx, row_cells)

    def data_cell(self, ridx, cidx):
        """Return cells from row col, if it exists"""
        return self.data[ridx].get(self.headings_index[cidx])

    def raw_cell(self, ridx, cidx):
        try:
            return self._raw_rows[ridx][cidx]
        except IndexError:
            return None
        return ARGHH

    def add_lost_row(self, row_cells, lidx):
        """Not sure, but we need add rows with no descriptors, or merge erors"""
        self.lost_rows.append(lidx)

    def data_row_dict(self, ridx):
        dic = {}
        for hc, cell in self.data[ridx].items():
            dic[hc] = cell.value
        return dic

    def data_rows_dict(self):
        lst = []
        for row in self.data:
            dic = {}
            for hc, cell in row.items():
                dic[hc] = cell.value
            lst.append(dic)
        return lst

    def data_column_from_head_code(self, head_code, as_cells=True):
        lst = []
        for ridx in range(0, self.data_rows_count):
            cell = self.data[ridx].get(head_code)
            if as_cells:
                lst.append(cell)
            else:
                if cell is not None:
                    lst.append(cell.value if cell else None)
        return lst

    @property
    def data_rows_count(self):
        return len(self.data)

    def data_dict(self):
        """Returns the data dictionary for this group, if it exists

        :return: dict if exists, else `None`

        """

        # TODO maybe this needs to returen custom stuff as well ?

        return ags4.DD.group(self.group_code)

    def to_dict(self):
        """
        :rtype: dict
        :return: A dictionary with the ags structures data (see :ref:`extended_mode`)
        """

        if self.parentDoc.opts.extended:

            # shortcut to data dict
            grp_dd = self.data_dict()
            # TODO cleanup data dict mess here

            heads = []
            for idx, head_code in enumerate(self.headings_index):

                ags_data_dict = None
                if head_code in grp_dd['headings_index']:
                    cidx = grp_dd['headings_index'].index(head_code)
                    ags_data_dict = grp_dd['headings'][cidx]

                heads.append({
                            "head_code": head_code,
                            "data_dict": ags_data_dict,
                            "unit": self.unit_for_heading(head_code),
                            "type": self.data_type_for_heading(head_code)
                            })

            dic = {
                    "group_code": self.group_code,
                    "data_dict": grp_dd,
                    "headings": heads,
                    "headings_sort": self.headings_index,
                    "data": self.data_rows_dict()
            }
            return dic

        dic = {
            ags4.DESCRIPTOR.heading: self.headings_index,
            ags4.DESCRIPTOR.unit: self.units_list(),
            ags4.DESCRIPTOR.type: self.data_types_list(),
            ags4.DESCRIPTOR.data: self.data_rows_dict()
        }

        return dic

    def add_units_row(self, row_cells):

        self.rows.append(row_cells)
        self._update_col_count(row_cells)

    def units_list(self):

        lst = []
        for hcode in self.headings_index:
            lst.append(self.headings_dict[hcode].unit)

        return lst

    def unit_for_heading(self, hcode):
        # TODO cleanup units
        if hcode in self.headings_dict:
            return self.headings_dict[hcode].unit
        return None  # should never happen

    def set_data_types_row(self, row_cells, lidx):

        self.types_idx = lidx - self.group_start_lidx
        self.rows.append(row_cells)
        self._update_col_count(row_cells)
        for idx, cell in enumerate(row_cells[1:]):
            self._headings[idx].set_type(cell)

    def data_types_list(self):

        lst = []
        for hcode in self.headings_index:
            lst.append(self.headings_dict[hcode].data_type)
        return lst

    def data_type_for_heading(self, hcode):
        return self.headings_dict[hcode].data_type

    @property
    def errors_warnings_count(self):
        if self._errors_cache is None:
            self._update_errors_cache()
        return len(self._errors_cache)

    def _update_errors_cache(self):
        self._errors_cache = []
        for ridx in range(0, self.data_rows_count):
            for cell in self.data[ridx].values():  # TODO
                self._errors_cache.extend(cell.errors_list())

    def errors_list(self):
        if self._errors_cache is None:
            self._update_errors_cache()
        return self._errors_cache

    def emit(self):
        self.parentDoc.emit()

    def clear_errors(self):
        self._errors_cache = None
        for ridx, dic in enumerate(self.data):

            for cell in dic.values():
                if isinstance(cell, ogt_cell.OGTCell):
                    cell.clear_errors()
                else:
                    pass

    def validate(self):

        # ogt_validate.group_code(self.raw_cell(0, 1))
        NOS = [str(n) for n in range(0, 10)]
        NOS.append(".")

        # headings code
        for headObj in self.headings_dict.values():

            ogt_validate.heading_code(self.group_code, headObj.head_cell)
            ogt_validate.data_type(headObj.data_type_cell)

            hcode = headObj.head_code

            # validate data
            if headObj.data_type == "PA":
                # check picklist
                # TODO
                pickcodes = self.parentDoc.abbrs(hcode, code_list=True)
                for ridx in range(0, self.data_rows_count):
                    cells_dic = self.data[ridx]
                    cell = cells_dic.get(hcode)
                    if cell:
                        if not cell.value:
                            continue
                        if pickcodes is not None and cell.value not in pickcodes:
                            cell.add_error(ogt_validate.OGTError(cell, "Invalid code", warn=False))

            if headObj.data_type in ["1DP", "2DP", "3DP", "4DP"]:
                # nos = NOS
                # nos.append(".")
                for ridx in range(0, self.data_rows_count):
                    cells_dic = self.data[ridx]
                    cell = cells_dic.get(hcode)
                    if cell:
                        if cell.value != "":
                            # validate nos and .
                            for c in cell.value:
                                if c not in NOS:
                                    cell.add_error(ogt_validate.OGTError(cell, "Not a NO", warn=False))
                                    break

                            # check decimals
                            dp = int(headObj.data_type[0:1])
                            parts = cell.value.split(".")
                            if len(parts) == 0 or len(parts[1]) != dp:
                                cell.add_error(ogt_validate.OGTError(cell, "Incorrect decimals", warn=False))

            if headObj.data_type == "IDDEADDDDD":
                # ID
                # ids = self.get_column(hcode)

                for ridx in range(0, self.data_rows_count):
                    cells_dic = self._data[ridx]
                    cell = cells_dic.get(hcode)
                    if cell:
                        if cell.value not in pickcodes:
                            cell.add_error(ogt_validate.OGTError(cell, "Invalid code", warn=False))

        return
        for ridx, row in enumerate(self._raw_rows):

            for cidx, cell in enumerate(row):

                # validate descriptor

                if ridx == self.headings_idx:
                    # validate headings
                    cell.value, fatal, errs = ags4.validate_heading_str(cell.value, cidx=cidx, lidx=ridx)
                    self.add_errors(errs)

                    if not fatal:
                        errs = ags4.validate_heading_ags(cell.value, self.group_code, cidx=cidx, lidx=ridx)

                        self.add_errors(errs)

                if ridx == self.types_idx:
                    pass
