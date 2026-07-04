## Startup Configuration

The startup configuration is stored in the `setting.json` file in the root directory. This file controls the global behavior of the program when it starts.

```json
{
  "desktopPet": "Example",
  "debug": true,
  "language": "zh-cn"
}
```

### `desktopPet` (Required)

The name of the pet directory to load at startup.

The program will look for the corresponding pet folder in the `data/` directory based on this name. For example, `"Example"` means loading the pet from the `data/Example/` directory.

### `debug` (Required)

Global debug mode toggle.

| Value | Description |
|------|------|
| `true` | Enable debug mode, output detailed logs, show collision boxes |
| `false` | Disable debug mode, only output necessary information |

When enabled, the right-click menu will display additional options like "Collision Box" and "Output Parameters" for development and debugging purposes.

### `language` (Required)

The interface language used by the program. This affects log output, right-click menus, dialog boxes, and plugin interfaces.

Currently supported languages:

| Language | Code |
| --- | --- |
| Chinese (Mainland China) | `zh-cn` |
| Chinese (Taiwan Region) | `zh-tw` |
| English (United States) | `en-us` |
| Japanese (Japan) | `ja-jp` |
| Korean (South Korea) | `ko-kr` |
| Russian (Russia) | `ru-ru` |
| French (France) | `fr-fr` |
