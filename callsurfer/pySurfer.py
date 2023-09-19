from enum import Enum

import win32com.client


class SrfGridAlgorithm(Enum):
    srfInverseDistance = 1
    srfKriging = 2
    srfMinCurvature = 3
    srfShepards = 4
    srfNaturalNeighbor = 5
    srfNearestNeighbor = 6
    srfRegression = 7
    srfRadialBasis = 8
    srfTriangulation = 9
    srfMovingAverage = 10
    srfDataMetrics = 11
    srfLocalPolynomial = 12


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
