#!/usr/bin/python3
import os ##
from pathlib import Path
import pandas
import re
import shutil
import sys

from pathlib import Path
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from PyQt5 import QtWidgets, QtCore, QtGui, uic

try:
    from .ui import peak_ui
    from .__id__ import ID
    from .backend import cli, database, peak_adapters
except ImportError:
    from __id__ import ID
    from backend import cli, database, peak_adapters

SET_FILE = Path.home() / ".config" / ID / "settings.json"
TMP_FILE = Path.home() / ".config" / ID / "_tmp.xlsx"
LOCAL = str(Path(__file__).parents[0])


class ConvertThread(QtCore.QObject):
    busy = QtCore.pyqtSignal(bool)
    status = QtCore.pyqtSignal(str, str)
    success = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.ui = parent.ui
        self.name = ""

    def _convert(self, files, output):
        pos = iter(("A1", "J1", "A15", "J15"))
        spectrum_type = self.ui.typeBox.currentText()
        stats_min = self.ui.statsMinBox.value()
        stats_max = self.ui.statsMaxBox.value()
        focus_min = self.ui.focusMinBox.value()
        focus_max = self.ui.focusMaxBox.value()
        labels = \
        {
            "x": self.ui.xLine.text(),
            "y": self.ui.yLine.text(),
            "stats title": self.ui.titleStatsLine.text(),
            "stats x": self.ui.xStatsLine.text(),
            "stats y": self.ui.yStatsLine.text(),
        }

        if spectrum_type == "Cary WinUV (v3)":
            sheet = peak_adapters.UVSheet(files, labels)
        elif spectrum_type == "OMNIC for Dispertive Raman (v8)":
            sheet = peak_adapters.RamanSheet(files, labels)
        if self.ui.statsBox.isChecked():
            sheet.add_stats(x_min=stats_min, x_max=stats_max)
        sheet.add_chart(pos=next(pos), peaks=False)
        sheet.add_chart(pos=next(pos), peaks=True)

        if self.ui.focusBox.isChecked():
            sheet.add_chart(pos=next(pos), x_min=focus_min, x_max=focus_max, peaks=False)
            sheet.add_chart(pos=next(pos), x_min=focus_min, x_max=focus_max, peaks=True)
        sheet.save(output)

    @QtCore.pyqtSlot(list, str)
    def convert(self, files, output):
        self.busy.emit(False)
        try:
            self._convert(files, output)
            if len(files) == 1:
                self.name = str(Path(files[0]).stem)
            self.success.emit()
        except pandas.errors.ParserError:
            self.status.emit("red", "Conversion failed: ParserError. Wrong data type ?")
        except Exception as error:
            self.status.emit("red", str(error))
        self.busy.emit(True)


