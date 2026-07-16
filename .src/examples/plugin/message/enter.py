from PySide6 import QtCore, QtGui, QtWidgets


class Template:
    def __init__(self):
        self._autoStart = False

    def init(self, image, mainTimer, physicsTimer, window):
        self._image = image
        self._mainTimer = mainTimer
        self._physicsTimer = physicsTimer
        self._window = window

    def activate(self, state):
        self._state = state

    def deactivate(self):
        pass

    def loadMovie(self, path: str):
        if self._image.fileName() != path:
            self._image.setFileName(path)
            self._image.jumpToFrame(0)
        self._image.start()


class Information(Template):
    def activate(self, state):
        super().activate(state)
        QtWidgets.QMessageBox.information(self._window, "消息", "消息正文")


class Question(Template):
    def activate(self, state):
        super().activate(state)
        QtWidgets.QMessageBox.question(self._window, "问题", "问题正文")


class Warning(Template):
    def activate(self, state):
        super().activate(state)
        QtWidgets.QMessageBox.warning(self._window, "警告", "警告正文")


class Error(Template):
    def activate(self, state):
        super().activate(state)
        QtWidgets.QMessageBox.critical(self._window, "错误", "错误正文")


pluginName = "弹窗消息"

menu = {
    "_type": "/",
    "消息": {"_type": "$", "_activate": Information()},
    "问题": {"_type": "$", "_activate": Question()},
    "警告": {"_type": "$", "_activate": Warning()},
    "错误": {"_type": "$", "_activate": Error()},
}
