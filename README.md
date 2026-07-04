# DesktopPet-Engine
[![GitHub Repo stars](https://img.shields.io/github/stars/FelixHajimi/desktoppet-engine?style=social)](https://github.com/FelixHajimi/desktoppet-engine)
[![GitHub forks](https://img.shields.io/github/forks/FelixHajimi/desktoppet-engine?style=social)](https://github.com/FelixHajimi/desktoppet-engine)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
A lightweight desktop pet loading engine that supports physics simulation, plugin extensions, internationalization, and logging. It brings any character to life on your desktop.

<!--## Demo Video
> Using a  as material for demonstration

| Interactive Effects | Right-Click Menu | Office Assistance |
| --- | --- | --- |
| Interactive Effects | Right-Click Menu | Office Assistance |-->
<!--Materials are currently being solicited, artists are welcome to contribute! 🙇-->

## What It Can Do
### For Users
- Desktop Pet: A cute little companion on your desktop that falls with gravity, bounces, and has physical collision
- Drag Interaction: Click and hold the left button to drag it up and throw it out – it will bounce physically
- Multi-State Animation: Standing, falling, being dragged – each state automatically switches to the corresponding animation
- Plugin Extension: Supports loading plugins to enable more features (e.g., timed reminders, weather display, etc.)
- Multi-Language: Built-in Chinese and English switching, configurable as needed
- Always on Top: Stays on the topmost layer of the desktop, never blocked by other windows
### For Developers
- Character Pack Ready to Use: Just prepare image assets and a config.json file – no coding required
- Freely Adjustable Physics Parameters: Gravity, bounce coefficient, friction – all customizable
- Plugin System: Supports Python plugins for extending any interactive logic
- Debug Mode: Displays collision boxes, outputs runtime parameters for easy tuning

## Project Structure
```text
├─ data/                      Root directory for all desktop pets
│  └─ pet_name/               Individual pet folder
│     ├─ config.json          Pet configuration
│     ├─ plugin/              Pet plugins
│     │  └─ [plugin_name]/    Individual plugin folder
│     │     └─ enter.py       Plugin entry point
│     └─ res/                 Pet resource files
│        ├─ drop.gif          Falling
│        ├─ icon.gif          Icon
│        └─ stand.gif         Standing
├─ languageMap.py             Internationalization language map
├─ main.py                    Main program
└─ setting.json               Startup settings
```

## How to Get Started
> Regular users can directly download the packaged program and use it
### Testing
You need a Python environment with PySide6 installed to run it.

Run `python main.py` in the terminal – if successful, the assets in the res folder will be displayed.

### Pet Configuration
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
| Key | Description | Recommended Value |
| --- | --- | --- |
| name | Pet name | |
| version | Version number | |
| author | Author | |
| acc | Gravity acceleration | [0, 0.8~2] |
| fri | Friction | t\|b=1~5 l\|r=0 |
| ela | Bounce coefficient | b=5 l\|r=10 |
| plugin | List of plugins to load | |

See `docs/English/pet_config.md` for details.

### Startup Settings
```json
{
    "desktopPet": "Example",
    "debug": true,
    "language": "en-us"
}
```
| Key | Description |
| --- | --- |
| desktopPet | The pet to load when the program starts |
| debug | Debug mode status |
| language | Language to be used by the program |

See `docs/English/startup_settings.md` for details.

## Frequently Asked Questions
Q: Why does it fail to start and show an error?  
A: It might be a configuration issue. Please submit an issue or check the relevant solutions.

Q: Why is my pet stuck at the edge of the screen?  
A: Check the `fri` setting of your pet. If it is greater than `acc`, adjust it to a normal value.

Q: Can I run multiple pets at the same time?  
A: Currently only single instance is supported. Multi-instance support is under development.

Q: How do I switch languages?  
A: Change the `language` in `setting.json` to `zh-cn` (Chinese) or `en-us` (English).

Q: What if a plugin fails to load?  
A: Check that the `plugin` list in `config.json` matches the folder names under `/data/pet_name/plugin/`, and ensure `enter.py` exists with correct syntax. Error logs will be written to `/last.log`.

Q: I want to create my own character pack – do I need to know programming?  
A: Generally no. A **basic** character only needs art assets – no programming skills required.

Q: How do I report a Bug?  
A: Please describe the issue and attach the `./last.log` log file when submitting an issue.

## Community Group
QQ Group: 109956850  
Please check the group announcement upon joining.

## Contributing
If you have suggestions or feedback for this project, please submit your ideas or improvement points via issue.

We are currently soliciting character assets! If you are good at pixel art / chibi-style characters, welcome to join the QQ group or submit an Issue!

## Related Documentation
Please refer to `/docs/English/*`