#!/usr/bin/python3
import copy
import json

from pathlib import Path
from PyQt5 import QtWidgets

try:
    from ..__db__ import DEFAULT
except ValueError:
    from __db__ import DEFAULT


class Database():
    def __init__(self, path):
        self.path = path
        path = Path(path)
        self.name = path.stem
        if path.is_file() and path.stat().st_size > 0:
            self._load()
            self._validate()
        else:
            path.parents[0].mkdir(parents=True, exist_ok=True)
            self.db = copy.deepcopy(DEFAULT)
            with open(path, "w") as f:
                f.write(json.dumps(self.db, indent=2, sort_keys=False))
            print(f"Created preferences file for '{self.name}'")

    def _load(self):
        with open(self.path, "r") as f:
            self.db = json.load(f)
        print(f"Loaded {self.name} database")

    def _repair(self, db, default=DEFAULT):
        for key in default:
            if isinstance(default[key], dict):
                db.setdefault(key, default[key])
                self._repair(db[key], default[key])
            else:
                db.setdefault(key, default[key])
            if not isinstance(default[key], type(db[key])):
                print(f"Fixed type for '{key}': {type(key)} to {type(default[key])}")
                db[key] = default.get(key)

    def _save(self):
        with open(self.path, "w") as f:
            f.write(json.dumps(self.db, indent=2, sort_keys=False))
        print(f"Saved {self.name} database")

    def _validate(self):
        old = json.dumps(self.db, sort_keys=True)
        self._repair(self.db)
        new = json.dumps(self.db, sort_keys=True)
        if not new == old:
            print(f"Repaired missing keys in {self.name} database")
            self._save()

    def load(self, db):
        for obj in self.fields:
            value = db[obj.objectName()]
            if isinstance(obj, QtWidgets.QLineEdit):
                obj.setText(value)
            elif isinstance(obj, QtWidgets.QComboBox):
                obj.setCurrentText(value)
            elif isinstance(obj, QtWidgets.QTextEdit) or isinstance(obj, QtWidgets.QPlainTextEdit):
                obj.setPlainText(value)
            elif isinstance(obj, QtWidgets.QCheckBox) or isinstance(obj, QtWidgets.QRadioButton):
                obj.setChecked(value)
            elif isinstance(obj, QtWidgets.QSpinBox) or isinstance(obj, QtWidgets.QDoubleSpinBox):
                obj.setValue(value)
            else:
                print(f"Could not handle object type {type(obj)}")

    def save(self, db):
        for obj in self.fields:
            name = obj.objectName()
            if isinstance(obj, QtWidgets.QLineEdit):
                db[name] = obj.text()
            elif isinstance(obj, QtWidgets.QComboBox):
                db[name] = obj.currentText()
            elif isinstance(obj, QtWidgets.QTextEdit) or isinstance(obj, QtWidgets.QPlainTextEdit):
                db[name] = obj.toPlainText()
            elif isinstance(obj, QtWidgets.QCheckBox) or isinstance(obj, QtWidgets.QRadioButton):
                db[name] = obj.isChecked()
            elif isinstance(obj, QtWidgets.QSpinBox) or isinstance(obj, QtWidgets.QDoubleSpinBox):
                db[name] = obj.value()
        self._save()
