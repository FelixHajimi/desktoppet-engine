const { app, BrowserWindow, ipcMain } = require("electron");
const { exec } = require("child_process");
const path = require("path");
const fs = require("fs");

/** @type {BrowserWindow|null} */
let win = null;
function createWindow() {
  win = new BrowserWindow({
    width: 800,
    height: 600,
    resizable: true,
    title: "桌宠启动器",
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  win.loadFile(path.join(__dirname, "main.html"));
  // win.webContents.openDevTools();
}

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

/**
 * @param {string} level
 * @param {string|any} message
 */
function createLog(level, message) {
  let launcher_log = path.join(__dirname, "launcher-log.log");
  fs.appendFile(
    launcher_log,
    `[${level}] (${new Date().toLocaleString()}) - ${message}\n`,
    (err) => {
      if (err) {
        console.error("写入日志失败: ", err);
      }
    },
  );
}

ipcMain.on("exec", (event, args) => {
  for (let command of args) {
    exec(command, (err, stdout, stderr) => {
      createLog("INFO", `执行命令: ${command}`);
      if (err) {
        createLog("ERROR", stdout);
      }
    });
  }
});

ipcMain.on("change_page", (event, args) => {
  if (["main"].includes(args[0]) && win) {
    win.loadFile(path.join(__dirname, `${args[0]}.html`));
  }
});
