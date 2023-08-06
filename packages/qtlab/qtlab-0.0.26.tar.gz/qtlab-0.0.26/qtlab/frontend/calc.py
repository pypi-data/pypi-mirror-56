#!/usr/bin/python3
import json
import shutil
import sys
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets, QtTest, uic

try:
    from ..ui import calc_ui
    from ..__id__ import ID
    from ..backend import database, calc, common
except ValueError:
    from __id__ import ID
    from backend import database, calc, common

SET_FILE = Path.home() / ".config" / ID / "settings.json"
SOLIDS_FILE = Path.home() / ".config" / ID / "calc_solids.json"
SOLUTIONS_FILE = Path.home() / ".config" / ID / "calc_solutions.json"
LOCAL = str(Path(__file__).parents[0])


class InputLine(QtWidgets.QLineEdit):
    def __init__(self, parent, db):
        super().__init__()
        self.parent = parent
        self.db = db
        self.last = ""
        self.setTextMargins(5, 2, 5, 2) ##pour tous
        self.textChanged.connect(self._saveLast)
        self.textChanged.connect(self._validate)
        self.setPlaceholderText("...")
        self.completerReload()

    def focusInEvent(self, event):
        if self.last == self.text():
            QtCore.QTimer.singleShot(0, self.selectAll)
        QtWidgets.QLineEdit.focusInEvent(self, event)

    def _completerActivated(self):
        self.setFocus(False)
        index = self.parent.ui.tabWidget.currentIndex()
        if index == 0:
            self.parent.ui.molConcBox.setFocus(True)
        elif index == 1:
            self.parent.ui.dilC2Box.setFocus(True)
        QtCore.QTimer.singleShot(0, self.deselect)

    def _saveLast(self, text):
        # Avoid selectAll when focus is lost to completer's popup
        self.last = text

    def _validate(self, text):
        if text in self.db:
            ui = self.parent.ui
            index = ui.tabWidget.currentIndex()
            value = self.db[text]
            if index == 0:
                ui.molMWBox.setValue(value)
            elif index == 1:
                ui.dilC1Box.setValue(value)

    def completerReload(self):
        keys = list(self.db.keys())
        completer = common.Completer(self, keys)
        completer.activated.connect(self._completerActivated)
        self.setCompleter(completer)


class FramelessWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        font = self.font()
        font.setBold(True)
        self.closeButton = QtWidgets.QToolButton(self)
        self.closeButton.setText("✖")
        self.closeButton.setFont(font)
        self.closeButton.setAutoRaise(True)
        self.closeButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.closeButton.setStyleSheet("margin-bottom: 3px;")
        self.closeButton.clicked.connect(self.close)

    def keyPressEvent(self, event):
        # Escape key close the window
        if event.key() == QtCore.Qt.Key_Escape:
            if self.ui.escapeKeyBox.isChecked():
                self.close()
        QtWidgets.QMainWindow.keyPressEvent(self, event)

    def mouseMoveEvent(self, event):
        # Enable mouse dragging
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def mousePressEvent(self, event):
        # Enable mouse dragging
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def paintEvent(self, event):
        # Draw a one pixel border
        borderColor = QtGui.QColor("black")
        bgColor = QtGui.QColor(self.palette().color(QtGui.QPalette.Background))
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(borderColor))
        painter.drawRect(0, 0, self.width(), self.height())
        painter.setBrush(QtGui.QBrush(bgColor))
        painter.drawRect(1, 1, self.width()-2, self.height()-2)


class TabBar(QtWidgets.QTabBar):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.addTab("Molar solution")
        self.addTab("Solution dilution")
        self.addTab("Notes")
        self.addTab("Settings")
        self.setDocumentMode(True)
        self.currentChanged.connect(self._currentChanged)

    def _currentChanged(self, index):
        if index == 0:
            self.parent._calcMolar()
        elif index == 1:
            self.parent._calcDilution()
        else:
            self.parent.ui.statusLabel.clear()

    def mouseMoveEvent(self, event):
        # Enable mouse dragging
        if event.buttons() == QtCore.Qt.LeftButton:
            self.parent.move(event.globalPos() - self.dragPosition)
            event.accept()
        QtWidgets.QTabBar.mouseMoveEvent(self, event)

    def mousePressEvent(self, event):
        # Enable mouse dragging
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.parent.frameGeometry().topLeft()
            event.accept()
        QtWidgets.QTabBar.mousePressEvent(self, event)


