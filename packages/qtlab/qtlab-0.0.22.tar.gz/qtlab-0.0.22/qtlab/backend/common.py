#!/usr/bin/python3
from PyQt5 import QtWidgets, QtCore


class Completer(QtWidgets.QCompleter):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.setFilterMode(QtCore.Qt.MatchContains)
        self.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() in (QtCore.Qt.Key_Down, QtCore.Qt.Key_Tab):
                self._nextCompletion()
                return True
            elif event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
                self.setCurrentRow(self.currentRow()-1)
                self.activated.emit(self.currentCompletion())
        return super().eventFilter(obj, event)

    def _nextCompletion(self):
        index = self.currentIndex()
        self.popup().setCurrentIndex(index)

        start = self.currentRow()
        if not self.setCurrentRow(start + 1):
            self.setCurrentRow(0)


class ConfirmPrompt(QtWidgets.QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setStandardButtons(QtWidgets.QMessageBox.Apply | QtWidgets.QMessageBox.Cancel)
        self.setDefaultButton(QtWidgets.QMessageBox.Cancel)
        self.setIcon(QtWidgets.QMessageBox.Warning)
