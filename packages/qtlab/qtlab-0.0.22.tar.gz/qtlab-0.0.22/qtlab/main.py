#!/usr/bin/python3
import sys
from PyQt5 import QtWidgets, QtCore

try:
    from .__id__ import ID, APP_NAME
    from .backend import cli
except ImportError:
    from __id__ import ID, APP_NAME
    from backend import cli


class Main(QtCore.QObject):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.clipboard = parent.clipboard
        self.calc = QtWidgets.QWidget()
        self.hsp = QtWidgets.QWidget()
        self.peak = QtWidgets.QWidget()

    def _calcImport(self):
        try:
            from .frontend import calc
        except ImportError:
            from frontend import calc
        self.calc = calc.Main(self)

    def _hspImport(self):
        try:
            from .frontend import hsp
        except ImportError:
            from frontend import hsp
        self.hsp = hsp.Main(self)

    def _peakImport(self):
        try:
            from .frontend import peak
        except ImportError:
            from frontend import peak
        self.peak = peak.Main(self)

    @QtCore.pyqtSlot(dict)
    def cli(self, cmd):
        if "quit" in cmd:
            sys.exit()

        elif "hsp" in cmd:
            if not self.hsp.isVisible():
                self._hspImport()

        elif "peak" in cmd:
            if not self.peak.isVisible():
                self._peakImport()

        elif "calc" in cmd:
            if "toggle" in cmd and self.calc.isVisible():
                self.calc.close()
            else:
                self._calcImport()


def main(cmd=""):
    app = QtWidgets.QApplication(sys.argv)
    app.setDesktopFileName(ID)
    app.setApplicationName(APP_NAME)
    cmd = cli.parse(cmd)
    widget = Main(app)
    widget.cli(cmd)
    widgetBus = cli.QDBusObject(parent=widget)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