class Main(FramelessWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.calc = calc.Calc()
        self._uiInit()
        self._iconsInit()
        self._settingsInit()
        self._settingsLoad()
        self.show()

    def closeEvent(self, event):
        self._saveDatabases()
        self._settingsSave()
        QtWidgets.QMainWindow.closeEvent(self, event)

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

    def _calcMolar(self):
        mw = self.ui.molMWBox.value()
        conc = self.ui.molConcBox.value()
        vol = self.ui.molVolBox.value()
        concUnit = self.ui.molConcCombo.currentText()
        volUnit = self.ui.molVolCombo.currentText()
        args = mw, conc, concUnit, vol, volUnit

        mass = self.calc.molar_solution(*args)
        self.ui.molResultBox.setValue(mass)

        formula = self.calc.molar_string(*args)
        self._updateFormula(formula)

    def _calcDilution(self):
        c1 = self.ui.dilC1Box.value()
        v2 = self.ui.dilV2Box.value()
        c2 = self.ui.dilC2Box.value()
        c1Unit = self.ui.dilC1Combo.currentText()
        v2Unit = self.ui.dilV2Combo.currentText()
        c2Unit = self.ui.dilC2Combo.currentText()
        resultUnit = self.ui.dilResultCombo.currentText()
        args = c1, c1Unit, c2, c2Unit, v2, v2Unit, resultUnit

        v1 = self.calc.dilution(*args)
        self.ui.dilResultBox.setValue(v1)

        formula = self.calc.dilution_string(*args)
        self._updateFormula(formula)

    def _dilClear(self):
        self.ui.dilNameLine.clear()
        self.ui.dilC1Box.setValue(0)
        self.ui.dilV2Box.setValue(0)
        self.ui.dilC2Box.setValue(0)

    def _dilDbAdd(self):
        name = self.ui.dilNameLine.text()
        unit = self.ui.dilC1Combo.currentText()
        c1 = self.ui.dilC1Box.value()
        c1_molar = c1 / calc.units_val[unit]
        self.dbSolutions[name] = c1_molar
        self.ui.dilNameLine.db = self.dbSolutions
        self.ui.dilNameLine.completerReload()

    def _dilDbDel(self):
        name = self.ui.dilNameLine.text()
        if name in self.dbSolutions:
            del self.dbSolutions[name]
            print(f"Deleted {name} from solutions database")
        self.ui.dilNameLine.clear()
        self.ui.dilC1Box.setValue(0)
        self.ui.dilNameLine.db = self.dbSolutions
        self.ui.dilNameLine.completerReload()

    def _iconsInit(self):
        icons = {}
        iconsPath = Path(__file__).parents[1] / "ui" / "icons"
        files = [x for x in iconsPath.glob("*.svg") if x.is_file()]
        for path in files:
            icons[path.stem] = QtGui.QIcon(str(path))
        self.ui.molDbAddButton.setIcon(icons["dbAdd"])
        self.ui.molDbDelButton.setIcon(icons["dbDel"])
        self.ui.molClearButton.setIcon(icons["clear"])
        self.ui.molCopyButton.setIcon(icons["copy"])
        self.ui.dilDbAddButton.setIcon(icons["dbAdd"])
        self.ui.dilDbDelButton.setIcon(icons["dbDel"])
        self.ui.dilClearButton.setIcon(icons["clear"])

    def _molCopy(self):
        name = self.ui.molNameLine.text()
        conc = self.ui.molConcBox.value()
        vf = self.ui.molVolBox.value()
        mass = self.ui.molResultBox.value()

        vfUnit = self.ui.molVolCombo.currentText()
        concUnit = self.ui.molConcCombo.currentText()
        vfUnit = calc.units_str[vfUnit]
        concUnit = calc.units_str[concUnit]

        if name and mass:
            # NaCl 200mM 5g/12mL
            txt = f"{name}\t{conc}{concUnit}\t{mass}g / {vf}{vfUnit}"
            if self.ui.copyClipboardBox.isChecked():
                self.parent.clipboard().setText(txt)
            if self.ui.copyNotesBox.isChecked():
                self.ui.notes.appendPlainText(txt)

    def _loadDatabases(self):
        solids = Path(SOLIDS_FILE ).is_file()
        solutions = Path(SOLUTIONS_FILE).is_file()

        if solids and solutions:
            with open(SOLIDS_FILE , "r") as f:
                self.dbSolids = json.load(f)
            with open(SOLUTIONS_FILE, "r") as f:
                self.dbSolutions = json.load(f)
        else:
            cfg = Path.home() / ".config" / ID
            Path(cfg).mkdir(parents=True, exist_ok=True)
            self._reset()
            print("Created default data files")

    def _saveDatabases(self):
        with open(SOLIDS_FILE, "w") as f:
            f.write(json.dumps(self.dbSolids, indent=2, sort_keys=False))
        with open(SOLUTIONS_FILE, "w") as f:
            f.write(json.dumps(self.dbSolutions, indent=2, sort_keys=False))

    def _molClear(self):
        self.ui.molNameLine.clear()
        self.ui.molMWBox.setValue(0)
        self.ui.molConcBox.setValue(0)
        self.ui.molVolBox.setValue(0)

    def _molDbAdd(self):
        name = self.ui.molNameLine.text()
        mw = self.ui.molMWBox.value()
        self.dbSolids[name] = mw
        self.ui.molNameLine.db = self.dbSolids
        self.ui.molNameLine.completerReload()

    def _molDbDel(self):
        name = self.ui.molNameLine.text()
        if name in self.dbSolids:
            del self.dbSolids[name]
            print(f"Deleted {name} from compounds database")
        self.ui.molNameLine.clear()
        self.ui.molMWBox.setValue(0)
        self.ui.molNameLine.db = self.dbSolids
        self.ui.molNameLine.completerReload()

    def _reset(self):
        solids_default = Path(LOCAL).parents[0] / "data" / "calc_solids.json"
        solutions_default = Path(LOCAL).parents[0] / "data" / "calc_solutions.json"
        shutil.copyfile(solids_default, SOLIDS_FILE)
        shutil.copyfile(solutions_default, SOLUTIONS_FILE)
        self._loadDatabases()

    def _resetDbs(self):
        self.ui.dilNameLine.db = self.dbSolutions
        self.ui.molNameLine.db = self.dbSolids
        self.ui.dilNameLine.completerReload()
        self.ui.molNameLine.completerReload()

    def _resetPrompt(self):
        msg = common.ConfirmPrompt()
        msg.setWindowTitle("Reset confirmation")
        msg.setText("This will reset databases of all compounds\n" +
                    "and solutions to their default value.\n" +
                    "\nDo you want to proceed?")
        if msg.exec_() == QtWidgets.QMessageBox.Apply:
            self._reset()
            self._resetDbs()

    def _settingsInit(self):
        self.settings = database.Database(SET_FILE)
        self.settings.fields = [self.ui.molConcCombo,
                                self.ui.molVolCombo,
                                self.ui.dilC1Combo,
                                self.ui.dilV2Combo,
                                self.ui.dilC2Combo,
                                self.ui.dilResultCombo,
                                self.ui.copyClipboardBox,
                                self.ui.copyNotesBox,
                                self.ui.displayFormulaBox,
                                self.ui.escapeKeyBox,
                                self.ui.notes]

    def _settingsLoad(self):
        db = self.settings.db["calc"]
        self.settings.load(db)

    def _settingsSave(self):
        db = self.settings.db["calc"]
        self.settings.save(db)

    def _uiInit(self):
        try:
            self.ui = calc_ui.Ui_MainWindow()
            self.ui.setupUi(self)
        except NameError:
            path = Path(LOCAL).parents[0] / "ui" / "calc_ui.ui"
            self.ui = uic.loadUi(path, self)

        path = str(Path(LOCAL).parents[0] / "ui" / "icons" / "qtlab-calc.svg")
        icon = QtGui.QIcon(path)
        self.setWindowIcon(icon)
        self.setWindowTitle("Solutions Calculator")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self._loadDatabases()

        self.tabBar = TabBar(self)
        self.ui.tabWidget.setTabBar(self.tabBar)
        self.ui.tabWidget.setCornerWidget(self.closeButton)
        self.ui.resetButton.clicked.connect(self._resetPrompt)

        self.ui.molNameLine = InputLine(self, db=self.dbSolids)
        self.ui.molInputLayout.insertWidget(0, self.ui.molNameLine)
        self.ui.molMWBox.valueChanged.connect(self._calcMolar)
        self.ui.molConcBox.valueChanged.connect(self._calcMolar)
        self.ui.molVolBox.valueChanged.connect(self._calcMolar)
        self.ui.molConcCombo.currentTextChanged.connect(self._calcMolar)
        self.ui.molVolCombo.currentTextChanged.connect(self._calcMolar)
        self.ui.molDbAddButton.clicked.connect(self._molDbAdd)
        self.ui.molDbDelButton.clicked.connect(self._molDbDel)
        self.ui.molClearButton.clicked.connect(self._molClear)
        self.ui.molCopyButton.clicked.connect(self._molCopy)

        self.ui.dilNameLine = InputLine(self, db=self.dbSolutions)
        self.ui.dilInputLayout.insertWidget(0, self.ui.dilNameLine)
        self.ui.dilC1Box.valueChanged.connect(self._calcDilution)
        self.ui.dilV2Box.valueChanged.connect(self._calcDilution)
        self.ui.dilC2Box.valueChanged.connect(self._calcDilution)
        self.ui.dilC1Combo.currentTextChanged.connect(self._calcDilution)
        self.ui.dilC2Combo.currentTextChanged.connect(self._calcDilution)
        self.ui.dilV2Combo.currentTextChanged.connect(self._calcDilution)
        self.ui.dilResultCombo.currentTextChanged.connect(self._calcDilution)
        self.ui.dilDbAddButton.clicked.connect(self._dilDbAdd)
        self.ui.dilDbDelButton.clicked.connect(self._dilDbDel)
        self.ui.dilClearButton.clicked.connect(self._dilClear)

        self.ui.molMWBox.installEventFilter(self)
        self.ui.molConcBox.installEventFilter(self)
        self.ui.molVolBox.installEventFilter(self)
        self.ui.molResultBox.installEventFilter(self)
        self.ui.dilC1Box.installEventFilter(self)
        self.ui.dilC2Box.installEventFilter(self)
        self.ui.dilV2Box.installEventFilter(self)
        self.ui.dilResultBox.installEventFilter(self)

        self.ui.molNameLine.setFocus(True)

    def _updateFormula(self, formula):
        if self.ui.displayFormulaBox.isChecked():
            self.ui.statusLabel.setText(formula)

