import win32com.client
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import QThread, pyqtSignal

from .ui.Grid import Ui_Form


class Surfer:
    def __init__(self):
        self.app = None
        self.Version = None
        self.dispatch()

    def dispatch(self):
        try:
            self.app = win32com.client.gencache.EnsureDispatch("Surfer.Application")
            self.Version = self.app.Version
        except Exception as e:
            # 如果创建 COM 对象时发生异常，打印错误消息
            print("无法绑定 COM 对象:", str(e))


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
