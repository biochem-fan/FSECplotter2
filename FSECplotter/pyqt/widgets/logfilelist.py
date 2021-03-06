#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from FSECplotter.core.logfile import *
from FSECplotter.pyqt.models.logfilelist_model import *
from FSECplotter.pyqt.view.logfilelist_view import *
import os
import platform


class LogfileListWidget(QtWidgets.QWidget):
    """Widget for control the logfiles"""

    def __init__(self, parent=None):
        super(LogfileListWidget, self).__init__(parent)

        # Standard item model
        self.model = LogfileModel(0, 5, self)
        self.selection_model = QtCore.QItemSelectionModel(self.model)

        self.treeview = LogfileListView(self)

        # set ItemModel to treeview widget
        self.treeview.setModel(self.model)
        self.treeview.setSelectionModel(self.selection_model)

        # TreeView setting
        self.treeview.setSelectionMode(
            QtWidgets.QAbstractItemView.ContiguousSelection
        )
        self.selection_model.clear()

        # set buttons
        self.open_button = QtWidgets.QPushButton(self)
        self.open_button.setObjectName("Open button")
        self.open_button.setText("Open file")

        self.delete_button = QtWidgets.QPushButton(self)
        self.delete_button.setObjectName("Delete button")
        self.delete_button.setText("Remove file")

        self.move_up_button = QtWidgets.QPushButton(self)
        self.move_up_button.setObjectName("Move-up button")
        self.move_up_button.setText("Move up")
        self.move_down_button = QtWidgets.QPushButton(self)
        self.move_down_button.setObjectName("Move-down button")
        self.move_down_button.setText("Move down")

        self.gridLay1 = QtWidgets.QGridLayout()
        self.gridLay1.addWidget(self.open_button, 0, 0, 1, 1)
        self.gridLay1.addWidget(self.delete_button, 0, 1, 1, 1)
        self.gridLay1.addWidget(self.move_up_button, 1, 0, 1, 1)
        self.gridLay1.addWidget(self.move_down_button, 1, 1, 1, 1)

        self.verLay1 = QtWidgets.QVBoxLayout()
        self.verLay1.addWidget(self.treeview)

        self.verLay2 = QtWidgets.QVBoxLayout(self)
        self.verLay2.addLayout(self.verLay1)
        self.verLay2.addLayout(self.gridLay1)

        # signal slot definition
        self.open_button.clicked.connect(self.open_file)
        self.delete_button.clicked.connect(self.delete_file)
        self.move_up_button.clicked.connect(lambda: self.move_selected(-1))
        self.move_down_button.clicked.connect(lambda: self.move_selected(1))

    def open_file(self):
        # open the file selection dialog
        # enable multiple selection
        filename = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Open file", os.path.expanduser('~'))
        for f in filename[0]:
            self.model.add_item(f)

    def delete_file(self):
        try:
            current_row = self.__get_current_index()
        except IndexOutOfRangeError:
            return

        self.model.delete_item(current_row)
        self.selection_model.clear()
        self.__select_row(current_row)

    def delete_all_files(self):
        while self.model.rowCount() > 0:
            self.model.delete_item(0)

    def move_selected(self, shift):
        try:
            current_row = self.__get_current_index()
        except IndexOutOfRangeError:
            return

        moved_to = self.model.move_item(current_row, int(shift))
        self.selection_model.clear()
        self.__select_row(moved_to)

    # private methods

    def __get_current_index(self):
        current_index = self.selection_model.currentIndex()
        current_row = current_index.row()
        if current_row == -1:
            QtWidgets.QApplication.beep()
            raise IndexOutOfRangeError
        return current_row

    def __select_row(self, row_idx):
        left_idx = self.model.index(row_idx, 0, QtCore.QModelIndex())
        right_idx = self.model.index(row_idx, self.model.columnCount() - 1)
        row_selection = QtCore.QItemSelection()
        row_selection.select(left_idx, right_idx)

        self.selection_model.setCurrentIndex(
            left_idx, QtCore.QItemSelectionModel.Rows)
        self.selection_model.select(
            row_selection, QtCore.QItemSelectionModel.Select)


class IndexOutOfRangeError(Exception):
    pass


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    win = LogfileListWidget()
    model = LogfileModel(0, 5, win)
    # win.setModel(model)

    win.show()

    app.exec_()
