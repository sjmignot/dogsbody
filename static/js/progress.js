const setAttributes = (el, attrs) => {
  Object.keys(attrs).forEach((key) => el.setAttribute(key, attrs[key]));
};

const getMax = () => document.body.scrollHeight - window.innerHeight;

const getValue = () => window.scrollY;
var progressBar = document.querySelector("progress");

progressBar.setAttribute("max", getMax());

document.onscroll = () => progressBar.setAttribute("value", getValue());

window.onresize = () =>
  setAttributes(progessBar, { max: getMax(), value: getValue() });
