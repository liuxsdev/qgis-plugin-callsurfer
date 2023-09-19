import pandas as pd
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import QThread, pyqtSignal
from qgis.PyQt.QtWidgets import QTableWidgetItem, QHeaderView
from qgis.core import QgsMapLayerProxyModel

from .pySurfer import Surfer
from .ui.Grid import Ui_Form


class CheckSurfer(QThread):
    check_finished = pyqtSignal(Surfer)

    def __init__(self):
        super().__init__()

    def run(self):
        app = Surfer()
        self.check_finished.emit(app)


class GridDialog(QtWidgets.QDialog, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.app = None
        self.check_surfer = None
        self.connect_surfer()
        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.set_layer()
        self.mMapLayerComboBox.layerChanged.connect(self.set_layer)
        self.pushButton.clicked.connect(self.show_info)

    def set_layer(self):
        pl = self.mMapLayerComboBox.currentLayer()
        self.mFieldComboBox.setLayer(pl)

    def show_info(self):
        pl = self.mMapLayerComboBox.currentLayer()
        fd = self.mFieldComboBox.currentField()
        features = list(pl.getFeatures())
        data = {
            "x": [f.geometry().asPoint().x() for f in features],
            "y": [f.geometry().asPoint().y() for f in features],
            "z": [f.attribute(fd) for f in features],
        }
        print(data)
        self.fill_data_table(data)
        df = pd.DataFrame(data)
        df.to_csv(
            "data11.csv", index=False
        )  # TODO: seve to plugin dir ,after close dialog remove it.

    def set_surfer(self, app: Surfer):
        self.app = app
        if self.app.Version is not None:
            self.label_surfer_connect_status.setText(
                f"Connected to Surfer {self.app.Version}"
            )
        else:
            self.label_surfer_connect_status.setText("Filed to connect Surfer")

    def connect_surfer(self):
        self.label_surfer_connect_status.setText("Connecting")
        self.check_surfer = CheckSurfer()
        self.check_surfer.check_finished.connect(self.set_surfer)
        self.check_surfer.start()

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
