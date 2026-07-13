from PySide6 import QtCore, QtGui, QtWidgets
import random

class Template:
    def __init__(self):
        self._autoStart = False

    def enter(self, image, mainTimer, physicsTimer, state, window):
        self._image = image
        self._mainTimer = mainTimer
        self._physicsTimer = physicsTimer
        self._state = state
        self._window = window


class Reminder(Template):
    def __init__(self):
        super().__init__()
        self._autoStart = True

    def enter(self, image, mainTimer, physicsTimer, state, window):
        super().enter(image, mainTimer, physicsTimer, state, window)
        print("提醒插件已加载！")
        
        timer = QtCore.QTimer()
        timer.timeout.connect(self.show_reminder)
        timer.start(2160000)
        self._state["reminder_timer"] = timer

    def show_reminder(self):
        messages = ["该休息一下了！", "起来走动走动！", "喝口水吧！"]
        QtWidgets.QMessageBox.information(
            self._window, 
            "提醒", 
            random.choice(messages)
        )


class StopReminder(Template):
    def enter(self, image, mainTimer, physicsTimer, state, window):
        super().enter(image, mainTimer, physicsTimer, state, window)
        if "reminder_timer" in state:
            state["reminder_timer"].stop()
            state["reminder_timer"].deleteLater()
            del state["reminder_timer"]
            print("提醒已关闭")


pluginName = "定时提醒"

menu = {
    "开启提醒": Reminder(),
    "关闭提醒": StopReminder()
}
