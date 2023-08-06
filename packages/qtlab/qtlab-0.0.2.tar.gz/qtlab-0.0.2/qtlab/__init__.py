#!/usr/bin/python3
import pathlib
import shutil
import sys
from PyQt5 import QtDBus

try:
    src = pathlib.Path(__file__).parents[1].joinpath("__id__.py")
    dst = pathlib.Path(__file__).parents[0].joinpath("__id__.py")
    shutil.copyfile(src, dst)
except FileNotFoundError:
    pass

try:
    from .__id__ import ID, HELP
except ImportError:
    from __id__ import ID, HELP


def main():
    service = f"org.{ID}"
    path = f"/org/{ID}"
    bus = QtDBus.QDBusConnection.sessionBus()
    interface = QtDBus.QDBusInterface(service, path, "", bus)

    cmd = sys.argv[1:]
    if not cmd or "--help" in cmd or "-h" in cmd:
        for h in HELP:
            print(h)

    elif interface.isValid():
        interface.call("ParseCommands", cmd)
        sys.exit(0)

    else:
        try:
            app = __import__(f"{ID}.main", fromlist=["main"])
        except ImportError:
            import main as app
        app.main(cmd)


if __name__ == '__main__':
    main()
