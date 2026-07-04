import json
import logging
import pprint
import sys
from dataclasses import dataclass, field
from importlib import util

from PySide6 import QtCore, QtGui, QtWidgets


# 创建菜单工具
# Create Menu Tool
def menuGenerate(master: QtWidgets.QWidget, structure: dict):
    menu = QtWidgets.QMenu(master)

    def func(mainMenu: QtWidgets.QMenu, structure: dict):
        for i in structure.keys():
            if i == "__type__":
                continue
            elif i == "__debug__":
                continue
            elif structure[i]["__type__"] == "command":
                command = QtGui.QAction(i, mainMenu)
                command.triggered.connect(structure[i]["__func__"])
                mainMenu.addAction(command)
            elif structure[i]["__type__"] == "sep":
                mainMenu.addSeparator()
            elif structure[i]["__type__"] == "menu":
                submenu = QtWidgets.QMenu(i, mainMenu)
                func(submenu, structure[i])
                mainMenu.addMenu(submenu)

    func(menu, structure)
    return menu


# 日志工具
# Log tool
def createLog(msg: str, level: int = 1, debug: bool = False):
    if debug:
        if level == 0:
            logging.debug(msg)
        if level == 1:
            logging.info(msg)
    if level == 2:
        logging.warning(msg)
    if level == 3:
        logging.error(msg)
    if level == 4:
        logging.critical(msg)


# 语言服务
# Language services
class Translate:
    def __init__(self, tran: dict[str, dict[str, str]], lang="en-us"):
        self.lang = lang
        self.tran = tran

    def run(self, key: str, fallback: str | None = None) -> str:
        if key in self.tran:
            if self.lang in self.tran[key]:
                return self.tran[key][self.lang]
            elif "en-us" in self.tran[key]:
                return self.tran[key]["en-us"]
            elif fallback is not None:
                return fallback
            else:
                return f'TRANSLATE ERROR: not found "{self.lang}" language and not found "en-us"'
        elif fallback is not None:
            return fallback
        else:
            return f'TRANSLATE ERROR: not found "{key}"'


# 配置类
# Configuration Class
@dataclass
class Setting:
    desktopPet: str
    dataDir: str
    desktoppetResourceDir: str
    pluginFileName: str
    pluginObjectEntry: str
    imageSize: list[int]
    language: str = "en-us"
    debug: bool = False
    logPath: str = "./last.log"


@dataclass
class DesktopPetConfig:
    name: str
    version: str
    author: str
    acc: list[float]
    fri: dict
    ela: dict
    plugin: list[str] = field(default_factory=list)


