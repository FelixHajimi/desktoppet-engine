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

    def loadMovie(self, path: str):
        if self.__image__.fileName() != path:
            self.__image__.setFileName(path)
            self.__image__.jumpToFrame(0)
        self.__image__.start()


class Information(Template):
    def __init__(self):
        super().__init__()

    def enter(
        self,
        image: QtGui.QMovie,
        mainTimer: QtCore.QTimer,
        physicsTimer: QtCore.QTimer,
        state: dict,
        window: QtWidgets.QWidget,
    ):
        super().enter(image, mainTimer, physicsTimer, state, window)
        QtWidgets.QMessageBox.information(window, "消息", "消息正文")


class Question(Template):
    def __init__(self):
        super().__init__()

    def enter(
        self,
        image: QtGui.QMovie,
        mainTimer: QtCore.QTimer,
        physicsTimer: QtCore.QTimer,
        state: dict,
        window: QtWidgets.QWidget,
    ):
        super().enter(image, mainTimer, physicsTimer, state, window)
        QtWidgets.QMessageBox.question(window, "问题", "问题正文")


class Warning(Template):
    def __init__(self):
        super().__init__()

    def enter(
        self,
        image: QtGui.QMovie,
        mainTimer: QtCore.QTimer,
        physicsTimer: QtCore.QTimer,
        state: dict,
        window: QtWidgets.QWidget,
    ):
        super().enter(image, mainTimer, physicsTimer, state, window)
        QtWidgets.QMessageBox.warning(window, "警告", "警告正文")


class Error(Template):
    def __init__(self):
        super().__init__()

    def enter(
        self,
        image: QtGui.QMovie,
        mainTimer: QtCore.QTimer,
        physicsTimer: QtCore.QTimer,
        state: dict,
        window: QtWidgets.QWidget,
    ):
        super().enter(image, mainTimer, physicsTimer, state, window)
        QtWidgets.QMessageBox.critical(window, "错误", "错误正文")


menu = {"消息": Information(), "问题": Question(), "警告": Warning(), "错误": Error()}
pluginName = "弹窗消息"
