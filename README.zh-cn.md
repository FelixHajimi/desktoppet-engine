## DesktopPet-Engine（桌宠引擎）

[![GitHub Repo stars](https://img.shields.io/github/stars/FelixHajimi/desktoppet-engine?style=social)](https://github.com/FelixHajimi/desktoppet-engine)
[![GitHub forks](https://img.shields.io/github/forks/FelixHajimi/desktoppet-engine?style=social)](https://github.com/FelixHajimi/desktoppet-engine)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

一个轻量级的桌宠加载引擎，支持物理模拟、插件扩展、国际化、日志记录。让任何角色都能在你的桌面上活过来。

---

## 它能干什么

### 对于用户

- **桌面宠物**：一个会重力下落、会弹跳、有物理碰撞的桌面小可爱
- **拖拽互动**：按住左键拖起来扔出去，它会物理弹跳
- **多状态动画**：站立、下落、被拖拽 —— 每个状态自动切换对应动画
- **插件扩展**：支持加载插件，让桌宠能做更多事（比如定时提醒、天气显示等）
- **多语言**：内置多语言支持，按需配置
- **窗口置顶**：始终悬浮在桌面最上层，不会被其他窗口挡住

### 对于开发者

- **角色包即开即用**：只需准备图片资源和一份 `config.json`，无需写代码
- **自由定义物理参数**：重力加速度、弹性系数、摩擦力全都可以调
- **插件系统**：支持 Python 插件，可以扩展任意交互逻辑
- **调试模式**：开启后显示碰撞箱、输出运行参数，方便调优

---

## 项目目录

```text
├─ data/                      存放所有桌宠的根目录
│  └─ 桌宠目录/                单个桌宠对象
│     ├─ config.json          桌宠配置
│     ├─ plugin/              桌宠插件
│     │  └─ [插件名]/          单个插件对象
│     │     └─ enter.py       插件入口
│     └─ res/                 桌宠资源文件
│        ├─ drop.gif          掉落动画
│        ├─ icon.gif          窗口图标
│        └─ stand.gif         站立动画
├─ docs/                      文档目录
│  └─ 中文/
│     ├─ 启动配置.md
│     ├─ 桌宠配置.md
│     ├─ 角色包制作.md
│     ├─ 插件开发.md
│     └─ 常见问题.md
├─ languageMap.json           国际化语言表
├─ main.py                    主程序
├─ setting.json               启动配置
└─ last.log                   运行日志
```

---

## 如何开始

### 运行程序

**方式一：使用打包程序**

普通用户可以直接下载打包后的可执行文件，解压后双击运行即可。

**方式二：源码运行**

你需要有 Python 环境并安装 PySide6：

```bash
pip install PySide6
python main.py
```

运行成功则会显示存放在 `res/` 中的桌宠素材。

### 基础配置

#### 启动设置（`setting.json`）

```json
{
  "desktopPet": "Example",
  "dataDir": "data",
  "imageSize": [128, 128],
  "language": "zh-cn",
  "logPath": "./last.log",
  "logLevel": 0
}
```

| 键           | 描述                 |
| ------------ | -------------------- |
| `desktopPet` | 启动后加载的桌宠名称 |
| `dataDir`    | 桌宠数据目录         |
| `imageSize`  | 桌宠显示尺寸         |
| `language`   | 界面语言             |
| `logPath`    | 日志文件路径         |
| `logLevel`   | 日志输出等级         |

详见 [`docs/中文/启动配置.md`](./docs/中文/启动配置.md)

#### 桌宠配置（`data/[桌宠名]/config.json`）

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
  "plugin": []
}
```

| 键        | 描述           | 推荐值                           |
| --------- | -------------- | -------------------------------- |
| `name`    | 桌宠名称       | -                                |
| `version` | 版本号         | -                                |
| `author`  | 作者           | -                                |
| `acc`     | 重力加速度     | `[0, 0.8~2]`                     |
| `fri`     | 摩擦力         | `top/bottom=1~5`，`left/right=0` |
| `ela`     | 弹性系数       | `bottom=5`，`left/right=10`      |
| `plugin`  | 加载的插件列表 | `[]`                             |

详见 [`docs/中文/桌宠配置.md`](./docs/中文/桌宠配置.md)

---

## 相关文档

完整文档请查阅 `docs/中文/` 目录：

| 文档                                         | 说明                      |
| -------------------------------------------- | ------------------------- |
| [`启动配置.md`](./docs/中文/启动配置.md)     | `setting.json` 各字段详解 |
| [`桌宠配置.md`](./docs/中文/桌宠配置.md)     | `config.json` 各字段详解  |
| [`角色包制作.md`](./docs/中文/角色包制作.md) | 从零制作角色包，无需编程  |
| [`插件开发.md`](./docs/中文/插件开发.md)     | 插件开发完整指南          |
| [`常见问题.md`](./docs/中文/常见问题.md)     | 用户常见问题汇总          |
