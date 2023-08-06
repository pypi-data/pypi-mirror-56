# coding: utf-8

from ogt import ags4
from ogt import CELL_COLORS


class OGTError:
    """"""
    WARN = 0
    ERR = 1
    OK = 5

    def __init__(self, message=None, cell=None, warn=False, rule=None):
        """Contains an error or warning

        .. code-block:: python

            cell = OGTCell(raw=" Samp ")

            if test_some_warning(cell.value):
                cell.add_error( OGTError(cell, "some not valid", warn=True)

            if test_some_error(cell.value):
                cell.add_error( OGTError(cell, "WTF !!")

            print( cell.errors )


        :param cell: reference to parent cell
        :type cell: OGTCell
        :param message: message string
        :type message: str
        :param warn: True if its not an error
        :type warn: bool
        :param rule: optional rule message
        :type rule: str or int
        """
        assert message is not None

        self.cell = cell
        """The parent cell of this error

        :type: OGTCell
        """

        self.err_type = OGTError.WARN if warn else OGTError.ERR
        """True to flag as error(default), False is a warning"""

        self.message = message
        """The error message

        :type: str
        """

        self.rule = None if rule is None else str(rule)
        """The ags4 rule of error"""

    def __repr__(self):
        return "<OGTError:%s: %s>" % ("ERR" if self.err_type else "WARN", self.message)


    @property
    def group_code(self):
        """"""
        return self.cell.parentHeading.parentGroup.group_code

    @property
    def head_code(self):
        """"""
        return self.cell.parentHeading.head_code

    @property
    def background(self):
        """Background color of error/warning"""
        return CELL_COLORS.err_bg if self.err_type == OGTError.ERR else CELL_COLORS.warn_bg


def to_upper(cell):
    """"""
    pre_up = str(cell.value)
    cell.value = cell.value.upper()
    if pre_up != cell.value:
        cell.add_error(OGTError(cell, "Not upper case `%s`" % pre_up, warn=True))


def ags4_descriptor(descriptor):
    """Check its case and whether its a data descriptor

    :return: Cleaned descriptor, valid_descroiptor and list of errors

    """

    # check upper
    up_des, errs = validate_upper(descriptor)

    # check only a2z
    cerrs = validate_a2z(up_des)
    if cerrs:
        errs.extend(cerrs)

    # check it a description
    if up_des in ags4.DD.descriptors():
        return up_des, True, errs

    errs.append(OGTError("Invalid descriptor `%s` " % up_des),
                warn=True, rule=3)
    return up_des, False, errs


def heading_code(group_code, cell):
    """"""
    grp = ags4.DD.group(group_code)
    if cell.value in grp['headings_index']:
        return

    mess = "Invalid heading `%s` in group `%s` " % (cell.value, group_code)
    cell.add_error(OGTError(cell, mess))


def data_type(cell):
    """"""
    types_dic = ags4.DD.data_types_dict
    if cell.value not in types_dic:
        mess = "Invalid type `%s` " % (cell.value)
        cell.add_error(OGTError(cell, mess))


def validate_clean_str(raw_code, upper=True):
    """
    :param raw_code: str to clean
    :type raw_code: str
    :param upper: Make string uppercase
    :type upper: bool
    :rtype: (str, [OGTError])
    :return: Stripped and optinal upper case
    """

    assert isinstance(raw_code, str)

    err_list = []

    # Check for whitespace
    code = str(raw_code).strip()
    if code != raw_code:
        if code == raw_code.lstrip():
            e = OGTError("Leading white space `%s`" % raw_code, warn=True)
            err_list.append(e)
        elif code == raw_code.rstrip():
            e = OGTError("Trailing white space `%s`" % raw_code, warn=True)
            err_list.append(e)
        else:
            e = OGTError("White space`%s`" % raw_code, warn=True)
            err_list.append(e)

    if not upper:
        return code, err_list


    ucode, xerrs = validate_upper(code)
    if len(xerrs) > 0:
        err_list.extend(xerrs)

    return ucode, err_list


def validate_upper(raw_str):
    """Validate uppercase

    :param raw_str:
    :type raw_str: str
    :rtype: (str, [OGTError])
    :return: Upper case string
    """
    err_list = []
    ustr = raw_str.upper()
    if ustr != raw_str:
        e = OGTError("Contains lower chars `%s`" % raw_str, warn=True)
        err_list.append(e)
    return ustr, err_list


A2Z = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS = "0123456789"
CHARS = A2Z + NUMBERS


