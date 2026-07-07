## Plugin Development Guide

---

### Overview

The desktop pet engine supports extending functionality through plugins. Each plugin is an independent folder containing an `enter.py` entry file.

Plugins can add right-click menu items, and when a menu item is clicked, its corresponding logic is executed. Plugins can also be set to run automatically on startup.

---

### Directory Structure

```
data/
└── pet_name/
    ├── config.json          # Pet configuration
    ├── plugin/              # Plugin directory
    │   └── [plugin_name]/   # Individual plugin folder
    │       └── enter.py     # Plugin entry file (required)
    └── res/                 # Pet resources
```

---

### Enabling Plugins

In the pet's `config.json`, declare the plugins to load via the `plugin` field:

```json
{
  "name": "Example",
  "version": "1.0.0",
  "author": "YourName",
  "acc": [0, 1.2],
  "fri": {
    "top": 2,
    "bottom": 3,
    "left": 0,
    "right": 0
  },
  "ela": {
    "top": 0,
    "bottom": 5,
    "left": 10,
    "right": 10
  },
  "plugin": ["message", "reminder"]
}
```

Each string in the `plugin` array corresponds to a plugin folder name under the `plugin/` directory.

---

### Plugin Entry File (enter.py)

Each plugin must contain an `enter.py` file with the following definitions:

#### 1. `pluginName` (Required)

The display name of the plugin, which appears as the submenu title in the right-click menu.

```python
pluginName = "Message Popup"
```

#### 2. `menu` Dictionary (Required)

Defines the right-click menu items. Each key is the menu display name, and each value is an object instance. When a user clicks a menu item, the main program calls that object's `enter` method.

```python
menu = {
    "Information": Information(),
    "Question": Question(),
    "Warning": Warning(),
    "Error": Error()
}
```

#### 3. `enter` Method (Required)

Each menu item class must implement the `enter` method, which is called when the user clicks the menu item:

```python
def enter(self, image, mainTimer, physicsTimer, state, window):
    """
    Callback method called when the menu item is clicked

    Parameters:
        image: QMovie object for controlling pet animation
        mainTimer: QTimer object for the main loop (20ms)
        physicsTimer: QTimer object for the physics loop (20ms)
        state: dict, pet state dictionary (read/write)
        window: QWidget object, the main window
    """
    pass
```

#### 4. `_autoStart` Attribute (Optional)

Define the `_autoStart` attribute in the class to control whether the `enter` method is automatically executed when the program starts:

```python
class Information(Template):
    def _init(self):
        super().__init__()
        self._autoStart = True  # Auto-execute on startup
```

---

### Complete Example: Message Popup Plugin

```python
from PySide6 import QtCore, QtGui, QtWidgets

# Base template class
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
        """Switch pet animation"""
        if self._image.fileName() != path:
            self._image.setFileName(path)
            self._image.jumpToFrame(0)
        self._image.start()


# Specific functionality classes
class Information(Template):
    def enter(self, image, mainTimer, physicsTimer, state, window):
        super().enter(image, mainTimer, physicsTimer, state, window)
        QtWidgets.QMessageBox.information(window, "Information", "This is an info message")


class Question(Template):
    def enter(self, image, mainTimer, physicsTimer, state, window):
        super().enter(image, mainTimer, physicsTimer, state, window)
        QtWidgets.QMessageBox.question(window, "Question", "Are you sure you want to proceed?")


class Warning(Template):
    def enter(self, image, mainTimer, physicsTimer, state, window):
        super().enter(image, mainTimer, physicsTimer, state, window)
        QtWidgets.QMessageBox.warning(window, "Warning", "This is a warning message")


class Error(Template):
    def enter(self, image, mainTimer, physicsTimer, state, window):
        super().enter(image, mainTimer, physicsTimer, state, window)
        QtWidgets.QMessageBox.critical(window, "Error", "An error has occurred")


# Plugin metadata (required)
pluginName = "Message Popup"

menu = {
    "Information": Information(),
    "Question": Question(),
    "Warning": Warning(),
    "Error": Error()
}
```

---

### Plugin with **autoStart** Example

```python
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
        self._autoStart = True  # Auto-execute on startup

    def enter(self, image, mainTimer, physicsTimer, state, window):
        super().enter(image, mainTimer, physicsTimer, state, window)
        print("Reminder plugin loaded!")

        # Start a timer that shows a reminder every 30 seconds
        timer = QtCore.QTimer()
        timer.timeout.connect(self.show_reminder)
        timer.start(30000)
        self._state["reminder_timer"] = timer

    def show_reminder(self):
        messages = ["Time for a break!", "Get up and stretch!", "Have some water!"]
        QtWidgets.QMessageBox.information(
            self._window,
            "Reminder",
            random.choice(messages)
        )


class StopReminder(Template):
    def enter(self, image, mainTimer, physicsTimer, state, window):
        super().enter(image, mainTimer, physicsTimer, state, window)
        if "reminder_timer" in state:
            state["reminder_timer"].stop()
            state["reminder_timer"].deleteLater()
            del state["reminder_timer"]
            print("Reminder stopped")


# Plugin metadata (required)
pluginName = "Timer Reminder"

menu = {
    "Start Reminder": Reminder(),
    "Stop Reminder": StopReminder()
}
```

---

### Plugin with State Update Example

If you need to execute logic every frame, you can register a function with `state["update"]`:

```python
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


class AutoMove(Template):
    def __init__(self):
        super()._init()
        self._autoStart = True

    def enter(self, image, mainTimer, physicsTimer, state, window):
        super().enter(image, mainTimer, physicsTimer, state, window)

        def update():
            # Executes every frame: makes the pet swing left and right
            import math
            time = QtCore.QDateTime.currentMSecsSinceEpoch() / 1000
            state["motion"][0] = math.sin(time) * 2
            state["motion"][1] = -1

        state["update"]["auto_move"] = update


pluginName = "Auto Motion"

menu = {
    "Enable Auto Motion": AutoMove()
}
```
