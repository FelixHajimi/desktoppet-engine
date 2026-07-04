from PySide6 import QtCore, QtGui, QtWidgets

class Template:
    def __init__(self):
        self.__autoStart__ = False

    def enter(self, image, mainTimer, physicsTimer, state, window):
        self.__image__ = image
        self.__mainTimer__ = mainTimer
        self.__physicsTimer__ = physicsTimer
        self.__state__ = state
        self.__window__ = window

    def loadMovie(self, path: str):
        """切换桌宠动画"""
        if self.__image__.fileName() != path:
            self.__image__.setFileName(path)
            self.__image__.jumpToFrame(0)
        self.__image__.start()


class Information(Template):
    def enter(self, image, mainTimer, physicsTimer, state, window):
        super().enter(image, mainTimer, physicsTimer, state, window)
        QtWidgets.QMessageBox.information(window, "消息", "这是一条提示消息")


class Question(Template):
    def enter(self, image, mainTimer, physicsTimer, state, window):
        super().enter(image, mainTimer, physicsTimer, state, window)
        QtWidgets.QMessageBox.question(window, "问题", "确定要执行此操作吗？")


class Warning(Template):
    def enter(self, image, mainTimer, physicsTimer, state, window):
        super().enter(image, mainTimer, physicsTimer, state, window)
        QtWidgets.QMessageBox.warning(window, "警告", "这是一个警告信息")


class Error(Template):
    def enter(self, image, mainTimer, physicsTimer, state, window):
        super().enter(image, mainTimer, physicsTimer, state, window)
        QtWidgets.QMessageBox.critical(window, "错误", "发生了一个错误")


pluginName = "弹窗消息"

menu = {
    "消息": Information(),
    "问题": Question(),
    "警告": Warning(),
    "错误": Error()
}
