import json
import logging
import sys
import os
from dataclasses import dataclass, field
from importlib import util

from PySide6 import QtCore, QtGui, QtWidgets

app = QtWidgets.QApplication(sys.argv)


# 创建菜单工具
# Create Menu Tool
def menuGenerate(master: "Window", structure: dict):
    menu = QtWidgets.QMenu(master)

    def func(mainMenu: QtWidgets.QMenu, structure: dict, master=master):
        for key in structure.keys():
            if key in ["_type", "_func", "_activate"]:
                continue
            elif structure[key]["_type"] == "$":
                command = QtGui.QAction(key, mainMenu)
                if "_func" in structure[key]:
                    command.triggered.connect(structure[key]["_func"])
                elif "_activate" in structure[key]:

                    def itemFunc(func=structure[key]["_activate"], displayName=key):
                        def insideFunc():
                            nonlocal displayName
                            try:
                                getattr(func, "activate")(master.state)
                                createLog(
                                    eval(
                                        tran.run(
                                            "program.plugin.function.run",
                                            'f"Plugin `{displayName}` has run"',
                                        )
                                    )
                                )
                            except Exception as error:  # noqa: F841
                                createLog(
                                    eval(
                                        tran.run(
                                            "program.plugin.function.runError",
                                            'f"Plugin `{displayName}` function error: `{error}`"',
                                        )
                                    ),
                                    3,
                                )

                        return insideFunc

                    command.triggered.connect(itemFunc())

                mainMenu.addAction(command)
            elif structure[key]["_type"] == "-":
                mainMenu.addSeparator()
            elif structure[key]["_type"] == "/":
                submenu = QtWidgets.QMenu(key, mainMenu)
                func(submenu, structure[key])
                mainMenu.addMenu(submenu)

    func(menu, structure)
    return menu


# 日志工具
# Log Tool
def createLog(msg: str, level: int = 0):
    """
    ## Level
    | Num | Level |
    | --- | --- |
    | 0 | debug |
    | 1 | info |
    | 2 | warn |
    | 3 | error |
    | 4 | critical |
    """
    if level >= setting.logLevel and level == 0:
        logging.debug(msg)
    if level >= setting.logLevel and level == 1:
        logging.info(msg)
    if level >= setting.logLevel and level == 2:
        logging.warning(msg)
    if level >= setting.logLevel and level == 3:
        logging.error(msg)
        QtWidgets.QMessageBox.critical(
            None, "错误", f"桌宠启动过程中出现错误，具体信息查看日志\n\n{msg}"
        )
    if level >= setting.logLevel and level == 4:
        logging.critical(msg)
        sys.exit()


# 语言服务
# Language Services
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
                createLog(
                    f'TRANSLATE ERROR: not found "{self.lang}" language and not found "en-us"',
                    3,
                )
                return "ERROR"
        elif fallback is not None:
            return fallback
        else:
            createLog(f'TRANSLATE ERROR: not found "{key}" key', 3)
            return "ERROR"


# 分隔符序号生成器
# Separator Number Generator
def sep_iter():
    count = 0
    while True:
        yield f"sep_{count}"
        count += 1


