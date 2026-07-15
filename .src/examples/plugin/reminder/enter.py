from PySide6 import QtCore, QtGui, QtWidgets
import random


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


class Reminder(Template):
    def __init__(self):
        super().__init__()
        self._autoStart = True

    def activate(self, state):
        super().activate(state)
        print("提醒插件已加载！")

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.show_reminder)
        self.timer.start(2160000)
        state["$reminder"]["reminder_timer"] = self.timer

    def deactivate(self):
        super().deactivate()
        del self.timer

    def show_reminder(self):
        messages = ["该休息一下了！", "起来走动走动！", "喝口水吧！"]
        QtWidgets.QMessageBox.information(self._window, "提醒", random.choice(messages))


class StopReminder(Template):
    def activate(self, state):
        super().activate(state)
        if "reminder_timer" in state:
            state["$reminder"]["reminder_timer"].stop()
            state["$reminder"]["reminder_timer"].deleteLater()
            del state["$reminder"]
            print("提醒已关闭")


pluginName = "定时提醒"

menu = {
    "_type": "/",
    "开启提醒": {"_type": "$", "_activate": Reminder()},
    "关闭提醒": {"_type": "$", "_activate": StopReminder()},
}
