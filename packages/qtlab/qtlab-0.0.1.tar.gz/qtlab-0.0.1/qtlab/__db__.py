#!/usr/bin/python3
DEFAULT = \
{
    "hsp": {
        "s1Line": "Acetonitrile",
        "s2Line": "",
        "targetS1VolBox": 100,
        "targetS2VolBox": 0,
        "dTargetBox": 0.0,
        "pTargetBox": 0.0,
        "hTargetBox": 0.0,
        "dTargetEnableBox": True,
        "pTargetEnableBox": True,
        "hTargetEnableBox": True,
        "groupPreferedBox": True,
        "groupUsableBox": False,
        "groupHazardousBox": False,
        "groupCustomBox": False,
        "filterAllBox": True,
        "filterSingleBox": False,
        "filterDualBox": False,
        "filterTripleBox": False,
    },
    "calc": {
        "molConcCombo": "millimolar (mM)",
        "molVolCombo": "milliliters (mL)",
        "dilC1Combo": "",
        "dilC2Combo": "",
        "dilV2Combo": "",
        "dilResultCombo": "milliliters (mL)",
        "notes": "μ°∙Å¢αβλΔδ™",
        "copyFormatLine": "TODO",
        "copyClipboardBox": True,
        "copyNotesBox": True,
        "escapeKeyBox": True,
        "displayFormulaBox": False,
    },
    "peak": {
        "autodetect": True,
        "last profile": "Cary WinUV (v3)",
        "profiles":
        {
            "Cary WinUV (v3)":
            {
                "focusBox": True,
                "statsBox": True,
                "focusMinBox": 500,
                "focusMaxBox": 800,
                "statsMinBox": 500,
                "statsMaxBox": 800,
                "xLine": "Wavelength (nm)",
                "yLine": "Absorbance",
                "titleStatsLine": "Sample",
                "xStatsLine": "λmax (nm)",
                "yStatsLine": "λmax (abs)",
                "output path": "",
                "input path": "",
            },
            "OMNIC for Dispertive Raman (v8)":
            {
                "focusBox": False,
                "statsBox": False,
                "focusMinBox": 0,
                "focusMaxBox": 0,
                "statsMinBox": 0,
                "statsMaxBox": 0,
                "xLine": "Raman shift (cm-1)",
                "yLine": "Intensity",
                "titleStatsLine": "Sample",
                "xStatsLine": "λmax (cm-1)",
                "yStatsLine": "λmax (intensity)",
                "output path": "",
                "input path": "",
            }
        }
    },
}

