## Frequently Asked Questions

---

### Startup Issues

**Q: The program does nothing when launched?**

**A:** Please check the following:

1. Verify that PySide6 is installed: `pip install PySide6`
2. Check that `setting.json` exists in the root directory
3. Check the `last.log` log file for error messages

---

**Q: The program reports that the pet cannot be found on startup?**

**A:** Check that the `desktopPet` value in `setting.json` matches a folder name under the `data/` directory.

- For example, `"desktopPet": "Example"` corresponds to `data/Example/`
- Folder names are case-sensitive

---

**Q: What if `setting.json` is missing or has incorrect formatting?**

**A:** The program will report an error and exit. You can copy a correct template from the project, or manually create it:

```json
{
  "desktopPet": "Example",
  "debug": false,
  "language": "en-us",
  "dataDir": "data",
  "desktoppetResourceDir": "res",
  "pluginFileName": "enter",
  "pluginObjectEnter": "enter",
  "logPath": "./last.log",
  "imageSize": [128, 128]
}
```

---

**Q: Where is the log file located?**

**A:** The log file path is specified by `logPath` in `setting.json`, defaulting to `last.log` in the root directory. It contains all log output during program runtime. More detailed information is output when debug mode is enabled.

---

### Configuration Issues

**Q: Configuration changes don't take effect?**

**A:** Restart the program after modifying `setting.json` or `config.json`.

---

**Q: Language changes don't take effect?**

**A:** Confirm that the `language` value is a supported language code, and restart the program after modification.

Currently supported languages:
`zh-cn`, `zh-tw`, `en-us`, `ja-jp`, `ko-kr`, `ru-ru`, `fr-fr`

---

### Physics Behavior Issues

**Q: The pet gets stuck at the screen edge and stops moving?**

**A:** Check the `fri` parameter in `config.json`. If friction is set too high, it may prevent velocity from overcoming gravity. Recommended `top` and `bottom` values are between `1` and `5`.

---

**Q: The pet falls too fast or too slow?**

**A:** Adjust the `y` value in the `acc` parameter:

- Higher values result in faster falling
- Recommended range: `0.8 ~ 2`

---

**Q: The pet bounces abnormally when hitting the edge?**

**A:** Check the `ela` parameter. Higher values result in stronger bounces. For example, `10` means a 10% velocity rebound.

| Direction         | Recommended Value |
| ----------------- | ----------------- |
| Bottom bounce     | `5`               |
| Left/Right bounce | `10`              |
| Top bounce        | `0`               |

---

**Q: How do I make the pet move horizontally?**

**A:** Adjust the `x` value in the `acc` parameter, or modify `state["motion"][0]` in a plugin.

---

### Animation Issues

**Q: The pet doesn't display animations?**

**A:** Verify the following:

1. `stand.gif` and `drop.gif` exist in the `res/` directory
2. Files are valid GIF format
3. Filenames are correct (case-sensitive, all lowercase)

---

**Q: The pet size is incorrect?**

**A:** Ensure the GIF dimensions match the `imageSize` setting in `setting.json`.

---

**Q: Transparent background isn't working?**

**A:** Verify that the GIF was saved with transparency enabled.

---

### Plugin Issues

**Q: A plugin fails to load?**

**A:** Check the following:

1. The `plugin` list in `config.json` matches the folder names under the `plugin/` directory
2. Each plugin directory contains the file specified by `pluginFileName` in `setting.json` (default: `enter.py`)
3. `pluginName` and `menu` are properly defined in `enter.py`
4. Error logs are written to `last.log`

---

**Q: The plugin menu doesn't appear?**

**A:** Verify:

1. The plugin is correctly listed in the `plugin` array
2. `pluginName` is defined
3. The `menu` dictionary is not empty

---

**Q: Auto-start doesn't execute for a plugin?**

**A:** Confirm that `self._autoStart = True` is set in the class.

---

### Packaging Issues

**Q: How do I package the program as an executable?**

**A:** Use PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "DesktopPet" main.py
```

---

**Q: The pet doesn't run after packaging?**

**A:** Check that the `data/` directory, `setting.json`, and `languageMap.json` are included in the package. You may need to use the `--add-data` parameter:

```bash
pyinstaller --onefile --windowed --add-data "data;data" --add-data "setting.json;." --add-data "languageMap.json;." main.py
```

---

### Other Issues

**Q: The pet window is covered by other programs?**

**A:** The program stays on top by default. If it's being covered, check if another program is forcing itself to stay on top. Try restarting the program.

---

**Q: How do I switch to a different pet?**

**A:** Change the `desktopPet` value in `setting.json` to the target pet folder name, and restart the program.

---

**Q: How do I share a pet package I created?**

**A:** Compress the pet folder into a `.zip` file. Other users can extract it into their `data/` directory and use it.

---

**Q: I don't understand the error message. What should I do?**

**A:**

1. Check the `last.log` log file
2. Submit an Issue with the error information and logs
3. Join the QQ group (109956850) for help
