from PySide6 import QtCore, QtGui, QtWidgets


class Template:
    def __init__(self):
        self.__autoStart__ = False

    def enter(
        self,
        image: QtGui.QMovie,
        mainTimer: QtCore.QTimer,
        physicsTimer: QtCore.QTimer,
        state: dict,
        window: QtWidgets.QWidget,
    ):
        self.__image__ = image
        self.__mainTimer__ = mainTimer
        self.__physicsTimer__ = physicsTimer
        self.__state__ = state
        self.__window__ = window

    def loadMovie(self, path: str):
        if self.__image__.fileName() != path:
            self.__image__.setFileName(path)
            self.__image__.jumpToFrame(0)
        self.__image__.start()


menu = {}
pluginName = "模板"
