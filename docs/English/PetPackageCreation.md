## Pet Package Creation

This tutorial is designed for designers and regular users, teaching you how to create a desktop pet package from scratch with no programming experience required.

---

### Overview

A pet package is a folder containing configuration files and animation assets. Users simply place the pet package into the `data/` directory, and it becomes available for use in the program.

---

### Directory Structure

```
data/
└── your_pet_name/        # Pet package root directory (folder name = pet name)
    ├── config.json       # Pet configuration file
    ├── res/              # Asset resources directory
    │   ├── stand.gif     # Standing animation
    │   ├── drop.gif      # Falling animation
    │   └── icon.gif      # Window icon
    └── plugin/           # Plugin directory (optional)
        └── ...           # Plugin folders
```

---

### Step 1: Create the Pet Folder

Create a new folder in the `data/` directory. The folder name will be the pet name.

```
data/
└── MyPet/                # Example: pet name is "MyPet"
```

**Naming Conventions**:

- Use English letters, numbers, and underscores
- Avoid special characters or spaces
- Examples: `MyPet`, `cat_white`, `robot_v2`

---

### Step 2: Prepare Animation Assets

The pet requires 3 GIF animation files, all sized at **128x128 pixels**, stored in the `res/` directory:

```
data/MyPet/
└── res/
    ├── stand.gif         # Standing animation (idle state)
    ├── drop.gif          # Falling animation (moving state)
    └── icon.gif          # Window icon
```

#### Asset Requirements

| File        | Description              | Size    | Format |
| ----------- | ------------------------ | ------- | ------ |
| `stand.gif` | Standing/idle animation  | 128x128 | GIF    |
| `drop.gif`  | Falling/moving animation | 128x128 | GIF    |
| `icon.gif`  | Taskbar/title bar icon   | 128x128 | GIF    |

#### Tips

- **Transparent Background**: Recommended for a more natural look
- **Looping**: GIFs should be set to loop continuously
- **Frame Rate**: 8–12 frames per second is recommended for smooth animation
- **Centering**: Keep the character centered within the canvas
- **Tools**: Recommended tools include Photoshop, Aseprite, or online GIF makers

---

### Step 3: Create the Configuration File

Create a `config.json` file in the pet root directory:

```
data/MyPet/
├── config.json           # Configuration file
└── res/                  # Assets directory
```

For detailed field descriptions, see: [PetConfiguration](./PetConfiguration.md)

#### Basic Configuration Template

```json
{
  "name": "MyPet",
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
  }
  // "plugin" field is optional; can be omitted if not used
}
```

---

### Step 4: Test the Pet Package

1. Place the pet package into the `data/` directory
2. Modify the root `setting.json` file:

```json
{
  "desktopPet": "MyPet", // Change to your pet folder name
  "debug": false,
  "language": "en-us"
}
```

3. Run `main.py` or launch the packaged program
4. Verify that the pet displays correctly and physics behave as expected

---

### Step 5: Adjust Physics Parameters (Optional)

If the pet's behavior isn't ideal, adjust the physics parameters in `config.json`. For detailed parameter explanations

| Issue                     | Adjustment                                        |
| ------------------------- | ------------------------------------------------- |
| Falls too fast            | Decrease `acc` `y` value                          |
| Falls too slow            | Increase `acc` `y` value                          |
| Bounces too strongly      | Decrease `ela` values in corresponding directions |
| Bounces too weakly        | Increase `ela` values in corresponding directions |
| Stuck at edge             | Check if `fri` is too high; reduce if necessary   |
| Doesn't move horizontally | Increase `acc` `x` value                          |

---

### Complete Example

Full directory structure:

```
data/MyPet/
├── config.json
├── res/
│   ├── stand.gif
│   ├── drop.gif
│   └── icon.gif
└── plugin/               # No plugins yet; can be omitted
```

`config.json` content:

```json
{
  "name": "MyPet",
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
  }
}
```

---

### Sharing Your Pet Package

A pet package is just a folder. You can:

1. **Compress and Share**: Zip the pet folder and share it
2. **Contribute to the Project**: If the quality is good, submit an Issue or PR
3. **Share in the Community**: Post it in the QQ group or forums

**Installation**: Users simply unzip the package into the `data/` directory.
