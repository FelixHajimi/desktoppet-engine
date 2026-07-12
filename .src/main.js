const { ipcRenderer } = require("electron");
const path = require("path")

async function loadSetting() {
  const setting_loader = await fetch("setting.json");
  const setting = await setting_loader.json();
  return setting;
}

/**
 * @param {object} setting
 * @returns {object}
 */
async function loadConfig(setting) {
  const config_loader = await fetch(
    `${setting.dataDir}/${setting.desktopPet}/config.json`,
  );
  const config = await config_loader.json();
  return config;
}

class Message {
  node;
  /**
   * @param {string} text
   * @param {string} type
   */
  constructor(text, type) {
    this.node = document.createElement("div");
    this.node.className = type;
    this.node.innerHTML = `<p>${text}</p>`;
    setTimeout(() => {
      this.node.querySelector("p").setAttribute("drop", "");
      setTimeout(() => {
        this.node.remove();
      }, 1000);
    }, 3000);
  }
}

class Information {
  node;
  /**
   * @param {string} text
   */
  constructor(text) {
    const message = new Message(text, "information");
    this.node = message.node;
  }
}

class Warning {
  node;
  /**
   * @param {string} text
   */
  constructor(text) {
    const message = new Message(text, "warning");
    this.node = message.node;
  }
}

class Error {
  node;
  /**
   * @param {string} text
   */
  constructor(text) {
    const message = new Message(text, "error");
    this.node = message.node;
  }
}

async function main() {
  const setting = await loadSetting();
  const config = await loadConfig(setting);

  const icon = document.getElementById("icon");
  icon.src = `${setting.dataDir}/${setting.desktopPet}/${setting.desktoppetResourceDir}/icon.gif`;

  const pet_name = document.getElementById("pet_name");
  pet_name.innerText = config.name;

  const pet_verstion = document.getElementById("pet_verstion");
  pet_verstion.innerText = "v" + config.version;

  const pet_author = document.getElementById("pet_author");
  pet_author.innerText = "作者:" + config.author;

  const start_button = document.getElementById("start_button");
  start_button.addEventListener("click", () => {
    const message = document.getElementById("message");
    message.appendChild(new Information("桌宠启动中,请稍等2-5秒").node);
    ipcRenderer.send("exec", [`python ${path.join(__dirname, "main.py")}`]);
  });

  const desktoppet_config = document.getElementById("desktoppet_config");
  desktoppet_config.addEventListener("click", (event) => {
    // ipcRenderer.send("change_page", ["desktoppet_config"]);
    ipcRenderer.send("exec", [
      `start ${path.join(__dirname, `${setting.dataDir}/${setting.desktopPet}/config.json`)}`,
    ]);
  });
}
main();
