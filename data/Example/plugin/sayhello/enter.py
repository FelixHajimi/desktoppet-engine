import logging
import os

from PySide6 import QtCore, QtGui, QtWidgets

pluginName = "Template"

PATH = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")


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
        """
        这是用来创建插件的模板
        发挥你的想象力！
        This is a template for creating plugins.
        Use your imagination!
        """
        self.__image__ = image

    def loadMovie(self, path: str):
        if self.__image__.fileName() != path:
            self.__image__.setFileName(path)
            self.__image__.jumpToFrame(0)
        self.__image__.start()


class Test(Template):
    def __init__(self):
        super().__init__()

    def enter(self, image, mainTimer, physicsTimer, state, window):
        super().enter(image, mainTimer, physicsTimer, state, window)
        logging.info("Hello My DesktopPet!")
        QtWidgets.QMessageBox.information(window, "Info", "Hello My DesktopPet!")


menu = {"Template": Test()}
