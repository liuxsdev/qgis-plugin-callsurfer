import pandas as pd
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import QThread, pyqtSignal
from qgis.PyQt.QtWidgets import QTableWidgetItem, QHeaderView
from qgis.core import QgsMapLayerProxyModel

from .pySurfer import Surfer, SrfGridAlgorithm
from .ui.Grid import Ui_Form
from .utils import Project_DIR


class CheckSurfer(QThread):
    check_finished = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        app = Surfer()
        self.check_finished.emit(app.Version)


def get_extent(data):
    return {
        "xmin": min(data["x"]),
        "xmax": max(data["x"]),
        "ymin": min(data["y"]),
        "ymax": max(data["y"]),
    }


class GridDialog(QtWidgets.QDialog, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.app = None
        self.grid_data = None
        self.check_surfer = None
        self.project_dir = Project_DIR
        self.initUI()

    def initUI(self):
        self.check_surfer_version()
        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.mMapLayerComboBox.layerChanged.connect(self.set_layer)
        self.pushButton.clicked.connect(self.show_info)
        self.pushButton_2.clicked.connect(self.make_grid)
        print(SrfGridAlgorithm.srfKriging.value)
        self.set_layer()

    def set_layer(self):
        pl = self.mMapLayerComboBox.currentLayer()
        self.mFieldComboBox.setLayer(pl)

    def init_surfer(self):
        self.app = Surfer()

    def show_info(self):
        pl = self.mMapLayerComboBox.currentLayer()
        fd = self.mFieldComboBox.currentField()
        features = list(pl.getFeatures())
        self.grid_data = {
            "x": [f.geometry().asPoint().x() for f in features],
            "y": [f.geometry().asPoint().y() for f in features],
            "z": [f.attribute(fd) for f in features],
        }
        self.fill_data_table(self.grid_data)
        df = pd.DataFrame(self.grid_data)
        df.to_csv(
            self.project_dir.joinpath("grid_data.csv"), index=False
        )  # TODO: seve to plugin dir ,after close dialog remove it.

    def set_surfer(self, version: str):
        if version is not None:
            self.label_surfer_connect_status.setText(f"Connected to Surfer {version}")
            self.init_surfer()
        else:
            self.label_surfer_connect_status.setText("Filed to connect Surfer")

    def check_surfer_version(self):
        self.label_surfer_connect_status.setText("Connecting")
        self.check_surfer = CheckSurfer()
        self.check_surfer.check_finished.connect(self.set_surfer)
        self.check_surfer.start()

    def toggle(self):
        # TODO toogle surfer window
        self.app.Visible = True

    def fill_data_table(self, data):
        self.data_tableWidget.clear()
        row_count = len(data.get("x"))
        self.data_tableWidget.setRowCount(row_count)
        self.data_tableWidget.setColumnCount(3)
        self.data_tableWidget.setHorizontalHeaderLabels(
            [x.upper() for x in data.keys()]
        )
        self.data_tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        for row in range(row_count):
            x = data["x"][row]
            item_x = QTableWidgetItem(str(x))
            self.data_tableWidget.setItem(row, 0, item_x)
            y = data["y"][row]
            item_y = QTableWidgetItem(str(y))
            self.data_tableWidget.setItem(row, 1, item_y)
            z = data["z"][row]
            item_z = QTableWidgetItem(str(z))
            self.data_tableWidget.setItem(row, 2, item_z)
        self.data_tableWidget.resizeRowsToContents()

    def make_grid(self):
        self.app.grid(
            self.project_dir.joinpath("grid_data.csv"),
            algorithm=SrfGridAlgorithm.srfKriging.value,
            extend=get_extent(self.grid_data),
        )

    def load_grd(self):
        pass
