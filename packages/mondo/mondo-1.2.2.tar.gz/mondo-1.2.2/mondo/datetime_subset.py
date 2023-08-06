# Copyright (c) 2016 Electric Power Research Institute, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the EPRI nor the names of its contributors may be used
#    to endorse or promote products derived from this software without specific
#    prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import logging

from PySide import QtGui, QtCore

from .ui_datetime_subset import Ui_DateTimeSubsetDialog

logger = logging.getLogger(__name__)


class DateTimeSubsetDialog(QtGui.QDialog, Ui_DateTimeSubsetDialog):
    def __init__(self, start, end, parent=None):
        # NOTE: WindowTitleHint | WindowSystemMenuHint disables "What's This"
        super().__init__(parent, QtCore.Qt.WindowTitleHint |
                         QtCore.Qt.WindowSystemMenuHint |
                         QtCore.Qt.MSWindowsFixedSizeDialogHint)

        self.start = start
        self.end = end

        self.setupUi(self)

        # write the all data labels
        self.allStart.setText(self.startDateTime.textFromDateTime(start))
        self.allEnd.setText(self.endDateTime.textFromDateTime(end))
        self.allDuration.setText(str(end.toPython() - start.toPython()))

        self.startDateTime.setDateTime(start)
        self.startDateTime.setWrapping(True)
        self.endDateTime.setDateTime(end)
        self.endDateTime.setWrapping(True)

        self.startDateTime.setCurrentSection(QtGui.QDateTimeEdit.SecondSection)
        self.endDateTime.setCurrentSection(QtGui.QDateTimeEdit.SecondSection)

        self.startDateTime.dateTimeChanged.connect(self.start_changed)
        self.startDateTime.editingFinished.connect(self.start_editing_finished)
        self.endDateTime.dateTimeChanged.connect(self.end_changed)
        self.endDateTime.editingFinished.connect(self.end_editing_finished)

        self.update_duration()

        self.layout().setSizeConstraint(QtGui.QLayout.SetFixedSize)

    def should_use_all(self):
        return self.useAllData.isChecked()

    def trim_datetime_to_range(self, value):
        if value < self.start:
            return self.start
        elif value > self.end:
            return self.end
        else:
            return value

    def datetime_in_range(self, value):
        return ((self.start <= value) and (value <= self.end))

    def get_subset(self):
        start = self.trim_datetime_to_range(self.startDateTime.dateTime())
        end = self.trim_datetime_to_range(self.endDateTime.dateTime())
        return (start, end)

    def start_changed(self, new_date_time):
        if self.datetime_in_range(new_date_time):
            if self.endDateTime.dateTime() < new_date_time:
                # start is later than end
                self.startDateTime.setStyleSheet(
                    "* { background-color: yellow }")
            else:
                # valid
                self.startDateTime.setStyleSheet("")
        else:
            # outside the bounds
            self.startDateTime.setStyleSheet("* { background-color: red }")

        self.update_duration()

    def end_changed(self, new_date_time):
        if self.datetime_in_range(new_date_time):
            if new_date_time < self.startDateTime.dateTime():
                # end is before start
                self.endDateTime.setStyleSheet(
                    "* { background-color: yellow }")
            else:
                # valid
                self.endDateTime.setStyleSheet("")
        else:
            # outside the bounds
            self.endDateTime.setStyleSheet("* { background-color: red }")

        self.update_duration()

    def start_editing_finished(self):
        if self.datetime_in_range(self.startDateTime.dateTime()):
            if self.endDateTime.dateTime() <= self.startDateTime.dateTime():
                self.endDateTime.setDateTime(self.startDateTime.dateTime())

                # trigger revalidation
                self.startDateTime.setDateTime(self.startDateTime.dateTime())
        else:
            self.startDateTime.setDateTime(self.start)

    def end_editing_finished(self):
        if self.datetime_in_range(self.endDateTime.dateTime()):
            if self.endDateTime.dateTime() <= self.startDateTime.dateTime():
                self.startDateTime.setDateTime(self.endDateTime.dateTime())

                # trigger revalidation
                self.endDateTime.setDateTime(self.endDateTime.dateTime())
        else:
            self.endDateTime.setDateTime(self.end)

    def update_duration(self):
        start_qdt = self.startDateTime.dateTime()
        end_qdt = self.endDateTime.dateTime()

        if (self.datetime_in_range(start_qdt) and
                self.datetime_in_range(end_qdt)):
            start = start_qdt.toPython()
            end = end_qdt.toPython()

            if end >= start:
                self.duration.setText(str(end - start))
            else:
                self.duration.setText(self.tr("Invalid"))
        else:
            self.duration.setText(self.tr("Invalid"))
