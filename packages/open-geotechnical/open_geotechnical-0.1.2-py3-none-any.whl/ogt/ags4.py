
"""This module provides the Data Dict (:class:`DD` module variable), an instance of :class:`AGS4_DataDict`

- This is used to present and validate :term:`ags4` files.
- See :ref:`ags4_data_dict`

"""

import os

from ogt import PROJECT_ROOT_PATH
from ogt import utils
from ogt.ogt_validate import OGTError

DICT_DTYP = "DICT_DTYP"


def ags4dd_file_path():
    """
    :rtype: str
    :return: Absolute path to the `ags4.min.json` data dict file
    """
    return os.path.abspath(os.path.join(PROJECT_ROOT_PATH, "ogtserver", "static",  "ags4.min.json"))


class DESCRIPTOR:
    """Constants defining the data descriptors (See :ref:`ags4_rule_3`)

       - The data descriptor is in the first column of every AGS row
       - If the first column is not one of above, then its an error.
    """
    group = "GROUP"
    heading = "HEADING"
    unit = "UNIT"
    data_type = "TYPE"
    data = "DATA"


class AGS4DataDict:
    """This class contains all the ags4 data dict """

    @staticmethod
    def group_header():
        """The list of headers as required and defined in :ref:`ags4_rule_2b`

        :type: list[str]
        :return: A list of `descriptors` in order
        """
        return [
            DESCRIPTOR.group,
            DESCRIPTOR.heading,
            DESCRIPTOR.unit,
            DESCRIPTOR.data_type
        ]

    @staticmethod
    def descriptors():
        """
        :return: A list of descriptors in correct order (see :ref:`ags4_rule_3`)
        :rtype: list
        """
        return [
            DESCRIPTOR.group, DESCRIPTOR.heading, DESCRIPTOR.unit, DESCRIPTOR.data_type, DESCRIPTOR.data
        ]

    def __init__(self):

        self.initialised = False
        """True if loaded with no errors (see :meth:`AGS4_DataDict.setup_initialise`"""

        self._data = None
        self._groups_dict = None
        self._groups_index = None
        self.abbrs_dict = None
        self._data_types = None
        self._units = None

        self._types_lookup_cache = None

        self.setup_initialise()


    def setup_initialise(self):
        """Check env is sane and loads the ags data dict file"""

        if not os.path.exists(ags4dd_file_path()):
            return "Missing ags4 data dict %s" % ags4dd_file_path()

        data, err = utils.read_json_file(ags4dd_file_path())
        if err:
            print("error..", err)
            return err

        self.abbrs_dict = data['abbrs']

        self._groups_dict = data['groups']

        self._groups_index = sorted(self._groups_dict.keys())

        # Walk groups/headings and create a _words dict for lookup
        self.words = {}
        # TODO
        # if False:
        #     for grp in self._groups_dict.itervalues():
        #         self.words[grp['group_code']] = dict(type="group",
        #                                               code=grp['group_code'],
        #                                               description=grp['group_description'])
        #         for head in grp['headings']:
        #             if not head['head_code'] in self.words: # not add dupes
        #                 self.words[head['head_code']] = dict(type="heading",
        #                                                       code=head['head_code'],
        #                                                       description=head['head_description'])

        self.initialised = True

    def groups_count(self):
        """
        :rtype: int
        :return:  Count of groups
        """
        return len(self._groups_index)

    def group_by_index(self, idx):
        """
        :param idx: index
        :type idx: int
        :rtype: dict
        :return:  dict at given index
        """
        return self._groups_dict[self._groups_index[idx]]

    def groups_list(self):
        return [self._groups_dict[gki] for gki in self._groups_index]

    def groups_dict(self):
        """
        :rtype: dict[group_code] -> dict
        :return: All groups with group code as key
        """
        return self._groups_dict

    def group(self, group_code):
        """
        :param group_code: four character group code
        :type group_code: str
        :rtype: dict or None
        :return:  the group data if successful, else `None`
        """
        return self._groups_dict.get(group_code)

    @property
    def data_types(self):
        """list of :term:`TYPE` s  (:ref:`ags4_rule_17`)

        :type: list[dict]
        """
        return self.abbrs_dict.get("DICT_DTYP")

    @property
    def data_types_list(self):
        """List of TYPE codes

        :type: list[str]
        """
        return [rec['code'] for rec in self.data_types]
        return self.abbrs_dict.get("DICT_DTYP")

    @property
    def data_types_dict(self):
        """data types the abbr code as key

        :type: dict[code] => dict
        """
        dic = {}
        for rec in self.data_types:
            dic[rec['code']] = rec
        return dic

    @property
    def units_list(self):
        """list of units (:ref:`ags4_rule_8`)

        :type: list
        """
        return self.abbrs_dict.get("UNIT_UNIT")

    def abbrs(self, head_code):
        """Abbreviations for heading (:ref:`ags4_rule_16`)

        :param head_code: heading code
        :type head_code: str
        :rtype: list[dict] else None
        :return:  a dict with the picklist if successful else `None`
        """
        recs = self.abbrs_dict.get(head_code)
        if recs:
            return recs
        return None

    def headings(self, group_code):
        """
        :param group_code: four characteter group code
        :type group_code: str
        :rtype: list[dict]
        :return: Headings in the group
        """
        if group_code not in self._groups_dict:
            return None
        return self._groups_dict[group_code]["headings"]

    def headings_index(self, group_code):
        """
        :param group_code: Four char group code
        :type group_code: str
        :rtype: list[str] or None
        :return: list of heading codes if group exist
        """
        if group_code not in self.groups_list():
            return None
        return [h['head_code'] for h in self._groups_dict[group_code]["headings"]]

    def heading(self, head_code):
        """
        Attempts to get the heading data from head_code (this
        may not work as expected as some groups are missing eg `SPEC`)

        :param hcode: heading code
        :type hcode: str
        :rtype: (dict or None, str)
        :return: Tuple if  data and error
        """
        gc = head_code.split("_")[0]
        if gc not in self._groups_dict:
            return None, "Invalid Group `%s` in head code  %s " % (gc, head_code)

        if head_code in self._groups_dict[gc]["headings"]:
            return self._groups_dict[gc]["headings"][head_code], None
        return None, "Invalid headcode `%s` in group  %s " % (head_code, gc)

    def classified_groups(self):
        """
        :rtype: dict[classificaton] => list[group_dict]
        :return: groups nested by classification
        """
        classes = {}
        for gcode, grp in self.groups_dict().items():
            cls = grp['class']
            if cls not in classes:
                classes[cls] = {}
            classes[cls][gcode] = grp
        return classes


