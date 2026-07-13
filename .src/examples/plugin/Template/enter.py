from PySide6 import QtCore, QtGui, QtWidgets


class Template:
    def __init__(self):
        self._autoStart = False

    def enter(
        self,
        image: QtGui.QMovie,
        mainTimer: QtCore.QTimer,
        physicsTimer: QtCore.QTimer,
        state: dict,
        window: QtWidgets.QWidget,
    ):
        self._image = image
        self._mainTimer = mainTimer
        self._physicsTimer = physicsTimer
        self._state = state
        self._window = window

    def loadMovie(self, path: str):
        if self._image.fileName() != path:
            self._image.setFileName(path)
            self._image.jumpToFrame(0)
        self._image.start()


menu = {}
pluginName = "模板"
