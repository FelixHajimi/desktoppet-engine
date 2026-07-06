const { app, BrowserWindow } = require("electron");
const { exec } = require("child_process");
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    resizable: true,
    title: "桌宠启动器",
    webPreferences: {
      contextIsolation: false,
      nodeIntegration: true,
    }
  });

  win.loadFile(path.join(__dirname, './main.html'));
  win.webContents.openDevTools();
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});