def validate_a2z(astr):
    """Ensure string contains only A-Z uppercase

    :return: A list of errors
    """
    errs = []
    for idx, char in enumerate(astr):
        if char not in A2Z:
            errs.append(OGTError("Invalid char `%s` at position %s `%s`" % (char, idx + 1, astr), rule=19))
    return errs


def validate_group_code(group_code):
    """ :ref:`ags4_rule_19`
    :param group_code: group code to validate
    :rtype: (str, [OGTError])
    :return: Tuple with cleaned string and errors
    """

    group_code, errs = validate_clean_str(group_code, upper=True)

    # first check length for empty
    lenny = len(group_code)
    if lenny == 0:
        # no group code so get outta here
        errs.append(OGTError("Invalid GROUP, needs one char at least `%s`" % group_code,
                            rule=19))
        return group_code, errs

    # check over length
    if lenny > 4:
        errs.append(OGTError("Invalid GROUP, longer then four chars `%s`" % group_code,
                             rule=19))
        return group_code, errs

    # check characters are valid
    errs = []
    for idx, char in enumerate(group_code):
        if char in A2Z or char in NUMBERS:
            pass  # ok
        else:
            errs.append(OGTError("Invalid char in  GROUP position %s `%s`" % (idx+1, group_code),
                                 rule=19))

    return group_code, errs


def validate_heading_str(head_code):
    """Checks the heading is valid
    - cleaned code
    - whether fatal
    - errors list
    """

    head_code, errs = validate_upper(head_code)

    if "_" not in head_code:
        errs.append(OGTError("Invalid HEADING requires a _ `%s` not found" % head_code))
        # cannot continue ??
        return head_code, True, errs

    # split the heading into group + remainder
    group_code, head_part = head_code.split("_")

    # validate the group part
    group_code, errs = validate_group_code(group_code)
    if len(errs) > 0:
        # assume we cannot continue
        return group_code, True, errs

    if len(head_code) > 9:
        errs.append(OGTError("Invalid HEADING > 9 chars `%s`" % head_code,
                             rule="19a"))

    if len(head_code) == 0:
        errs.append(OGTError("Invalid HEADING needs at least one char `%s`" % head_code,
                             rule="19a"))

    return head_code, False, errs


def validate_heading_ags(head_code, group_code_in):
    """Check the heading is in ags data dict. This is done by
         - First check if the heading is in the group (eg SPEC_*)
         - Then split the HEAD_ING and check the group and the heading in theat group

    """
    # first get the group that this heading is in
    # check group exists
    grpdic = ags4.DD.group(group_code_in)

    if grpdic is None:
        return OGTError("Invalid GROUP `%s` for HEADING `%s`, not in ags data dict" % (group_code_in, head_code),
                        rule="9")

    heads = grpdic.get("headings")
    for h in heads:
        if head_code == h['head_code']:
            # Yipee, the head_code is in the origin group
            return None

    # split the head code amd check source group + heading i that group

    sgroup_code, _ = head_code.split("_")

    # check group exists
    grpdic = ags4.DD.group(sgroup_code)

    if grpdic is None:
        return OGTError("Invalid GROUP part of HEADING not in ags data dict `%s`" % head_code,
                        rule=9)

    heads = grpdic.get("headings")
    for h in heads:
        if head_code == h['head_code']:
            return None
    return OGTError("HEADING `%s` not found in GROUP `%s`" % (head_code, sgroup_code),
                    warn=True, rule=9)


def validate_type_ags(typ):

    types = ags4.DD.data_types_dict
    if typ in types:
        return None

    return OGTError("TYPE `%s` not ing AGS4 " % (typ), rule="TODO")


def validate_headings_sort(group_code, heading_codes):

    # get ags headings list for group
    ags_headings = ags4.DD.headings_index(group_code)
    if ags_headings is None:
        return

    plst = []
    for ags_head in ags_headings:
        if ags_head in heading_codes:
            plst.append(ags_head)
        # else:
        #    plst.append(None)
    if plst == heading_codes:
        return None

    clst = []
    cidxs = []

    for idx, c in enumerate(plst):
        if c is None:
            continue
        if heading_codes[idx] != c:
            clst.append(c)
            cidxs.append(idx + 1)
    if len(clst) == 0:
        return None
    errs = []
    for idx, cidx in enumerate(cidxs):
        mess = "heads order incorrect, should be `%s` cols %s " % (",".join(clst), ",".join([str(c) for c in cidxs]))
        errs.append(OGTError(message=mess, rule=9))
    return errs
