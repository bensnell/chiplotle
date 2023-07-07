from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()
from chiplotle.plotters.drawingplotter import _DrawingPlotter


class HP7570A(_DrawingPlotter):
    def __init__(self, ser, **kwargs):
        ## allowedHPGLCommands must be set prior to base class init.
        self.allowedHPGLCommands = (
            "\x1b.",
            "AA",
            "AP",
            "AR",
            "CA",
            "CI",
            "CP",
            "CS",
            "CT",
            "DC",
            "DF",
            "DI",
            "DP",
            "DR",
            "DT",
            "DV", # Same as DL.
            "EA",
            "EP",
            "ER",
            "ES",
            "EW",
            "FP",
            "FT",
            "GC", # Same as GM, GP; however, HP7570A may only recognize GM.
            "IM",
            "IN",
            "IP",
            "IW",
            "LB",
            "LO",
            "LT",
            "NR",
            "OA",
            "OC",
            "OD",
            "OE",
            "OF",
            "OH",
            "OI",
            "OO",
            "OP",
            "OS",
            "OT",
            "OW",
            "PA",
            "PD",
            "PM",
            "PR",
            "PT",
            "PU",
            "RA",
            "RO",
            "RR",
            "SA",
            "SC",
            "SS", # Same as SG, but HP7570A may only recognize SG.
            "SI",
            "SL",
            "SM",
            "SP",
            "SR",
            "SS",
            "TL",
            "UC",
            "VS",
            "WG",
            "XT",
            "YT",
        )

        _DrawingPlotter.__init__(self, ser, **kwargs)
        self.type = "HP7570A"
