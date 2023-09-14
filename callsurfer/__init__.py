from .CallSurfer import CallSurferPlugin


def classFactory(iface):
    """QGIS Plugin"""
    return CallSurferPlugin(iface)
