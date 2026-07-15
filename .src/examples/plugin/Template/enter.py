from PySide6 import QtCore, QtGui, QtWidgets
import os

PATH = os.path.dirname(__file__)

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


menu = {"_type": "/"}
pluginName = "模板"
