## Pet Configuration

The pet configuration is stored in the `data/[pet_name]/config.json` file. This file defines the behavior parameters for an individual pet.

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
  "plugin": ["message"]
}
```

---

### `name` (Required)

The pet name, displayed in the window title bar.

### `version` (Required)

The pet version number.

### `author` (Required)

The pet author.

### `acc` (Required)

Gravity acceleration, formatted as `[x_direction, y_direction]`.

| Direction | Description | Recommended Value |
|------|------|--------|
| `x` | Horizontal acceleration | `0` |
| `y` | Vertical acceleration (gravity) | `0.8 ~ 2` |

### `fri` (Required)

Friction. When the pet reaches the screen edge, friction in the corresponding direction gradually reduces its velocity.

| Parameter | Description | Recommended Value |
|------|------|--------|
| `top` | Friction when reaching the top edge | `1 ~ 5` |
| `bottom` | Friction when reaching the bottom edge | `1 ~ 5` |
| `left` | Friction when reaching the left edge | `0` |
| `right` | Friction when reaching the right edge | `0` |

### `ela` (Required)

Bounce coefficient. When the pet hits the screen edge, velocity is rebounded by a percentage.

| Parameter | Description | Recommended Value |
|------|------|--------|
| `top` | Bounce coefficient at the top edge | `0` |
| `bottom` | Bounce coefficient at the bottom edge | `5` (i.e., 5%) |
| `left` | Bounce coefficient at the left edge | `10` (i.e., 10%) |
| `right` | Bounce coefficient at the right edge | `10` (i.e., 10%) |

### `plugin` (Optional)

List of plugins to load. Each element corresponds to a folder name under the `plugin/` directory.

```json
"plugin": ["message", "reminder"]
```

If you are not using plugins, you may omit this field:

```json
"plugin": []
```

---

### Animation Resources

The pet requires the following animation resources, sized at 128x128, stored in the `res/` directory:

| Filename | Description | Size |
|---|---|---|
| `stand.gif` | Standing animation (idle state) | 128x128 |
| `drop.gif` | Falling animation (moving state) | 128x128 |
| `icon.gif` | Window icon | 128x128 |

The program automatically switches between `stand` and `drop` animations based on the pet's motion state.
