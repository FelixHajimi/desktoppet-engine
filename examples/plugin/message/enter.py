from PySide6 import QtCore, QtGui, QtWidgets


class Template:
    def __init__(self):
        self._autoStart = False

    def enter(self, image, mainTimer, physicsTimer, state, window):
        self._image = image
        self._mainTimer = mainTimer
        self._physicsTimer = physicsTimer
        self._state = state
        self._window = window

    def loadMovie(self, path: str):
        """切换桌宠动画"""
        if self._image.fileName() != path:
            self._image.setFileName(path)
            self._image.jumpToFrame(0)
        self._image.start()


class Information(Template):
    def enter(self, image, mainTimer, physicsTimer, state, window):
        super().enter(image, mainTimer, physicsTimer, state, window)
        QtWidgets.QMessageBox.information(window, "消息", "消息正文")


class Question(Template):
    def enter(self, image, mainTimer, physicsTimer, state, window):
        super().enter(image, mainTimer, physicsTimer, state, window)
        QtWidgets.QMessageBox.question(window, "问题", "问题正文")


class Warning(Template):
    def enter(self, image, mainTimer, physicsTimer, state, window):
        super().enter(image, mainTimer, physicsTimer, state, window)
        QtWidgets.QMessageBox.warning(window, "警告", "警告正文")


class Error(Template):
    def enter(self, image, mainTimer, physicsTimer, state, window):
        super().enter(image, mainTimer, physicsTimer, state, window)
        QtWidgets.QMessageBox.critical(window, "错误", "错误正文")


pluginName = "弹窗消息"

menu = {
    "消息": Information(),
    "问题": Question(),
    "警告": Warning(),
    "错误": Error(),
}
