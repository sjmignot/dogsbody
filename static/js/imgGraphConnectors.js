const offset = (el) => {
  let rect = el.getBoundingClientRect(),
    scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,
    scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  return { top: rect.top + scrollTop, left: rect.left + scrollLeft };
};

const removeElementsByClass = (className) => {
  var elements = document.getElementsByClassName(className);
  while (elements.length > 0) {
    elements[0].parentNode.removeChild(elements[0]);
  }
};

const body = document.querySelector("body");

const drawImageLinks = (offset, removeElementsByClass) => {
  removeElementsByClass("connector");

  imgs = document.querySelectorAll('img[src*="img-"]');
  let imgArray = [...imgs].sort(
    (a, b) =>
      a.src.split("#").pop().split("-").pop() -
      b.src.split("#").pop().split("-").pop()
  );
  console.log(imgArray);
  imgArray.map((img, i) => {
    let imgCircle = document.querySelector(`#img-${i + 1}`);
    let imgCircleWidth = imgCircle.getBoundingClientRect().width;

    let { top: imgCircleTop, left: imgCircleLeft } = offset(imgCircle);
    let { top: imgTop } = offset(img);
    let strokeWidth = 2;
    let div = document.createElement("div");
    div.style.cssText = `position:absolute;top:${imgCircleTop}px;height:calc(${imgTop}px - ${imgCircleTop}px);left:calc(${imgCircleLeft}px - var(--page-margin) + ${
      imgCircleWidth / 2
    }px - ${
      strokeWidth / 2
    }px);background:rgb(0,0,0,.1);width:${strokeWidth}px;z-index:-1`;
    div.classList.add("connector");
    body.append(div);
  });
};

drawImageLinks(offset, removeElementsByClass);

window.addEventListener("resize", () => {
  drawImageLinks(offset, removeElementsByClass);
});
