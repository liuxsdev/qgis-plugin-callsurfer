from pathlib import Path

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from .grid_dialog import GridDialog

Plugin_DIR = Path(__file__).parent


class CallSurferPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.toolbar = self.iface.addToolBar("Call Surfer Toolbar")
        self.action = None
        self.initGui()

    def initGui(self):
        self.action = QAction(
            QIcon(str(Plugin_DIR.joinpath("images/icon.png"))),
            "Surfer",
        )
        self.action.triggered.connect(self.open)
        self.toolbar.addAction(self.action)

    def open(self):
        dlg = GridDialog()
        dlg.show()
        dlg.exec_()

    def unload(self):
        """Unload from the QGIS interface"""
        self.iface.removeToolBarIcon(self.action)
