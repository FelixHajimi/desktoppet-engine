import json
import logging
import pprint
import sys
from importlib import util

from PySide6 import QtCore, QtGui, QtWidgets

# 初始化配置
logging.basicConfig(
    filename="./last.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="[%(levelname)s] <%(pathname)s> (%(asctime)s) - %(message)s",
)


# 创建菜单工具
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
def createLog(msg: str, level: int = 1):
    if setting["debug"]:
        if level == 0:
            logging.debug(msg)
        elif level == 1:
            logging.info(msg)
        elif level == 2:
            logging.warning(msg)
        elif level == 3:
            logging.error(msg)
        elif level == 4:
            logging.critical(msg)


# 定义窗口
class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(config["name"])
        self.setWindowIcon(QtGui.QIcon(f"./data/{setting['desktopPet']}/res/icon.gif"))
        self.setWindowFlags(
            QtCore.Qt.WindowType.WindowStaysOnTopHint
            | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        createLog("窗口初始化完毕")

        self.nowMousePos = [0, 0]
        self.lastMousePos = [0, 0]
        self.position = [(screenWidth - 128) // 2, screenHeight - 128]
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
        self.desktopPet.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)
        self.desktopPet.mousePressEvent = self.MousePressEvent
        self.desktopPet.mouseMoveEvent = self.MouseMoveEvent
        self.desktopPet.mouseReleaseEvent = self.MouseReleaseEvent
        self.image = QtGui.QMovie()
        self.desktopPet.setMovie(self.image)
        self.desktopPet.resize(128, 128)

        self.state = {
            "pause": False,
            "position": self.position,
            "motion": self.motion,
            "screenWidth": screenWidth,
            "screenHeight": screenHeight,
            "update": [],
        }
        createLog("参数配置完毕")

        # 自启动判断
        _ = []
        for plugin in pluginList:
            for displayName, entry in plugin.menu.items():

                def itemFunc(f=entry):
                    def _():
                        getattr(f, "enter")(
                            self.image,
                            self.mainTimer,
                            self.physicsTimer,
                            self.state,
                            self,
                        )

                    return _

                if getattr(entry, "__autoStart__"):
                    _.append(itemFunc())
                    createLog(
                        f"桌宠 {plugin.pluginName} 插件的 {displayName} 功能已添加置自启动"
                    )
        for i in _:
            try:
                i()
                createLog(f"{i} 自启动函数已运行")
            except Exception as error:
                createLog(f"{i} 自启动函数运行错误:{error}", 3)

    def loadMovie(self, path: str):
        # 加载动画
        if self.image.fileName() != path:
            self.image.setFileName(path)
            self.image.jumpToFrame(0)
        self.image.start()

    def mainStep(self):
        # 主时钟循环
        self.pause = self.state["pause"]
        self.motion = self.state["motion"]
        self.position = self.state["position"]
        if not self.pause:
            if (
                abs(self.state["motion"][0]) <= config["acc"][0]
                and abs(self.state["motion"][1]) <= config["acc"][1]
            ):
                self.loadMovie(f"./data/{setting['desktopPet']}/res/basic/stand.gif")
            else:
                self.loadMovie(f"./data/{setting['desktopPet']}/res/basic/drop.gif")

        for i in self.state["update"]:
            try:
                i()
            except Exception as error:
                createLog(f"{i} 循环函数运行错误:{error}", 3)

        self.desktopPet.move(self.state["position"][0], self.state["position"][1])

    def physicsStep(self):
        # 物理时钟循环

        # 重力模拟
        self.state["motion"][0] += config["acc"][0]
        self.state["motion"][1] += config["acc"][1]

        # 速度预处理
        if self.state["motion"][0] > screenWidth - (self.state["position"][0] + 128):
            self.state["motion"][0] = (-self.state["motion"][0]) * (
                config["ela"][1] / 100
            )
            self.state["position"][0] = screenWidth - 128
        elif -self.state["motion"][0] > self.state["position"][0]:
            self.state["motion"][0] = (-self.state["motion"][0]) * (
                config["ela"][1] / 100
            )
            self.state["position"][0] = 0
        elif self.state["motion"][1] > screenHeight - (self.state["position"][1] + 128):
            self.state["motion"][1] = (-self.state["motion"][1]) * (
                config["ela"][0] / 100
            )
            self.state["position"][1] = screenHeight - 128
        elif -self.state["motion"][1] > self.state["position"][1]:
            self.state["motion"][1] = (-self.state["motion"][1]) * (
                config["ela"][0] / 100
            )
            self.state["position"][1] = 0

        # 摩擦力
        if (
            self.state["position"][0] == 0
            or self.state["position"][0] == screenWidth - 128
        ):
            if abs(self.state["motion"][1]) < config["fri"][1]:
                self.state["motion"][1] = 0
            else:
                self.state["motion"][1] += config["fri"][1] * (
                    (-1) ** (self.state["motion"][1] > 0)
                )
        elif (
            self.state["position"][1] == 0
            or self.state["position"][1] == screenHeight - 128
        ):
            if abs(self.state["motion"][0]) < config["fri"][0]:
                self.state["motion"][0] = 0
            else:
                self.state["motion"][0] += config["fri"][0] * (
                    (-1) ** (self.state["motion"][0] > 0)
                )

        # 设置位置
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
        def about():
            QtWidgets.QMessageBox.about(
                self,
                f"关于{config['name']}",
                f"桌宠名字: {config['name']}\n版本号: v{config['version']}\n作者: {config['author']}",
            )

        menuDict = {
            "退出": {"__type__": "command", "__func__": self.close},
            f"关于{config['name']}": {"__type__": "command", "__func__": about},
        }
        createLog("已创建基础右键菜单")

        # 导入插件
        for plugin in pluginList:
            menuDict[plugin.pluginName] = {"__type__": "menu"}
            for displayName, entry in plugin.menu.items():

                def itemFunc(f=entry):
                    def _():
                        try:
                            getattr(f, "enter")(
                                self.image,
                                self.mainTimer,
                                self.physicsTimer,
                                self.state,
                                self,
                            )
                        except Exception as error:
                            createLog(
                                f"桌宠 {plugin.pluginName} 插件的 {displayName}:{getattr(f, 'create')} 功能错误:{error}",
                                3,
                            )

                    return _

                menuDict[plugin.pluginName][displayName] = {
                    "__type__": "command",
                    "__func__": itemFunc(),
                }
                createLog(f"桌宠 {plugin.pluginName} 插件的 {displayName} 功能已添加")

        if setting["debug"]:
            if self.showBox:
                menuDict["开/关碰撞箱"] = {
                    "__type__": "command",
                    "__func__": lambda: self.desktopPet.setStyleSheet(""),
                }
                self.showBox = False
            else:
                menuDict["开/关碰撞箱"] = {
                    "__type__": "command",
                    "__func__": lambda: self.desktopPet.setStyleSheet(
                        "border: 1px solid yellow;"
                    ),
                }
                self.showBox = True
            menuDict["输出所有参数"] = {
                "__type__": "command",
                "__func__": lambda: createLog(
                    "\n" + pprint.pformat(globals(), 2, sort_dicts=False)
                ),
            }
        menu = menuGenerate(self, menuDict)
        menu.exec(globalPos)
        createLog(f"{setting['desktopPet']}:{config['name']} 桌宠右键菜单已显示")


# 导入数据
setting = json.load(open("./setting.json", encoding="utf-8"))
for key in ["desktopPet", "debug"]:
    if key not in setting:
        logging.error(f"setting.json 文件没有 {key} 键!")
        exit()

config = json.load(
    open(f"./data/{setting['desktopPet']}/config.json", encoding="utf-8")
)
for key in [
    "name",
    "version",
    "author",
    "acc",
    "fri",
    "plugin",
]:
    if key not in config:
        logging.error(f"config.json 文件没有 {key} 键!")
        exit()

pluginList = []
if "plugin" in config:
    for path in config["plugin"]:
        spec = util.spec_from_file_location(
            "plugin", f"./data/{setting['desktopPet']}/plugin/{path}/main.py"
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
