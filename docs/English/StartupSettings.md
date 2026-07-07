## Startup Configuration

The startup configuration is stored in the `setting.json` file in the root directory. This file controls the global behavior of the program when it starts.

```json
{
  "desktopPet": "Example",
  "debug": true,
  "language": "en-us",
  "dataDir": "data",
  "desktoppetResourceDir": "res",
  "pluginFileName": "enter",
  "pluginObjectEntry": "enter",
  "logPath": "./last.log",
  "imageSize": [128, 128]
}
```

---

### `desktopPet`

The name of the pet directory to load at startup.

The program will look for the corresponding pet folder in the directory specified by `dataDir`. For example, `"Example"` means loading the pet from the `data/Example/` directory.

---

### `debug`

Global debug mode toggle.

| Value   | Description                                                   |
| ------- | ------------------------------------------------------------- |
| `true`  | Enable debug mode, output detailed logs, show collision boxes |
| `false` | Disable debug mode, only output necessary information         |

When enabled, the right-click menu will display additional options like "Collision Box" and "Output Parameters" for development and debugging purposes.

---

### `language`

The interface language used by the program. This affects log output, right-click menus, dialog boxes, and plugin interfaces.

Currently supported languages:

| Language                 | Code    |
| ------------------------ | ------- |
| Chinese (Mainland China) | `zh-cn` |
| Chinese (Taiwan Region)  | `zh-tw` |
| English (United States)  | `en-us` |
| Japanese (Japan)         | `ja-jp` |
| Korean (South Korea)     | `ko-kr` |
| Russian (Russia)         | `ru-ru` |
| French (France)          | `fr-fr` |

---

### `dataDir`

The pet data directory name.

The program will look for all pet folders under this directory.

---

### `desktoppetResourceDir`

The pet resource directory name.

Animation assets for each pet are stored under `[pet_directory]/[resource_directory]/`.

---

### `pluginFileName`

The plugin entry file name (without extension).

The program will load `[pet_directory]/plugin/[plugin_name]/[plugin_filename].py`.

---

### `pluginObjectEntry`

The plugin entry object name.

The program will call the method named `[plugin_entry_object]` in the plugin.

---

### `logPath`

The log file path.

All log output during program runtime will be written to this file.

---

### `imageSize`

The pet animation size, formatted as `[width, height]`.

The program will automatically scale animations to this size for display.
