async function loadSetting() {
  const setting_loader = await fetch("../setting.json");
  const setting = await setting_loader.json();
  return setting;
}

async function loadConfig(setting) {
  const config_loader = await fetch(
    `${setting.dataDir}/${setting.desktopPet}/config.json`,
  );
  const config = await config_loader.json();
  return config;
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
}
main();
