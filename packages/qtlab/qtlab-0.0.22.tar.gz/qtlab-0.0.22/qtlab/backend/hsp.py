#!/usr/bin/python3
import json
import math
from pathlib import Path
from itertools import combinations

try:
    from ..__id__ import ID
except ValueError:
    from __id__ import ID

SLV_FILE = Path.home() / ".config" / ID / "hsp_solvents.json"
GRP_FILE = Path.home() / ".config" / ID / "hsp_groups.json"


def combine(s1, s2, s3=None):
    if s3:
        s3_dD = s3["vol"]*s3["dD"]
        s3_dP = s3["vol"]*s3["dP"]
        s3_dH = s3["vol"]*s3["dH"]
    else:
        s3_dD, s3_dP, s3_dH = 0, 0, 0

    # dX = (a*dX1 + b*dX2) / (a+b)
    blend = {}
    blend["dD"] = (s1["vol"]*s1["dD"] + s2["vol"]*s2["dD"] + s3_dD) / 100
    blend["dP"] = (s1["vol"]*s1["dP"] + s2["vol"]*s2["dP"] + s3_dP) / 100
    blend["dH"] = (s1["vol"]*s1["dH"] + s2["vol"]*s2["dH"] + s3_dH) / 100
    return blend


def dph(target):
    with open(SLV_FILE, "r") as f:
        db = json.load(f)
    if target in db:
        return db[target]
    return None


class HSP():
    def __init__(self):
        self.abort = False
        self.reset()

    def _data_format(self, data):
        try:
            return "%.2f" % data
        except TypeError:
            pass
        return data

    def _distance(self, s1, s2, dph):
        dD, dP, dH = 0, 0, 0
        if dph[0]:
            dD = 4*(s1["dD"]-s2["dD"])**2
        if dph[1]:
            dP = (s1["dP"]-s2["dP"])**2
        if dph[2]:
            dH = (s1["dH"]-s2["dH"])**2

        ra = math.sqrt(dD + dP + dH)  # Ra^2 = {4*(dD1-dD2)^2 + (dP1-dP2)^2 +(dH1-dH2)^2}
        return round(ra, 2)

    def _single(self, target, dph):
        solvents = {}
        for name in self.available:
            if self.abort: return {}
            s = self.available[name]
            ra = self._distance(s, target, dph)
            solvents[name] = {"dD": s["dD"], "dP": s["dP"], "dH": s["dH"], "Ra": ra, "s1": name}

        for slv in solvents:
            for attr in solvents[slv]:
                value = self._data_format(solvents[slv][attr])
                solvents[slv][attr] = value
        return solvents

    def _dual(self, target, dph):
        solvents = {}
        for names in combinations(self.available, 2):
            if self.abort: return {}
            s1, s2 = names
            s1, s2 = self.available[s1], self.available[s2]
            s1["name"], s2["name"] = names
            results = {}

            for vol in range(0, 101, 1):
                s1["vol"] = 100 - vol
                s2["vol"] = 100 - s1["vol"]
                blend = combine(s1, s2)
                ra = self._distance(blend, target, dph)
                results[ra] = {"dD": blend["dD"], "dP": blend["dP"], "dH": blend["dH"], "Ra": ra,
                                    "s1": s1["name"], "s2": s2["name"], "ratio": (s1["vol"], s2["vol"])}

            best = results[min(results)]
            for key in best:
                value = self._data_format(best[key])
                best[key] = value
            key = (s1["name"], s2["name"])
            solvents[key] = best
        solvents = self._sort_dual(solvents)
        return solvents

    def _triple(self, target, dph):
        solvents = {}
        for names in combinations(self.available, 3):
            if self.abort: return {}
            s1, s2, s3 = names
            s1, s2, s3 = self.available[s1], self.available[s2], self.available[s3]
            s1["name"], s2["name"], s3["name"] = names
            results = {}

            for prop in [(i, 100-i-k, k) for i in range(1,99) for k in range(1,100-i)]:
                s1["vol"], s2["vol"], s3["vol"] = prop
                blend = combine(s1, s2, s3)
                ra = self._distance(blend, target, dph)
                results[ra] = {"dD": blend["dD"], "dP": blend["dP"], "dH": blend["dH"], "Ra": ra,
                                    "s1": s1["name"], "s2": s2["name"], "s3": s3["name"],
                                    "ratio": (s1["vol"], s2["vol"], s3["vol"])}

            best = results[min(results)]
            for key in best:
                value = self._data_format(best[key])
                best[key] = value
            key = (s1["name"], s2["name"], s3["name"])
            solvents[key] = best
        solvents = self._sort_triple(solvents)
        return solvents

    def _sort_dual(self, solvents):
        for s in dict(solvents):
            slv = solvents[s]
            r1, r2 = slv["ratio"]
            if r1 < r2:
                r1, r2 = r2, r1
                slv["s1"], slv["s2"] = slv["s2"], slv["s1"]
            slv["ratio"] = (r1, r2)

            if r1 > 98:
                del solvents[s]
        return solvents

    def _sort_triple(self, solvents):
        for s in dict(solvents):
            slv = solvents[s]
            r1, r2, r3 = slv["ratio"]

            for i in range(2):
                if r1 < r2:
                    r1, r2 = r2, r1
                    slv["s1"], slv["s2"] = slv["s2"], slv["s1"]
                if r2 < r3:
                    r2, r3 = r3, r2
                    slv["s2"], slv["s3"] = slv["s3"], slv["s2"]
            slv["ratio"] = (r1, r2, r3)

            if r3 <= 2:
                del solvents[s]
        return solvents

    def _updateGroups(self, selected_groups):
        with open(SLV_FILE, "r") as f:
            db = json.load(f)

        with open(GRP_FILE, "r") as f:
            groups = json.load(f)

        self.available = {}
        for grp in selected_groups:
            for slv in groups[grp]:
                if slv in db:
                    self.available[slv] = db[slv]

    def reset(self):
        self.all, self.single, self.dual, self.triple = {}, {}, {}, {}

    def search(self, scope, dph, target, groups):
        self._updateGroups(groups)
        if scope in ("single", "all"):
            self.single = self._single(target, dph)
        if scope in ("dual", "all"):
            self.dual = self._dual(target, dph)
        if scope in ("triple", "all"):
            self.triple = self._triple(target, dph)
        self.all = {**self.single, **self.dual, **self.triple}
        self.abort = False
