#!/usr/bin/env python3
# coding: utf-8
""""""
from ogt.ogt_validate import OGTError
from ogt import CELL_COLORS


class OGTCell:

    def __init__(self, parent_heading=None, parent_group=None, src_ref=None, lidx=None, cidx=None,
                 raw=None):
        """Core class that contains a cell value

        :param parent_heading: the parent heading this cell belong to
        :type parent_heading: OGTHeading
        :param src_ref: source reference
        :type src_ref: str
        :param lidx: line index in source
        :type lidx: int
        :param cidx: column index in source
        :type cidx: int
        :param raw: the raw value
        :type raw: str

        """

        self.parent_group = parent_group

        self.parent_heading = parent_heading
        """The heading this cell is within

        :type: OGTHeading

        """
        self.src_ref = src_ref
        """Source reference

        :type: str
        """

        self.lidx = lidx
        """Line index within source

        :type: int
        """

        self.cidx = cidx
        """column index

        :type: int
        """

        self.raw = raw
        """Raw value

        :type: str
        """

        self.value = None
        """actual value

        :type: str or None
        """

        self._import_warnings = []
        self._warnings = []
        self._errors = []
        self._strip()

    def __repr__(self):
        return "<OGTCell `%s`>" % self.value

    def _strip(self):
        # check and remove whitespace, called at import
        if self.raw is None:
            return
        self.value = self.raw.strip()
        if self.value != self.raw:

            if self.value == self.raw.lstrip():
                error = OGTError(self, "Leading white space `%s`" % self.raw, warn=True)
                self._import_warnings.append(error)

            elif self.value == self.raw.rstrip():
                error = OGTError(self, "Trailing white space `%s`" % self.raw, warn=True)
                self._import_warnings.append(error)

            else:
                error = OGTError(self, "White space`%s`" % self.raw, warn=True)
                self._import_warnings.append(error)

    def clear_errors(self):
        """Clears all errors and warnings"""
        del self._import_warnings[:]
        del self._warnings[:]
        del self._errors[:]

    @property
    def warnings_count(self):
        """"""
        return len(self._import_warnings) + len(self._warnings)

    def warnings_list(self):
        """"""
        return self._import_warnings + self._warnings

    def errors_list(self):
        """"""
        return self._errors

    @property
    def errors_count(self):
        """"""
        return len(self._errors)

    def add_error(self, err):
        """
        :param err: error/warning instance to add
        :type err: OGTError
        """
        if err.err_type == OGTError.WARN:
            self._warnings.append(err)
        else:
            self._errors.append(err)

    def background(self):
        """Background color

        Not really logic, but the idea is to color cells in code, and across www, desktop, mobile

        See :data:`~ogt.__init__.CELL_COLORS`
        """
        if self.errors_count:
            return CELL_COLORS.err_bg

        if self.warnings_count:
            return CELL_COLORS.warn_bg

        return CELL_COLORS.ok_bg
