const hero_section = document.getElementById("hero-section");
const [about, project_description, memebers, other] =
  document.querySelectorAll("#option");

const restore_window = () => {
  const base = document.createElement("div");
  base.className = "logo-and-text center";

  const img = document.createElement("img");
  img.setAttribute("src", "assets/appIco.png");

  const p = document.createElement("p");
  p.textContent = "Axumit";

  base.append(img);
  base.append(p);

  hero_section.innerHTML = "";
  hero_section.append(base);
};

const about_window = () => {
  const base = document.createElement("div");
  base.className = "base-window";

  const title = document.createElement("h1");
  title.textContent = "About";

  const content = document.createElement("p");
  content.textContent = "about content";
  base.append(title);
  base.append(content);
  return base;
};

const memebers_window = () => {
  const base = document.createElement("div");
  base.className = "base-window";

  const title = document.createElement("h1");
  title.textContent = "Memebers";

  const content = document.createElement("p");
  content.textContent = "memebers content";
  base.append(title);
  base.append(content);
  return base;
};

const project_description_window = () => {
  const base = document.createElement("div");
  base.className = "base-window";

  const title = document.createElement("h1");
  title.textContent = "Project Description";

  const content = document.createElement("p");
  content.textContent = "Project Description Content";
  base.append(title);
  base.append(content);
  return base;
};

const other_window = () => {
  const base = document.createElement("div");
  base.className = "base-window";

  const title = document.createElement("h1");
  title.textContent = "Others";

  const content = document.createElement("p");
  content.textContent = "Others Description Content";
  base.append(title);
  base.append(content);
  return base;
};

const replaceContent = (content) => {
  hero_section.innerHTML = "";
  hero_section.append(content);
};

about.onmouseover = () => replaceContent(about_window());
memebers.onmouseover = () => replaceContent(memebers_window());
project_description.onmouseover = () =>
  replaceContent(project_description_window());
other.onmouseover = () => replaceContent(other_window());

document
  .querySelectorAll("#option")
  .forEach((btn) => (btn.onmouseleave = restore_window));
