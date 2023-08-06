#!/usr/bin/python3
import json

units_val = \
{
    "molar (M)": 1,
    "millimolar (mM)": 10**3,
    "micromolar (μM)": 10**6,
    "nanomolar (nM)": 10**9,
    "picomolar (pM)": 10**12,
    "liters (L)": 1,
    "milliliters (mL)": 10**3,
    "microliters (μL)": 10**6,
}

units_str = \
{
    "molar (M)": "M",
    "millimolar (mM)": "mM",
    "micromolar (μM)": "μM",
    "nanomolar (nM)": "nM",
    "picomolar (pM)": "pM",
    "liters (L)": "L",
    "milliliters (mL)": "mL",
    "microliters (μL)": "μL",
}

MINUS_ONE = f"\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}"


try:
    from ..__id__ import ID
except ValueError:
    from __id__ import ID


class Calc():
    def __init__(self):
        pass

    def dilution(self, c1, c1Factor, c2, c2Factor, v2, v2Unit, resultUnit):
        try:
            c1Factor = units_val[c1Factor]
            c2Factor = units_val[c2Factor]
            v2Factor = units_val[v2Unit]
            resultFactor = units_val[resultUnit]

            # v1 = (c2 * v2) / c1
            v1 = (((c2 / c2Factor) * v2) / (c1 / c1Factor)) * (resultFactor/v2Factor)
            return v1
        except ValueError:
            return 0
        except ZeroDivisionError:
            return 0

    def dilution_string(self, c1, c1Factor, c2, c2Factor, v2, v2Unit, resultUnit):
        if c1 and c2 and v2:
            c1Unit = units_str[c1Factor]
            c2Unit = units_str[c2Factor]
            c1Factor = units_val[c1Factor]
            c2Factor = units_val[c2Factor]
            v2Factor = units_val[v2Unit]
            resultFactor = units_val[resultUnit]
            v2UnitStr = units_str[v2Unit]
            resultUnitStr = units_str[resultUnit]

            if c2Unit == "M":
                term_1st = f"({c2}{c2Unit} * {v2}{v2UnitStr})"
            else:
                term_1st = f"({c2}{c2Unit} / {c2Factor}{c2Unit}∙M{MINUS_ONE}) * {v2}{v2UnitStr})"

            if c1Unit == "M":
                term_2nd = f"{c1}{c1Unit}"
            else:
                term_2nd = f"({c1}{c1Unit} / {c1Factor}{c1Unit}∙M{MINUS_ONE})"

            if v2Factor == resultFactor:
                vol_str = f"({term_1st} / {term_2nd}"
            else:
                term_3rd = f"({resultFactor}{resultUnitStr} / {v2Factor}{v2UnitStr})"
                vol_str = f"(({term_1st} / {term_2nd}) * {term_3rd}"

            return vol_str
        return ""

    def molar_solution(self, mw, conc, concFactor, vol, volUnit):
        try:
            concFactor = units_val[concFactor]
            volUnit = units_val[volUnit]
            mass = mw * (conc / concFactor) * (vol / volUnit)
            return mass
        except ValueError:
            return 0

    def molar_string(self, mw, conc, concFactor, vol, volUnit):
        if mw and conc and vol:
            concUnit = units_str[concFactor]
            volUnitStr = units_str[volUnit]
            concFactor = units_val[concFactor]
            volUnit = units_val[volUnit]

            if concUnit == "M":
                term_1st = f"{conc}{concUnit}"
            else:
                term_1st = f"({conc}{concUnit} / {concFactor}{concUnit}∙M{MINUS_ONE})"

            if volUnitStr == "L":
                term_2nd = f"{vol}{volUnitStr}"
            else:
                term_2nd = f"({vol}{volUnitStr} / {volUnit}{volUnitStr}∙L{MINUS_ONE})"

            mass_str = f"{mw}g∙mol{MINUS_ONE} * {term_1st} * {term_2nd}"
            return mass_str
        return ""
