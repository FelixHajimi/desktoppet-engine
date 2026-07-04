# DesktopPet-Engine(桌宠引擎)
[![GitHub Repo stars](https://img.shields.io/github/stars/FelixHajimi/desktoppet-engine?style=social)](https://github.com/FelixHajimi/desktoppet-engine)
[![GitHub forks](https://img.shields.io/github/forks/FelixHajimi/desktoppet-engine?style=social)](https://github.com/FelixHajimi/desktoppet-engine)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
一个轻量级的桌宠加载引擎，支持物理模拟、插件扩展、国际化、日志记录。让任何角色都能在你的桌面上活过来

<!--## 演示视频
> 以一个 为素材进行展示

| 互动效果 | 右键菜单 | 辅助办公 |
| --- | --- | --- |
| 互动效果 | 右键菜单 | 辅助办公 |-->
<!--目前素材正在征集中，请各位画师多多贡献！🙇‍-->

## 它能干什么
### 对于用户
- 桌面宠物：一个会重力下落、会弹跳、有物理碰撞的桌面小可爱
- 拖拽互动：按住左键拖起来扔出去，它会物理弹跳
- 多状态动画：站立、下落、被拖拽 —— 每个状态自动切换对应动画
- 插件扩展：支持加载插件，让桌宠能做更多事（比如定时提醒、天气显示等）
- 多语言：内置中英文切换，按需配置
- 窗口置顶：始终悬浮在桌面最上层，不会被其他窗口挡住
### 对于开发者
- 角色包即开即用：只需准备图片资源和一份 config.json，无需写代码
- 自由定义物理参数：重力加速度、弹性系数、摩擦力全都可以调
- 插件系统：支持 Python 插件，可以扩展任意交互逻辑
- 调试模式：开启后显示碰撞箱、输出运行参数，方便调优

## 项目目录
```text
├─ data/                      存放所有桌宠的根目录
│  └─ 桌宠目录/                单个桌宠对象
│     ├─ config.json          桌宠配置
│     ├─ plugin/              桌宠插件
│     │  └─ [插件名]/          单个插件对象
│     │     └─ enter.py       插件入口
│     └─ res/                 桌宠资源文件
│        ├─ drop.gif          掉落
│        ├─ icon.gif          图标
│        └─ stand.gif         站立
├─ languageMap.py             国际化语言表
├─ main.py                    主程序
└─ setting.json               启动设置
```

## 如何开始
> 普通用户可以直接下载打包程序并使用
### 测试
你需要有一个Python环境并且安装上PySide6才能运行

在终端输入`python main.py`，运行成功则会显示存放在res里面的素材

### 桌宠配置
```json
{
  "name": "",
  "version": "",
  "author": "",
  "acc": [...],
  "fri": {...},
  "ela": {...},
  "plugin": [...]
}
```
| 键 | 描述 | 推荐值 |
| --- | --- | --- |
| name | 桌宠名称 |
| version | 版本号 |
| author | 作者 |
| acc | 重力加速度 | [0, 0.8~2] |
| fri | 摩擦力 | t\|b=1~5 l\|r=0 |
| ela | 弹力系数 | b=5 l\|r=10 |
| plugin | 加载的插件列表 |

详见`docs/中文/桌宠配置.md`

### 启动设置
```json
{
    "desktopPet": "Example",
    "debug": true,
    "language": "zh-cn"
}
```
| 键 | 描述 |
| --- | --- |
| desktopPet | 启动程序后将要开启的桌宠对象 |
| debug | 调试模式状态 |
| language | 程序将使用的语言 |

详见`docs/中文/启动设置.md`

## 常见问题
Q 为什么启动不成功，显示了报错？  
A 可能是配置原因，请提交issue或查看相关问题解决方案

Q 为什么桌宠卡在屏幕边缘不动了？  
A 请查看桌宠的`fri`设置，如果大于`acc`则请调整为正常数值

Q 能不能同时开启多个桌宠？  
A 目前仅支持单例启动，正在开发中

Q 怎么切换语言？  
A 修改`setting.json`中的`language`为`zh-cn`(中文)或`en-us`(英文)

Q 插件加载失败怎么办？  
A 检查`config.json`中的`plugin`列表是否与`/data/角色名/plugin/`下的文件夹名一致，同时确保`enter.py`存在且语法正确。错误日志会写入`/last.log`

Q 我想自己做一个角色包，需要会编程吗？  
A 一般情况下不需要，**基础**的角色只需要美术素材，不需要你会编程

Q 我怎么报告 Bug？  
A 请说明错误情况以及附带`./last.log`日志文件提交issue

## 交流群
QQ群：109956850  
进群请查看群公告

## 贡献
如果你有对该项目的建议反馈，请提交想法或希望改进的点到issue

我们正在征集角色素材！如果你擅长画像素风/Q版角色，欢迎加入 QQ 群或提交 Issue！

## 相关文档
请查阅`/docs/中文/*`
