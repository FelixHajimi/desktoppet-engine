## DesktopPet-Engine

[![GitHub Repo stars](https://img.shields.io/github/stars/FelixHajimi/desktoppet-engine?style=social)](https://github.com/desktoppet-engine/desktoppet-engine)
[![GitHub forks](https://img.shields.io/github/forks/FelixHajimi/desktoppet-engine?style=social)](https://github.com/desktoppet-engine/desktoppet-engine)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

A lightweight desktop pet engine that supports physics simulation, plugin extensions, internationalization, and logging. Bring any character to life on your desktop.

---

## What It Can Do

### For Users

- **Desktop Pet**: A cute little companion that falls with gravity, bounces, and responds to physics collisions
- **Drag & Drop Interaction**: Drag it up with left mouse button and throw it — it will bounce physically
- **Multi-State Animation**: Standing, falling, being dragged — each state automatically switches to the corresponding animation
- **Plugin Extensions**: Load plugins to add more features (e.g., timed reminders, weather display, etc.)
- **Multi-Language**: Built-in multi-language support, configurable as needed
- **Always on Top**: Stays on top of all other windows

### For Developers

- **Ready-to-Use Character Packs**: Just prepare image assets and a `config.json` file, no coding required
- **Customizable Physics Parameters**: Gravity, elasticity, friction — all adjustable
- **Plugin System**: Python plugin support for extending any interaction logic
- **Debug Mode**: Shows collision boxes and outputs runtime parameters for easy tuning

---

## Project Structure

```text
├─ data/                      Root directory for all desktop pets
│  └─ [pet_name]/             Individual pet directory
│     ├─ config.json          Pet configuration
│     ├─ plugin/              Pet plugins
│     │  └─ [plugin_name]/    Individual plugin directory
│     │     └─ enter.py       Plugin entry point
│     └─ res/                 Pet resource files
│        ├─ drop.gif          Falling animation
│        ├─ icon.gif          Window icon
│        └─ stand.gif         Standing animation
├─ docs/                      Documentation directory
│  ├─ 中文/
│  │  ├─ 启动配置.md
│  │  ├─ 桌宠配置.md
│  │  ├─ 角色包制作.md
│  │  ├─ 插件开发.md
│  │  └─ 常见问题.md
│  └─ English/
│     ├─ StartupConfiguration.md
│     ├─ PetConfiguration.md
│     ├─ PetPackageCreation.md
│     ├─ Plugin.md
│     └─ FrequentlyAskedQuestions.md
├─ languageMap.json           Internationalization language map
├─ main.py                    Main program
├─ setting.json               Launch configuration
└─ last.log                   Runtime log
```

---

## Getting Started

### Running the Program

**Option 1: Using the Packaged Executable**

Regular users can download the pre-packaged executable, extract it, and double-click to run.

**Option 2: Running from Source**

You need a Python environment with PySide6 installed:

```bash
pip install PySide6
python main.py
```

If successful, the pet assets in `res/` will be displayed.

### Basic Configuration

#### Launch Configuration (`setting.json`)

```json
{
  "desktopPet": "Example",
  "dataDir": "data",
  "imageSize": [128, 128],
  "language": "en-us",
  "logPath": "./last.log",
  "logLevel": 0
}
```

| Key | Description |
|---|---|
| `desktopPet` | Name of the pet to load on startup |
| `dataDir` | Data directory for pets |
| `imageSize` | Display size of the pet |
| `language` | Interface language |
| `logPath` | Log file path |
| `logLevel` | Log output level |

See [`docs/English/StartupConfiguration.md`](./docs/English/StartupConfiguration.md) for details.

#### Pet Configuration (`data/[pet_name]/config.json`)

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

| Key | Description | Recommended Value |
|---|---|---|
| `name` | Pet name | - |
| `version` | Version number | - |
| `author` | Author | - |
| `acc` | Gravity acceleration | `[0, 0.8~2]` |
| `fri` | Friction | `top/bottom=1~5`, `left/right=0` |
| `ela` | Elasticity | `bottom=5`, `left/right=10` |
| `plugin` | Plugin list to load | `[]` |

See [`docs/English/PetConfiguration.md`](./docs/English/PetConfiguration.md) for details.

---

## Documentation

For full documentation, please refer to the `docs/` directory:

| Document |
|---|
| [`docs/English/StartupConfiguration.md`](./docs/English/StartupConfiguration.md) |
| [`docs/English/PetConfiguration.md`](./docs/English/PetConfiguration.md) |
| [`docs/English/PetPackageCreation.md`](./docs/English/PetPackageCreation.md) |
| [`docs/English/Plugin.md`](./docs/English/Plugin.md) |
| [`docs/English/FrequentlyAskedQuestions.md`](./docs/English/FrequentlyAskedQuestions.md) |