# 定义窗口
# Define Window
class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(config.name)
        self.setWindowIcon(
            QtGui.QIcon(f"{setting.dataDir}/{setting.desktopPet}/{setting.desktoppetResourceDir}/icon.gif")
        )
        self.setWindowFlags(
            QtCore.Qt.WindowType.WindowStaysOnTopHint
            | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        createLog(tran.run("window.complete"), debug=setting.debug)

        self.W, self.H = setting.imageSize
        self.nowMousePos = [0, 0]
        self.lastMousePos = [0, 0]
        self.position = [(screenWidth - self.W) // 2, screenHeight - self.H]
        self.motion = [0, 0]
        self.pause = False
        self.showBox = False

        self.mainTimer = QtCore.QTimer(self)
        self.mainTimer.timeout.connect(self.mainStep)
        self.mainTimer.start(20)

        self.physicsTimer = QtCore.QTimer(self)
        self.physicsTimer.timeout.connect(self.physicsStep)
        self.physicsTimer.start(20)

        self.desktopPet = QtWidgets.QLabel(self)
        self.desktopPet.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.desktopPet.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)
        self.desktopPet.mousePressEvent = self.MousePressEvent
        self.desktopPet.mouseMoveEvent = self.MouseMoveEvent
        self.desktopPet.mouseReleaseEvent = self.MouseReleaseEvent
        self.image = QtGui.QMovie()
        self.image.setScaledSize(QtCore.QSize(self.W, self.H))
        self.desktopPet.setMovie(self.image)
        self.desktopPet.resize(self.W, self.H)

        self.state = {
            "pause": False,
            "position": self.position,
            "motion": self.motion,
            "screenWidth": screenWidth,
            "screenHeight": screenHeight,
            "update": dict(),
        }
        createLog(tran.run("program.ready"), debug=setting.debug)

        # 自启动判断
        # Autostart judgment
        autostartFunctions = []
        for plugin in pluginList:
            for _displayName, entry in plugin.menu.items():

                def itemFunc(f=entry):
                    return lambda: getattr(f, setting.pluginObjectEntry)(
                        self.image,
                        self.mainTimer,
                        self.physicsTimer,
                        self.state,
                        self,
                    )

                if getattr(entry, "__autoStart__"):
                    autostartFunctions.append(itemFunc())
                    createLog(
                        eval(tran.run("program.plugin.autostart.add")),
                        debug=setting.debug,
                    )
        for func in autostartFunctions:
            try:
                func()
                createLog(
                    eval(tran.run("program.plugin.autostart.run")),
                    debug=setting.debug,
                )
            except Exception as error:  # noqa: F841
                createLog(
                    eval(tran.run("program.plugin.autostart.runError")),
                    3,
                    debug=setting.debug,
                )

    def loadMovie(self, path: str):
        # 加载动画
        # Loading animation
        if self.image.fileName() != path:
            self.image.setFileName(path)
            self.image.jumpToFrame(0)
        self.image.start()

    def mainStep(self):
        # 主时钟循环
        # Main clock loop
        self.pause = self.state["pause"]
        self.motion = self.state["motion"]
        self.position = self.state["position"]
        if not self.pause:
            if (
                abs(self.state["motion"][0]) <= config.acc[0]
                and abs(self.state["motion"][1]) <= config.acc[1]
            ):
                self.loadMovie(f"{setting.dataDir}/{setting.desktopPet}/{setting.desktoppetResourceDir}/stand.gif")
            else:
                self.loadMovie(f"{setting.dataDir}/{setting.desktopPet}/{setting.desktoppetResourceDir}/drop.gif")

        for func in self.state["update"].values():
            try:
                func()
            except Exception as error:  # noqa: F841
                createLog(
                    eval(tran.run("program.plugin.loopFunction.runError")),
                    3,
                    debug=setting.debug,
                )

        self.desktopPet.move(self.state["position"][0], self.state["position"][1])

    def physicsStep(self):
        # 物理时钟循环
        # Physical clock cycle
        config.ela = {"top": 0, "bottom": 0, "left": 0, "right": 0} | config.ela
        config.fri = {"top": 0, "bottom": 0, "left": 0, "right": 0} | config.fri

        # 重力模拟
        # Gravity simulation
        self.state["motion"][0] += config.acc[0]
        self.state["motion"][1] += config.acc[1]

        # 速度预处理
        # Speed preprocessing
        if self.state["motion"][0] > screenWidth - (self.state["position"][0] + self.W):
            self.state["motion"][0] = (-self.state["motion"][0]) * (
                config.ela["right"] / 100
            )
            self.state["position"][0] = screenWidth - self.W
        elif -self.state["motion"][0] > self.state["position"][0]:
            self.state["motion"][0] = (-self.state["motion"][0]) * (
                config.ela["left"] / 100
            )
            self.state["position"][0] = 0
        elif self.state["motion"][1] > screenHeight - (self.state["position"][1] + self.H):
            self.state["motion"][1] = (-self.state["motion"][1]) * (
                config.ela["bottom"] / 100
            )
            self.state["position"][1] = screenHeight - self.H
        elif -self.state["motion"][1] > self.state["position"][1]:
            self.state["motion"][1] = (-self.state["motion"][1]) * (
                config.ela["top"] / 100
            )
            self.state["position"][1] = 0

        # 摩擦力
        # Friction
        if self.state["position"][0] == 0:
            if abs(self.motion[1]) < config.fri["left"]:
                self.motion[1] = 0
            else:
                self.motion[1] += config.fri["left"] * ((-1) ** (self.motion[1] > 0))
        elif self.state["position"][0] == screenWidth - self.W:
            if abs(self.motion[1]) < config.fri["right"]:
                self.motion[1] = 0
            else:
                self.motion[1] += config.fri["right"] * ((-1) ** (self.motion[1] > 0))
        if self.state["position"][1] == 0:
            if abs(self.motion[0]) < config.fri["top"]:
                self.motion[0] = 0
            else:
                self.motion[0] += config.fri["top"] * ((-1) ** (self.motion[0] > 0))
        elif self.state["position"][1] == screenHeight - self.H:
            if abs(self.motion[0]) < config.fri["bottom"]:
                self.motion[0] = 0
            else:
                self.motion[0] += config.fri["bottom"] * ((-1) ** (self.motion[0] > 0))

        # 设置位置
        # Set position
        self.state["position"][0] += self.state["motion"][0]
        self.state["position"][1] += self.state["motion"][1]

    def MouseMoveEvent(self, event: QtGui.QMouseEvent):
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.state["position"] = [
                event.globalPosition().x() - self.mouseOffset[0],
                event.globalPosition().y() - self.mouseOffset[1],
            ]
            self.nowMousePos = [
                event.globalPosition().x(),
                event.globalPosition().y(),
            ]
            self.state["motion"] = [
                self.nowMousePos[0] - self.lastMousePos[0],
                self.nowMousePos[1] - self.lastMousePos[1],
            ]
            self.lastMousePos = self.nowMousePos

    def MousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.mouseOffset = [
                event.position().x(),
                event.position().y(),
            ]
            self.state["motion"] = [0, 0]
            self.desktopPet.setCursor(QtCore.Qt.CursorShape.ClosedHandCursor)
            self.physicsTimer.stop()
        elif event.button() == QtCore.Qt.MouseButton.RightButton:
            self.showMenu(event.globalPosition().toPoint())

    def MouseReleaseEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.desktopPet.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)
            self.physicsTimer.start(20)

    def showMenu(self, globalPos):
        # 右键菜单
        # Right-click menu
        menuDict = {
            tran.run("program.menu.exit"): {
                "__type__": "command",
                "__func__": self.close,
            },
            eval(tran.run("program.menu.about.title")): {
                "__type__": "command",
                "__func__": lambda: QtWidgets.QMessageBox.about(
                    self,
                    eval(tran.run("program.menu.about.title")),
                    eval(tran.run("program.menu.about.text")),
                ),
            },
        }
        createLog(tran.run("program.menu.complete"), debug=setting.debug)

        # 导入插件
        for plugin in pluginList:
            menuDict[plugin.pluginName] = {"__type__": "menu"}
            for displayName, entry in plugin.menu.items():

                def itemFunc(f=entry):
                    def _():
                        try:
                            getattr(f, setting.pluginObjectEntry)(
                                self.image,
                                self.mainTimer,
                                self.physicsTimer,
                                self.state,
                                self,
                            )
                        except Exception as error:  # noqa: F841
                            createLog(
                                eval(tran.run("program.plugin.function.runError")),
                                3,
                                debug=setting.debug,
                            )

                    return _

                menuDict[plugin.pluginName][displayName] = {
                    "__type__": "command",
                    "__func__": itemFunc(),
                }
                createLog(
                    eval(tran.run("program.plugin.function.add")),
                    debug=setting.debug,
                )

        if setting.debug:
            if self.showBox:
                menuDict[tran.run("program.menu.collisionBox")] = {
                    "__type__": "command",
                    "__func__": lambda: self.desktopPet.setStyleSheet(""),
                }
                self.showBox = False
            else:
                menuDict[tran.run("program.menu.collisionBox")] = {
                    "__type__": "command",
                    "__func__": lambda: self.desktopPet.setStyleSheet(
                        "border: 1px solid red;"
                    ),
                }
                self.showBox = True
            menuDict[tran.run("program.menu.outputParameter")] = {
                "__type__": "command",
                "__func__": lambda: createLog(
                    "\n" + pprint.pformat(globals(), 2, sort_dicts=False),
                    debug=setting.debug,
                ),
            }
        menu = menuGenerate(self, menuDict)
        menu.exec(globalPos)
        createLog(
            eval(tran.run("program.menu.show")),
            debug=setting.debug,
        )


# 导入数据
# Import Data
setting = Setting(**json.load(open("./setting.json", encoding="utf-8")))
config = DesktopPetConfig(
    **json.load(
        open(f"{setting.dataDir}/{setting.desktopPet}/config.json", encoding="utf-8")
    )
)

# 日志配置
# Log Configuration
logging.basicConfig(
    filename=f"{setting.logPath}",
    encoding="utf-8",
    level=logging.DEBUG,
    format="[%(levelname)s] <%(pathname)s> (%(asctime)s) - %(message)s",
)

tran = Translate(
    json.load(open("./languageMap.json", encoding="utf-8")), setting.language
)

pluginList = []
for path in config.plugin:
    spec = util.spec_from_file_location(
        "plugin",
        f"{setting.dataDir}/{setting.desktopPet}/plugin/{path}/{setting.pluginFileName}.py",
    )
    if spec and spec.loader:
        plugin = util.module_from_spec(spec)
        sys.modules["plugin"] = plugin
        spec.loader.exec_module(plugin)
        pluginList.append(plugin)

app = QtWidgets.QApplication(sys.argv)

screenWidth = app.primaryScreen().size().width()
screenHeight = app.primaryScreen().size().height()

window = Window()
window.showFullScreen()

sys.exit(app.exec())
