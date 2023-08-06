#!/usr/bin/python3
import json
import unicodedata
import shutil
import sys
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets, QtTest, uic

try:
    from ..ui import hsp_ui
    from ..__id__ import ID
    from ..backend import database, hsp, common
except ValueError:
    from __id__ import ID
    from backend import database, hsp, common

SET_FILE = Path.home() / ".config" / ID / "settings.json"
SLV_FILE = Path.home() / ".config" / ID / "hsp_solvents.json"
GRP_FILE = Path.home() / ".config" / ID / "hsp_groups.json"
LOCAL = str(Path(__file__).parents[0])


class InputLine(QtWidgets.QLineEdit):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.last = ""
        self.setTextMargins(5, 2, 5, 2)
        self.textChanged.connect(self._resetPalette)
        self.textChanged.connect(self._saveLast)
        self.editingFinished.connect(self._validate)
        self.setPlaceholderText("...")

        completer = common.Completer(self, list(parent.db.keys()))
        completer.activated.connect(parent._updateTarget)
        self.setCompleter(completer)

    def _saveLast(self, text):
        # Avoid selectAll when focus is lost to completer's popup
        self.last = text

    def focusInEvent(self, event):
        if self.last == self.text():
            QtCore.QTimer.singleShot(0, self.selectAll)
        QtWidgets.QLineEdit.focusInEvent(self, event)

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            self.parent.searchDual()
        QtWidgets.QLineEdit.keyPressEvent(self, event)

    def _errorPalette(self):
        fg = QtGui.QColor("#ffc7ce")
        bg = QtGui.QColor("#9c0006")
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Base, bg)
        palette.setColor(QtGui.QPalette.Text, fg)
        self.setPalette(palette)

    def _normalize(self, text):
        # Normalize case and diacritics
        normalized = unicodedata.normalize("NFKD", text)
        normalized = "".join(c for c in normalized if unicodedata.category(c) != "Mn")
        return normalized.lower()

    def _resetPalette(self, text):
        self.setPalette(self.parent.palette())
        self.setAttribute(QtCore.Qt.WA_SetPalette, False)

    def _validate(self):
        text = self.text()
        bland_names = {}
        for name in self.parent.db:
            n = self._normalize(name)
            bland_names[n] = name

        if text:
            bland_input = self._normalize(text)
            if bland_input in bland_names:
                valid_input = bland_names[bland_input]
                self.setText(valid_input)
            else:
                self._errorPalette()


class GroupTree(QtWidgets.QTreeWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.current = "preferred"
        self.selectedItem = None
        self.setIndentation(5)
        self.setAlternatingRowColors(True)
        self.setStyleSheet("QTreeView::item {padding: 0 20px;}")
        self.setHeaderLabels(["Name", "𝛿D", "𝛿P", "𝛿H", "Molar Volume"])
        self.itemChanged.connect(self._itemChanged)
        self.itemClicked.connect(self._itemClicked)
        self.load()

    def keyPressEvent(self, event):
        item = self.currentItem()
        key = event.key()
        if key == QtCore.Qt.Key_Delete:
            index = self.indexOfTopLevelItem(item)
            self._deletePrompt(item.text(0), index)
        elif key == QtCore.Qt.Key_Space:
            if item:
                self._itemClicked(item)
        else:
            QtWidgets.QTreeWidget.keyPressEvent(self, event)

    def _delete(self, name, index):
        self.takeTopLevelItem(index)
        for grp in dict(self.parent.groups):
            if name in self.parent.groups[grp]:
                self.parent.groups[grp].remove(name)
        del self.parent.db[name]
        print(f"Deleted {name} from solvents database")

    def _deletePrompt(self, name, index):
        msg = common.ConfirmPrompt()
        msg.setWindowTitle("Delete confirmation")
        msg.setText(f"Please confirm deletion of '{name}'")
        if msg.exec_() == QtWidgets.QMessageBox.Apply:
            self._delete(name, index)

    def _itemChanged(self, item):
        state = bool(item.checkState(0))
        slv = item.text(0)
        db = self.parent.groups[self.current]
        if state:
            if slv not in db:
                db.append(slv)
        else:
            if slv in db:
                db.remove(slv)

    def _itemClicked(self, item):
        if item == self.selectedItem:
            state = bool(item.checkState(0))
            if state:
                item.setCheckState(0, QtCore.Qt.Unchecked)
            else:
                item.setCheckState(0, QtCore.Qt.Checked)
        else:
            self.selectedItem = item

    def load(self):
        self.clear()
        for slv in self.parent.db:
            item = GroupTreeItem(self, slv)
            if slv not in self.parent.groups[self.current]:
                item.setCheckState(0, QtCore.Qt.Unchecked)
                self.addTopLevelItem(item)

        group = self.parent.groups[self.current]
        for slv in sorted(group, reverse=True):
            item = GroupTreeItem(self, slv)
            item.setCheckState(0, QtCore.Qt.Checked)
            self.insertTopLevelItem(0, item)

        for i in range(0, self.columnCount()+1):
            self.resizeColumnToContents(i)

    def select(self, name):
        itemCount = self.topLevelItemCount()
        for item in range(itemCount):
            item = self.topLevelItem(item)
            if item.text(0) == name:
                index = self.indexOfTopLevelItem(item)
                item = self.takeTopLevelItem(index)
                self.insertTopLevelItem(0, item)
                self.setCurrentItem(item)
                self.selectedItem = item
                break


class GroupTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, name):
        super().__init__()
        self.setFlags(self.flags() &~ QtCore.Qt.ItemIsDropEnabled)
        self.setFlags(self.flags() &~ QtCore.Qt.ItemIsUserCheckable)

        slv = parent.parent.db[name]
        self.setText(0, name)
        self.setText(1, str(slv["dD"]))
        self.setText(2, str(slv["dP"]))
        self.setText(3, str(slv["dH"]))
        self.setText(4, str(slv["mv"]))