class Main(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self._uiInit()
        self._settingsInit()
        self._settingsLoad()

        self.worker = ConvertThread(self)
        self.workerThread = QtCore.QThread()
        self.worker.moveToThread(self.workerThread)
        self.worker.success.connect(self.save)
        self.worker.status.connect(self.statusUpdate)
        self.worker.busy.connect(self.ui.tree.setEnabled)
        self.worker.busy.connect(self.ui.convertButton.setEnabled)
        self.workerThread.start()

    def _convert(self):
        files = []
        for item in range(self.ui.tree.topLevelItemCount()):
            item = self.ui.tree.topLevelItem(item)
            files.append(item.text(0))
        self.ui.tree.clearSelection()
        self.statusUpdate("default", "Conversion in progress...")
        a1 = QtCore.Q_ARG(list, files)
        a2 = QtCore.Q_ARG(str, str(TMP_FILE))
        QtCore.QMetaObject.invokeMethod(self.worker, "convert", QtCore.Qt.QueuedConnection, a1, a2)

    def _clear(self):
        self.ui.tree.clear()
        self.ui.treeItemHook()

    def _settingsInit(self):
        self.settings = database.Database(SET_FILE)
        self.settings.fields = [self.ui.focusBox,
                                self.ui.statsBox,
                                self.ui.statsMinBox,
                                self.ui.statsMaxBox,
                                self.ui.focusMinBox,
                                self.ui.focusMaxBox,
                                self.ui.xLine,
                                self.ui.yLine,
                                self.ui.titleStatsLine,
                                self.ui.xStatsLine,
                                self.ui.yStatsLine]

    def _settingsLoad(self):
        last = self.settings.db["peak"]["last profile"]
        self._profileLoad(last)
        self.ui.typeBox.setCurrentText(last)

    def _settingsSave(self):
        current = self.ui.typeBox.currentText()
        db = self.settings.db["peak"]["profiles"][current]
        db.setdefault(current, {})
        self.settings.db["peak"]["autodetect"] = self.ui.autodetectBox.isChecked()
        self.settings.db["peak"]["last profile"] = current
        self.settings.save(db)

    def _profileLoad(self, profile):
        current = self.ui.typeBox.currentText()
        db = self.settings.db["peak"]["profiles"][current]
        self.settings.load(db)
        self.ui.autodetectBox.setChecked(self.settings.db["peak"]["autodetect"])
        self.ui.typeBox.clearFocus()

    def _saveDialog(self, name):
        dialog = QtWidgets.QFileDialog(self, "Save file as")#, name)
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        dialog.setNameFilter("*.xlsx")

        current = self.ui.typeBox.currentText()
        directory = self.settings.db["peak"]["profiles"][current]["output path"]
        dialog.setDirectory(directory)
        dialog.selectFile(name)

        if dialog.exec_():
            output = dialog.selectedFiles()[0]
            if not output.endswith(".xlsx"):
                output += ".xlsx"
            return output
        return None

    def _typeDetect(self, path):
        try:
            df = pandas.read_csv(path, sep=",", encoding="latin-1")
        except pandas.errors.ParserError:
            df = pandas.read_csv(path, sep=";", encoding="latin-1")

        strings, nums = [], []
        for index, col in enumerate(df.columns):
            if index > 1: break
            else:
                strings.append(is_string_dtype(df[col].dtype))
                nums.append(is_numeric_dtype(df[col].dtype))

        # Omnic: contain only floats
        if True not in strings:
            return "OMNIC for Dispertive Raman (v8)"

        # Cary WinUV: the two first row are strings
        elif True not in nums:
            return "Cary WinUV (v3)"

        return None

    def _uiInit(self):
        try:
            self.ui = peak_ui.Ui_MainWindow()
            self.ui.setupUi(self)
        except NameError:
            path = Path(LOCAL).parents[0] / "ui" / "peak_ui.ui"
            self.ui = uic.loadUi(path, self)

        path = str(Path(LOCAL).parents[0] / "ui" / "icons" / "qtlab-peak.svg")
        icon = QtGui.QIcon(path)
        self.setWindowIcon(icon)
        self.setWindowTitle("Peakcell: CSV to Excel Converter")

        self.ui.tree = Tree(self)
        self.ui.treeLayout.insertWidget(1, self.ui.tree)
        self.ui.typeBox.currentTextChanged.connect(self._profileLoad)
        self.ui.convertButton.clicked.connect(self._convert)
        self.ui.quitButton.clicked.connect(self.close)
        self.ui.clearButton.clicked.connect(self._clear)

        self.ui.statusRightLabel = QtWidgets.QLabel()
        self.ui.statusBar = QtWidgets.QStatusBar()
        self.ui.statusBar.addPermanentWidget(self.ui.statusRightLabel)
        self.ui.statusBar.setStyleSheet("QStatusBar::item { border: 0 }")
        self.setStatusBar(self.ui.statusBar)

        self.ui.tree.setFocus(True)
        self.setSaveEnabled(False)
        self.show()

    def treeItemHook(self):
        count = self.ui.tree.topLevelItemCount()
        if count == 0:
            self.setSaveEnabled(False)
        elif count == 1:
            if self.ui.autodetectBox.isChecked():
                item = self.ui.tree.topLevelItem(0)
                dataType = self._typeDetect(path=item.text(0))
                self.ui.typeBox.setCurrentText(dataType)

        if count > 0:
            self.statusUpdate("default")
            self.setSaveEnabled(True)
            self.ui.tree.setFocus(True)

    def setSaveEnabled(self, state):
        self.ui.convertButton.setEnabled(state)

    @QtCore.pyqtSlot(dict)
    def cli(self, cmd):
        if "quit" in cmd:
            self.parent.quit()

    @QtCore.pyqtSlot()
    def save(self):
        output = self._saveDialog(self.worker.name)
        if output:
            shutil.move(TMP_FILE, output)

            # Remember output path
            current = self.ui.typeBox.currentText()
            dirname = str(Path(output).parents[0])
            self.settings.db["peak"]["profiles"][current]["output path"] = dirname

            self.statusUpdate("green", "Conversion successful", output)
            self._settingsSave()
            self.setSaveEnabled(False)
            self.ui.tree.clear()
        else:
            self.statusUpdate("default", "Aborted")
        self.ui.tree.setFocus(True)

    @QtCore.pyqtSlot(str, str)
    def statusUpdate(self, color, left="", right=""):
        if color == "default":
            self.ui.statusBar.setStyleSheet("QStatusBar::item { border: 0 }")
        else:
            palettes = \
            {
                "green": {"bg": "#C6EFCE", "fg": "#004000"},
                "red": {"bg": "#FFC7CE", "fg": "#9C0006"}
            }
            bg = QtGui.QColor(palettes[color]["bg"])
            fg = QtGui.QColor(palettes[color]["fg"])

            palette = self.ui.statusBar.palette()
            palette.setColor(QtGui.QPalette.Window, bg)
            palette.setColor(QtGui.QPalette.WindowText, fg)
            self.ui.statusBar.setPalette(palette)
        self.ui.statusBar.showMessage(left)
        self.ui.statusRightLabel.setText(right)


class Tree(QtWidgets.QTreeWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setHeaderHidden(True)
        self.setAlternatingRowColors(True)
        self.setIndentation(6)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.viewport().installEventFilter(self)

    def _add(self, path):
        if path.suffix.lower() == ".csv":
            item = TreeItem(self)
            item.setText(0, str(path))
            index = self.currentIndex().row()

            if index == -1: index = 0
            self.insertTopLevelItem(index, item)
            item.setSelected(True)
            self.parent.treeItemHook()

    def _openDialog(self):
        dialog = QtWidgets.QFileDialog(self, "Open CSV files")
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        dialog.setNameFilter("*.csv *.CSV")

        current = self.parent.ui.typeBox.currentText()
        current = self.parent.settings.db["peak"]["profiles"].get(current)
        if current:
            directory = current["input path"]
            dialog.setDirectory(directory)

        if dialog.exec_():
            for f in dialog.selectedFiles():
                self._add(Path(f))

            # Remember the new input path
            current = self.parent.ui.typeBox.currentText()
            dirname = str(Path(f).parents[0])
            self.parent.settings.db["peak"]["profiles"][current]["input path"] = dirname

    def _translateHexCodes(self, string):
        """Find and replace hex codes from a string
        Replace '%5BFF1~10%5D.mp3 %21' to '[FF1~10].mp3 !'
        """
        # %\d{2}       Patterns starting with a %, followed by two digit
        # %\d[a-fA-F]  Patterns starting with a %, followed by one digit and one letter from a to F
        hexChars = re.findall(r"%\d{2}|%\d[a-fA-F]", string)
        for code in hexChars:
            litteral = code.replace("%", "0x")
            litteral = chr(eval(litteral))
            string = string.replace(code, litteral)
        return string

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        QtWidgets.QTreeWidget.dragEnterEvent(self, event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                path = url.toString(QtCore.QUrl.PreferLocalFile)
                path = self._translateHexCodes(path)
                path = Path(path)
                if path.is_file():
                    self._add(path)
                elif path.is_dir():
                    for p in path.rglob("*"):
                        if p.is_file():
                            self._add(p)
        QtWidgets.QTreeWidget.dropEvent(self, event)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if self.topLevelItemCount() == 0:
                self._openDialog()
        return QtCore.QObject.event(obj, event)

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Delete:
            for item in self.selectedItems():
                index = self.indexOfTopLevelItem(item)
                self.takeTopLevelItem(index)
        self.parent.treeItemHook()

    def paintEvent(self, event):
        if self.model() and self.model().rowCount(self.rootIndex()) > 0:
            QtWidgets.QTreeWidget.paintEvent(self, event)
            return
        p = QtGui.QPainter(self.viewport())
        p.drawText(self.rect(), QtCore.Qt.AlignCenter, "Drop CSV files here")


class TreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setFlags(self.flags() &~ QtCore.Qt.ItemIsDropEnabled)