# 配置类
# Configuration Class
@dataclass
class Setting:
    desktopPet: str
    dataDir: str
    imageSize: list[int]
    language: str
    logPath: str = "./last.log"
    logLevel: int = 0


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
            QtGui.QIcon(f"{setting.dataDir}/{setting.desktopPet}/res/icon.gif")
        )
        self.setWindowFlags(
            QtCore.Qt.WindowType.WindowStaysOnTopHint
            | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        createLog(tran.run("window.complete", "Window initialization complete"))

        self.WIDTH, self.HEIGHT = setting.imageSize
        self.nowMousePos = [0, 0]
        self.lastMousePos = [0, 0]

        self.pause = False
        self.position = [(screenWidth - self.WIDTH) // 2, screenHeight - self.HEIGHT]
        self.motion = [0, 0]
        self.sep_iter = sep_iter()

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
        self.image.setScaledSize(QtCore.QSize(self.WIDTH, self.HEIGHT))
        self.desktopPet.setMovie(self.image)
        self.desktopPet.resize(self.WIDTH, self.HEIGHT)

        self.state = {
            "pause": False,
            "position": self.position,
            "motion": self.motion,
            "sep_iter": self.sep_iter,
            "update": dict(),
            "screenWidth": screenWidth,
            "screenHeight": screenHeight,
        }
        createLog(tran.run("program.ready", "Program is ready"))

        # 插件初始化
        # Plugin Init
        def plugin_init(structure: dict):
            for key in structure.keys():
                if key in ["_type", "_func", "_activate"]:
                    continue
                elif structure[key]["_type"] == "$":
                    if "_activate" in structure[key]:
                        getattr(structure[key]["_activate"], "init")(
                            self.image, self.mainTimer, self.physicsTimer, self
                        )
                        if getattr(structure[key]["_activate"], "_autoStart"):
                            try:
                                getattr(structure[key]["_activate"], "activate")(
                                    self.state,
                                )
                                createLog(
                                    eval(
                                        tran.run(
                                            "program.plugin.autostart.run",
                                            'f"`{key}` auto-start function has run"',
                                        )
                                    ),
                                    0,
                                )
                            except Exception as error:
                                createLog(
                                    eval(
                                        tran.run(
                                            "program.plugin.autostart.runError",
                                            'f"`{key}` auto-start function run error: `{error}`"',
                                        )
                                    ),
                                    3,
                                )
                elif structure[key]["_type"] == "/":
                    plugin_init(structure[key])

        for plugin in pluginList:
            plugin_init(plugin.menu)

    def deactivate(self):
        def plugin_deactivate(structure: dict):
            for key in structure.keys():
                if key in ["_type", "_func", "_activate"]:
                    continue
                elif structure[key]["_type"] == "$":
                    if "_activate" in structure[key]:
                        getattr(structure[key]["_activate"], "deactivate")()
                elif structure[key]["_type"] == "/":
                    plugin_deactivate(structure[key])

        for plugin in pluginList:
            plugin_deactivate(plugin.menu)
        self.close()

    def loadMovie(self, path: str):
        # 加载动画
        # Loading Animation
        if self.image.fileName() != path:
            self.image.setFileName(path)
            self.image.jumpToFrame(0)
        self.image.start()

    def mainStep(self):
        # 主时钟循环
        # Main Clock Cycle
        self.pause = self.state["pause"]
        self.motion = self.state["motion"]
        self.position = self.state["position"]
        if not self.pause:
            if (
                abs(self.state["motion"][0]) <= config.acc[0]
                and abs(self.state["motion"][1]) <= config.acc[1]
            ):
                self.loadMovie(f"{setting.dataDir}/{setting.desktopPet}/res/stand.gif")
            else:
                self.loadMovie(f"{setting.dataDir}/{setting.desktopPet}/res/drop.gif")

        for key, func in self.state["update"].items():
            try:
                func()
            except Exception as error:  # noqa: F841
                createLog(
                    eval(
                        tran.run(
                            "program.plugin.loopFunction.runError",
                            'f"`{func}` loop function run error: `{error}`"',
                        )
                    ),
                    3,
                )
                self.deactivate()

        self.move(self.state["position"][0], self.state["position"][1])

    def physicsStep(self):
        # 物理时钟循环
        # Physical Clock Cycle
        config.ela = {"top": 0, "bottom": 0, "left": 0, "right": 0} | config.ela
        config.fri = {"top": 0, "bottom": 0, "left": 0, "right": 0} | config.fri

        # 重力模拟
        # Gravity Simulation
        self.state["motion"][0] += config.acc[0]
        self.state["motion"][1] += config.acc[1]

        # 速度预处理
        # Speed Preprocessing
        if self.state["motion"][0] > screenWidth - (
            self.state["position"][0] + self.WIDTH
        ):
            self.state["motion"][0] = (-self.state["motion"][0]) * (
                config.ela["right"] / 100
            )
            self.state["position"][0] = screenWidth - self.WIDTH
        elif -self.state["motion"][0] > self.state["position"][0]:
            self.state["motion"][0] = (-self.state["motion"][0]) * (
                config.ela["left"] / 100
            )
            self.state["position"][0] = 0
        elif self.state["motion"][1] > screenHeight - (
            self.state["position"][1] + self.HEIGHT
        ):
            self.state["motion"][1] = (-self.state["motion"][1]) * (
                config.ela["bottom"] / 100
            )
            self.state["position"][1] = screenHeight - self.HEIGHT
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
        elif self.state["position"][0] == screenWidth - self.WIDTH:
            if abs(self.motion[1]) < config.fri["right"]:
                self.motion[1] = 0
            else:
                self.motion[1] += config.fri["right"] * ((-1) ** (self.motion[1] > 0))
        if self.state["position"][1] == 0:
            if abs(self.motion[0]) < config.fri["top"]:
                self.motion[0] = 0
            else:
                self.motion[0] += config.fri["top"] * ((-1) ** (self.motion[0] > 0))
        elif self.state["position"][1] == screenHeight - self.HEIGHT:
            if abs(self.motion[0]) < config.fri["bottom"]:
                self.motion[0] = 0
            else:
                self.motion[0] += config.fri["bottom"] * ((-1) ** (self.motion[0] > 0))

        # 设置位置
        # Set Position
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
        # Right-Click Menu
        menuDict = {
            tran.run("program.menu.exit", "Exit"): {
                "_type": "$",
                "_func": self.deactivate,
            },
            next(self.sep_iter): {"_type": "-"},
            eval(tran.run("program.menu.about.title", 'f"About `{config.name}`"')): {
                "_type": "$",
                "_func": lambda: QtWidgets.QMessageBox.about(
                    self,
                    eval(
                        tran.run("program.menu.about.title", 'f"About `{config.name}`"')
                    ),
                    eval(
                        tran.run(
                            "program.menu.about.text",
                            'f"Desktop pet name: `{config.name}`\\nVersion: v`{config.version}`\\nAuthor: `{config.author}`"',
                        )
                    ),
                ),
            },
        }

        # 导入插件
        # Import Plugin
        for plugin in pluginList:
            menuDict[plugin.pluginName] = plugin.menu
        menu = menuGenerate(self, menuDict)
        menu.exec(globalPos)
        createLog(
            eval(
                tran.run(
                    "program.menu.show",
                    'f"`{setting.desktopPet}` desktop pet right-click menu is displayed"',
                )
            ),
            0,
        )


PATH = os.path.dirname(__file__)
# 导入数据
# Import Data
setting = Setting(**json.load(open(f"{PATH}/setting.json", encoding="utf-8")))
logging.debug("Setting loaded")
config = DesktopPetConfig(
    **json.load(
        open(f"{setting.dataDir}/{setting.desktopPet}/config.json", encoding="utf-8")
    )
)
logging.debug("Config loaded")

# 日志配置
# Log Configuration
logging.basicConfig(
    filename=f"{setting.logPath}",
    encoding="utf-8",
    level=logging.DEBUG,
    format="[%(levelname)s] <%(pathname)s> (%(asctime)s) - %(message)s",
)

tran = Translate(
    json.load(open(f"{PATH}/languageMap.json", encoding="utf-8")), setting.language
)
logging.debug("Translate object created")

pluginList = []
for path in config.plugin:
    spec = util.spec_from_file_location(
        "plugin",
        f"{setting.dataDir}/{setting.desktopPet}/plugin/{path}/enter.py",
    )
    if spec and spec.loader:
        plugin = util.module_from_spec(spec)
        sys.modules["plugin"] = plugin
        try:
            spec.loader.exec_module(plugin)
            pluginList.append(plugin)
            plugin.menu
            plugin.pluginName
            logging.debug(f"Plugin `{path}` loaded")
        except FileNotFoundError as error:
            logging.error(
                f"Failed to load the plugin in the directory of `{path}`, please check if the name in `config.json` is correct"
            )
        except NameError as error:
            logging.error(f"Plugin name error: {error}")


screenWidth = app.primaryScreen().size().width()
screenHeight = app.primaryScreen().size().height()

window = Window()
window.show()

sys.exit(app.exec())