DD = AGS4DataDict()
"""Global Instance of :class:`AGS4DataDict` initialised on import """


def summary_to_string(summary):

    ret = ""

    for sum_dic in summary:
        ret += report_to_string(sum_dic)

    return ret


def report_to_string(report):
    ret = "=" * 50
    ret += "\n%s\n" % report['file_path']
    ret += "-" * 50
    ret += "\n"

    for rule, dic in sorted(report['rules'].items()):
        if len(dic['errors']) == 0 and len(dic['problems']) == 0:
            pass
        else:
            ret += "%s:" % rule.replace("_", " ").capitalize()
            ret += " FAIL\n"

            if len(dic['errors']):
                ret += "\tSystem Errors:\n"
                for item in dic['errors']:
                    ret += "\t\t%s\n" % item

            lp = len(dic['problems'])
            if lp:
                ret += "\tProblem: %s %s\n" % (lp, "item" if lp == 1 else "items")
                for prob in dic['problems']:
                    ret += "\t\t%s\n" % prob

    return ret


def rule_1(doc):
    """ Validate :ref:`ags4_rule_1`

    :param raw_str:
    :rtype: tuple
    :return:
        - A list of ags_errors
        - A list of sys_errors
    """
    warnings = []
    errors = []
    try:
        # try and force to ascii in a one liner
        doc.source.decode("ascii")
        return warnings, errors

    except UnicodeDecodeError:

        # raw_str has problem somewhere.
        # so split to lines, = line
        # and then check every char in line = column
        # if char fail, we add to errrors
        errors.append("Unicode decode error")
        for lidx, line in enumerate(doc.source.split("\n")):

            for cidx, charlie in enumerate(line):
                # TODO . check visible.. maybe some < 30 chard are a hacker
                if ord(charlie) < 128:
                    pass
                else:
                    warnings.append(dict(line=lidx+1, column=cidx+1, illegal=[]))
    return warnings, errors


def rule_2(doc):
    """ Validate :ref:`ags4_rule_2`

    :param doc:
    :type doc: :class:`~ogt.ogt_doc.OGTDocument`
    :rtype: tuple
    :return:
        - a list of ags_errors
        - a list of sys errors
    """
    problems = []
    # report = []
    errors = []

    RULE = 2

    # check more than one group
    if doc.groups_count() < 2:
        p = OGTError(message="Need more than one group")
        problems.append(p)

    # Each data GROUP shall comprise a number of GROUP HEADER
    # TODO

    # rows must have one or more ref DATA rows
    for group_code, grp in doc.groups.items():
        if len(grp.data) == 0:
            p = OGTError(group_code, rule=RULE)
            problems.append(p)
            # report.append("group `%s` has no DATA rows" % group_code)

    # Rule 2b - CRLF end each line
    # so we in unix.. so split source with \n and check there's a \r at end
    # can only be done with raw files
    # TODO
    l_rep = []

    # Rule 2c GROUP HEADER
    # loop each group, and check the headers
    l_rep = []
    for group_code, grp in doc.groups.items():

        for idx, dd in enumerate(DD.group_header()):

            if grp.csv_rows()[0] != dd:
                p = OGTError(group_code, rule=RULE)

                p.message = "GROUP_HEADER error. "
                p.message += "Incorrect order line "
                problems.append(p)

    if len(l_rep):
        # report.append(l_rep)
        pass

    return problems, errors


EXAMPLES_FILE = os.path.join(PROJECT_ROOT_PATH, "ogtserver", "static", "ags4_examples.min.json")


def examples_all():
    # TODO check dir exists

    data, err = utils.read_json_file(EXAMPLES_FILE)
    return data, err


def examples_list():
    data, err = utils.read_json_file(EXAMPLES_FILE)
    if err:
        return None, err
    return [{"file_name": r['file_name']} for r in data['ags4_examples']], None


def example(file_name):

    data, err = examples_all()
    if err:
        return None, err
    for r in data['ags4_examples']:
        if r['file_name'] == file_name:
            return r, None
    return None, "Example `%s` not found " % file_name