class SearchTree(QtWidgets.QTreeWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.clipboard = parent.parent.clipboard()
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setIndentation(5)
        self.setStyleSheet("QTreeView::item { padding: 0 20px; }")
        self.setHeaderLabels(["Solvent 1", "Solvent 2", "Solvent 3", "Ratio", "𝛿D", "𝛿P", "𝛿H", "Molar Volume", "Ra"])
        self.sortByColumn(8, QtCore.Qt.AscendingOrder)
        self.header().setMinimumSectionSize(0)

    def keyPressEvent(self, event):
        ctrl = event.modifiers() == QtCore.Qt.ControlModifier
        c = event.key() == QtCore.Qt.Key_C
        if ctrl and c:
            self._clipboardExport()
        else:
            QtWidgets.QTreeWidget.keyPressEvent(self, event)

    def _clipboardExport(self):
        item = self.currentItem()
        if item:
            export = ""
            for i in range(0, self.columnCount()+1):
                if item.text(i):
                    export += f"{item.text(i)}\t"
            self.clipboard.setText(export)

    def addItem(self, item):
        names = (item.text(0), item.text(1))
        s1 = self.parent.ui.s1Line.text()
        s2 = self.parent.ui.s2Line.text()
        s1_valid = not s1 or s1 not in names
        s2_valid = not s2 or s2 not in names
        if s1_valid and s2_valid:
            self.addTopLevelItem(item)

    def resizeToContent(self):
        for i in range(0, self.columnCount()+1):
            self.resizeColumnToContents(i)

        if not self.parent.worker.hsp.all:
            self.setColumnWidth(1, 0)  # Solvent 2
            self.setColumnWidth(2, 0)  # Solvent 3
            self.setColumnWidth(3, 0)  # Ratio
        else:
            single = self.parent.ui.filterSingleBox.isChecked()
            dual = self.parent.ui.filterDualBox.isChecked()
            if single:
                self.setColumnWidth(1, 0)  # Solvent 2
                self.setColumnWidth(2, 0)  # Solvent 3
                self.setColumnWidth(3, 0)  # Ratio
            elif dual:
                self.setColumnWidth(2, 0)  # Solvent 3
            self.setColumnWidth(7, 0)  # Molar Volume


class SearchTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setFlags(self.flags() &~ QtCore.Qt.ItemIsDropEnabled)

    def __lt__(self, other):
        column = self.treeWidget().sortColumn()
        key1 = self.text(column)
        key2 = other.text(column)
        try:
            return float(key1) < float(key2)
        except ValueError:
            return key1.lower() < key2.lower()

    def setColor(self, column, color):
        try:
            if color == "none":
                self.setData(column, QtCore.Qt.BackgroundRole, None)
                self.setData(column, QtCore.Qt.ForegroundRole, None)
            elif color == "preferred":
                self.setForeground(column, QtGui.QColor("#004000"))
                self.setBackground(column, QtGui.QColor("#c6efce"))
            elif color == "usable":
                self.setForeground(column, QtGui.QColor("#553400"))
                self.setBackground(column, QtGui.QColor("#ffeb9c"))
            elif color == "hazardous":
                self.setForeground(column, QtGui.QColor("#9c0006"))
                self.setBackground(column, QtGui.QColor("#ffc7ce"))
        except RuntimeError:
            pass


class WorkerThread(QtCore.QObject):
    addItem = QtCore.pyqtSignal(object)
    working = QtCore.pyqtSignal(bool)
    resize = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.busy = False
        self.hsp = hsp.HSP()

    def _makeItem(self, slv):
        slv = self.hsp.all[slv]
        item = SearchTreeItem(self)
        item.setText(0, slv["s1"])

        if "s3" in slv:
            r1, r2, r3 = slv['ratio']
            ratio = f"{r1}:{r2}:{r3}"
            item.setText(1, slv["s2"])
            item.setText(2, slv["s3"])
            item.setText(3, ratio)

        elif "s2" in slv:
            r1, r2 = slv['ratio']
            ratio = f"{r1}:{r2}"
            item.setText(1, slv["s2"])
            item.setText(3, ratio)

        item.setText(4, str(slv["dD"]))
        item.setText(5, str(slv["dP"]))
        item.setText(6, str(slv["dH"]))
        item.setText(8, str(slv["Ra"]))
        item = self._setColor(item)
        return item

    def _setColor(self, item):
        for grp in ("preferred", "usable", "hazardous"):
            for col in range (0, 3):
                if item.text(col) in self.parent.groups[grp]:
                    item.setColor(col, grp)
        return item

    def _show(self, db):
        for slv in db:
            item = self._makeItem(slv)
            self.addItem.emit(item)
        self.resize.emit()

    @QtCore.pyqtSlot(str, tuple, dict, list)
    def search(self, scope, dph, target, groups):
        self.busy = True
        self.working.emit(True)
        self.hsp.search(scope, dph, target, groups)
        self.working.emit(False)
        self.busy = False

    @QtCore.pyqtSlot()
    def showAll(self):
        self._show(self.hsp.all)

    @QtCore.pyqtSlot()
    def showSingle(self):
        self._show(self.hsp.single)

    @QtCore.pyqtSlot()
    def showDual(self):
        self._show(self.hsp.dual)

    @QtCore.pyqtSlot()
    def showTriple(self):
        self._show(self.hsp.triple)

    @QtCore.pyqtSlot()
    def stop(self):
        self.hsp.abort = True


class Main(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self._loadDatabases()
        self._uiInit()
        self.show()
        self.showMaximized()

        self.timer = QtCore.QElapsedTimer()
        self.worker = WorkerThread(self)
        self.workerThread = QtCore.QThread()
        self.worker.moveToThread(self.workerThread)
        self.workerThread.start()
        self.worker.addItem.connect(self.ui.searchTree.addItem)
        self.worker.working.connect(self._updateStatus)
        self.worker.working.connect(self._searchBlock)
        self.worker.resize.connect(self.ui.searchTree.resizeToContent)

        self.ui.searchAllButton.clicked.connect(self.searchAll)
        self.ui.searchSingleButton.clicked.connect(self.searchSingle)
        self.ui.searchDualButton.clicked.connect(self.searchDual)
        self.ui.searchTripleButton.clicked.connect(self.searchTriple)
        self.ui.filterAllBox.clicked.connect(self._updateFilter)
        self.ui.filterSingleBox.clicked.connect(self._updateFilter)
        self.ui.filterDualBox.clicked.connect(self._updateFilter)
        self.ui.filterTripleBox.clicked.connect(self._updateFilter)
        self.ui.groupPreferedButton.clicked.connect(self._updateGroupView)
        self.ui.groupUsableButton.clicked.connect(self._updateGroupView)
        self.ui.groupHazardousButton.clicked.connect(self._updateGroupView)
        self.ui.groupCustomButton.clicked.connect(self._updateGroupView)
        self.ui.groupClearButton.clicked.connect(self._groupClear)
        self.ui.groupAddButton.clicked.connect(self._groupAdd)
        self.ui.resetButton.clicked.connect(self._resetPrompt)

        self.ui.searchTree.currentItemChanged.connect(self._itemChanged)
        self.ui.s1Line.editingFinished.connect(self._updateTarget)
        self.ui.s2Line.editingFinished.connect(self._updateTarget)
        self.ui.dTargetBox.valueChanged.connect(self._customTarget)
        self.ui.pTargetBox.valueChanged.connect(self._customTarget)
        self.ui.hTargetBox.valueChanged.connect(self._customTarget)
        self.ui.targetS1VolBox.valueChanged.connect(self._updateVolume)
        self.ui.targetS2VolBox.valueChanged.connect(self._updateVolume)

        self.ui.dTargetBox.installEventFilter(self)
        self.ui.pTargetBox.installEventFilter(self)
        self.ui.hTargetBox.installEventFilter(self)
        self.ui.dGroupBox.installEventFilter(self)
        self.ui.pGroupBox.installEventFilter(self)
        self.ui.hGroupBox.installEventFilter(self)
        self.ui.mvGroupBox.installEventFilter(self)

        self._settingsInit()
        self._settingsLoad()
        self._updateTarget()
        self._showDefault()

    def closeEvent(self, event):
        self._solventsSave()
        self._groupsSave()
        self._settingsSave()

    def eventFilter(self, obj, event):
        # Select all on focus
        if event.type() == QtCore.QEvent.FocusIn:
            QtCore.QTimer.singleShot(0, obj.selectAll)

        # Replace , with .
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Comma:
                QtTest.QTest.keyPress(obj, QtCore.Qt.Key_Period, QtCore.Qt.NoModifier)
                QtTest.QTest.keyRelease(obj, QtCore.Qt.Key_Period, QtCore.Qt.NoModifier)
                return True
        return QtCore.QObject.event(obj, event)

    def _blockTargetBoxes(self, state):
        # Qt limitation; signal is blocked to ignore programatically changed value in QSpinBox
        self.ui.dTargetBox.blockSignals(state)
        self.ui.pTargetBox.blockSignals(state)
        self.ui.hTargetBox.blockSignals(state)

    def _customTarget(self):
        self.worker.hsp.reset()
        self.ui.s1Line.clear()
        self.ui.s2Line.clear()

    def _filter(self):
        if self.ui.filterAllBox.isChecked():
            return "showAll"
        elif self.ui.filterSingleBox.isChecked():
            return "showSingle"
        elif self.ui.filterDualBox.isChecked():
            return "showDual"
        elif self.ui.filterTripleBox.isChecked():
            return "showTriple"

    def _groupAdd(self):
        name = self.ui.groupNameLine.text()
        if name:
            dD = self.ui.dGroupBox.value()
            dP = self.ui.pGroupBox.value()
            dH = self.ui.hGroupBox.value()
            mv = self.ui.mvGroupBox.value()
            self.db[name] = {"dD": dD, "dP": dP, "dH": dH, "mv": mv}
            self._solventsSave()
            print(f"Added {name} to solvents database")

            self.ui.groupTree.load()
            self.ui.groupTree.select(name)
            self.ui.groupTree.setFocus(True)
            self._groupClear()

    def _groupClear(self):
        self.ui.groupNameLine.clear()
        self.ui.dGroupBox.setValue(0)
        self.ui.pGroupBox.setValue(0)
        self.ui.hGroupBox.setValue(0)
        self.ui.mvGroupBox.setValue(0)

    def _groupsSave(self):
        with open(GRP_FILE, "w") as f:
            f.write(json.dumps(self.groups, indent=2, sort_keys=False))
        print(f"Saved groups database")

    def _itemChanged(self, current, previous):
        if current:
            self.ui.dSelectLine.setText(current.text(4))
            self.ui.pSelectLine.setText(current.text(5))
            self.ui.hSelectLine.setText(current.text(6))
            self._updateDelta()

    def _loadDatabases(self):
        slv = Path(SLV_FILE).is_file()
        grp = Path(GRP_FILE).is_file()

        if slv and grp:
            with open(SLV_FILE, "r") as f:
                self.db = json.load(f)
            with open(GRP_FILE, "r") as f:
                self.groups = json.load(f)
        else:
            cfg = Path.home() / ".config" / ID
            Path(cfg).mkdir(parents=True, exist_ok=True)
            self._reset()
            print("Created default data files")

    def _readEnableDPH(self):
        dD = self.ui.dTargetEnableBox.isChecked()
        dP = self.ui.pTargetEnableBox.isChecked()
        dH = self.ui.hTargetEnableBox.isChecked()
        return (dD, dP, dH)

    def _readGroups(self):
        groups = []
        if self.ui.groupPreferedBox.isChecked():
            groups.append("preferred")
        if self.ui.groupUsableBox.isChecked():
            groups.append("usable")
        if self.ui.groupHazardousBox.isChecked():
            groups.append("hazardous")
        if self.ui.groupCustomBox.isChecked():
            groups.append("custom")
        return groups

    def _readTarget(self):
        self._updateTarget()
        dD = self.ui.dTargetBox.value()
        dP = self.ui.pTargetBox.value()
        dH = self.ui.hTargetBox.value()
        return {"dD": dD, "dP": dP, "dH": dH}

    def _reset(self):
        slv_default = Path(LOCAL).parents[0] / "data" / "hsp_solvents.json"
        grp_default = Path(LOCAL).parents[0] / "data" / "hsp_groups.json"
        shutil.copyfile(slv_default, SLV_FILE)
        shutil.copyfile(grp_default, GRP_FILE)
        self._loadDatabases()

    def _resetPrompt(self):
        msg = common.ConfirmPrompt()
        msg.setWindowTitle("Reset confirmation")
        msg.setText("This will reset solvent database and all\n" +
                    "groups content to their default value.\n" +
                    "\nDo you want to proceed?")
        if msg.exec_() == QtWidgets.QMessageBox.Apply:
            self._reset()
            self.ui.groupTree.load()

    def _search(self, scope):
        if self.worker.busy:
            QtCore.QMetaObject.invokeMethod(self.worker, "stop", QtCore.Qt.DirectConnection)
        else:
            target = self._readTarget()
            self.ui.searchTree.clear()
            self.ui.dTargetLine.setText("%.1f" % target["dD"])
            self.ui.pTargetLine.setText("%.1f" % target["dP"])
            self.ui.hTargetLine.setText("%.1f" % target["dH"])
            target = QtCore.Q_ARG(dict, target)
            scope = QtCore.Q_ARG(str, scope)
            groups = QtCore.Q_ARG(list, self._readGroups())
            dph = QtCore.Q_ARG(tuple, self._readEnableDPH())

            QtCore.QMetaObject.invokeMethod(self.worker, "search", QtCore.Qt.QueuedConnection, scope, dph, target, groups)
            QtCore.QMetaObject.invokeMethod(self.worker, self._filter(), QtCore.Qt.QueuedConnection)

    def _searchBlock(self, state):
        state = not state
        if state:
            self.ui.searchAllButton.setText("Optimize")
        else:
            self.ui.searchAllButton.setText("Stop")
        self.ui.searchSingleButton.setEnabled(state)
        self.ui.searchDualButton.setEnabled(state)
        self.ui.searchTripleButton.setEnabled(state)

    def _setColor(self, item):
        for grp in ("preferred", "usable", "hazardous"):
            for col in range (0, 3):
                if item.text(col) in self.groups[grp]:
                    item.setColor(col, grp)
        return item

    def _settingsInit(self):
        self.settings = database.Database(SET_FILE)
        self.settings.fields = [self.ui.s1Line,
                                self.ui.s2Line,
                                self.ui.targetS1VolBox,
                                self.ui.targetS2VolBox,
                                self.ui.dTargetBox,
                                self.ui.pTargetBox,
                                self.ui.hTargetBox,
                                self.ui.dTargetEnableBox,
                                self.ui.pTargetEnableBox,
                                self.ui.hTargetEnableBox,
                                self.ui.groupPreferedBox,
                                self.ui.groupUsableBox,
                                self.ui.groupHazardousBox,
                                self.ui.groupCustomBox,
                                self.ui.filterAllBox,
                                self.ui.filterSingleBox,
                                self.ui.filterDualBox,
                                self.ui.filterTripleBox]

    def _settingsLoad(self):
        db = self.settings.db["hsp"]
        self._blockTargetBoxes(True)
        self.settings.load(db)
        self._blockTargetBoxes(False)

    def _settingsSave(self):
        db = self.settings.db["hsp"]
        self.settings.save(db)

    def _showDefault(self):
        for slv in self.db:
            item = SearchTreeItem(self)
            item.setText(0, slv)
            item.setText(4, str(self.db[slv]["dD"]))
            item.setText(5, str(self.db[slv]["dP"]))
            item.setText(6, str(self.db[slv]["dH"]))
            item.setText(7, str(self.db[slv]["mv"]))
            item.setText(8, "-")
            item = self._setColor(item)
            self.ui.searchTree.addTopLevelItem(item)
        self.ui.searchTree.resizeToContent()

    def _solventsSave(self):
        with open(SLV_FILE, "w") as f:
            f.write(json.dumps(self.db, indent=2, sort_keys=False))
        print(f"Saved solvents database")

    def _uiInit(self):
        try:
            self.ui = hsp_ui.Ui_MainWindow()
            self.ui.setupUi(self)
        except NameError:
            path = Path(LOCAL).parents[0] / "ui" / "hsp_ui.ui"
            self.ui = uic.loadUi(path, self)

        path = str(Path(LOCAL).parents[0] / "ui" / "icons" / "qtlab-hsp.svg")
        icon = QtGui.QIcon(path)
        self.setWindowIcon(icon)
        self.setWindowTitle("HSP Utility - Hansen Solubility Parameters")

        self.ui.searchTree = SearchTree(self)
        self.ui.groupTree = GroupTree(self)
        self.ui.s1Line = InputLine(self)
        self.ui.s2Line = InputLine(self)
        self.ui.s1Line.setObjectName("s1Line")
        self.ui.s2Line.setObjectName("s2Line")
        self.ui.searchTreeLayout.insertWidget(0, self.ui.searchTree)
        self.ui.groupTreeLayout.insertWidget(0, self.ui.groupTree)
        self.ui.inputLayout.insertWidget(0, self.ui.s1Line)
        self.ui.inputLayout.insertWidget(1, self.ui.s2Line)

    def _updateDelta(self):
        try:
            dD = float(self.ui.dSelectLine.text()) - float(self.ui.dTargetLine.text())
            dP = float(self.ui.pSelectLine.text()) - float(self.ui.pTargetLine.text())
            dH = float(self.ui.hSelectLine.text()) - float(self.ui.hTargetLine.text())
            self.ui.dDeltaLine.setText("%.1f" % dD)
            self.ui.pDeltaLine.setText("%.1f" % dP)
            self.ui.hDeltaLine.setText("%.1f" % dH)
        except ValueError:
            pass

    def _updateFilter(self):
        if self.worker.hsp.all:
            self.ui.searchTree.clear()
        QtCore.QMetaObject.invokeMethod(self.worker, self._filter(), QtCore.Qt.QueuedConnection)

    def _updateGroupView(self):
        old = self.ui.groupTree.current
        if self.ui.groupPreferedButton.isChecked():
            new = "preferred"
        elif self.ui.groupUsableButton.isChecked():
            new = "usable"
        elif self.ui.groupHazardousButton.isChecked():
            new = "hazardous"
        elif self.ui.groupCustomButton.isChecked():
            new = "custom"

        if old != new:
            self.ui.groupTree.current = new
            self.ui.groupTree.load()

    def _updateStatus(self, working):
        if working:
            self.timer.start()
            self.statusBar().showMessage("Calculation in progress...")
        else:
            elapsed = round((self.timer.elapsed()/1000), 2)
            msg = f"Search done after {elapsed}s"
            self.statusBar().showMessage(msg)

    def _updateTarget(self):
        self._blockTargetBoxes(True)
        s1 = self.ui.s1Line.text()
        s2 = self.ui.s2Line.text()
        s1_vol = self.ui.targetS1VolBox.value()
        s2_vol = self.ui.targetS2VolBox.value()

        slv = None
        if s1 in self.db and s2 in self.db:
            s1, s2 = hsp.dph(s1), hsp.dph(s2)
            s1["vol"], s2["vol"] = s1_vol, s2_vol
            slv = hsp.combine(s1, s2)
        elif s1 in self.db:
            slv = self.db[s1]

        if slv:
            self.ui.dTargetBox.setValue(slv["dD"])
            self.ui.pTargetBox.setValue(slv["dP"])
            self.ui.hTargetBox.setValue(slv["dH"])
            self._updateDelta()
        self._blockTargetBoxes(False)

    def _updateVolume(self, value):
        sender = QtCore.QObject.sender(self)
        value = 100 - value
        if self.ui.targetS1VolBox is sender:
            self.ui.targetS2VolBox.setValue(value)
        else:
            self.ui.targetS1VolBox.setValue(value)
        self._updateTarget()

    def searchAll(self):
        self.ui.filterAllBox.setChecked(True)
        self._search(scope="all")

    def searchSingle(self):
        self.ui.filterSingleBox.setChecked(True)
        self._search(scope="single")

    def searchDual(self):
        self.ui.filterDualBox.setChecked(True)
        self._search(scope="dual")

    def searchTriple(self):
        self.ui.filterTripleBox.setChecked(True)
        self._search(scope="triple")
