const notes = [
  "eighth_note.svg",
  "eighth_notes.svg",
  "half_note.svg",
  "half_note_d.svg",
  "quarter_note_d.svg",
  "quarter_note_u.svg",
  "quarter_rest.svg",
  "sixteenth_notes.svg",
];

const imageDiv = document.querySelector(".section__wrapper");
const rotationRange = 20;
const disRange = 15;

const birdSings = () => {
  let randomNote = notes[Math.floor(Math.random() * notes.length)];
  let image = new Image();
  image.src = `/static/img/notes/${randomNote}`;
  image.classList+='animated-svg';
  let rotation = Math.round(Math.random()*rotationRange*(Math.random() < 0.5 ? -1 : 1));
  let xdis = Math.round(Math.random()*disRange*(Math.random() < 0.5 ? -1 : 1));
  image.style.transform= `rotate(${rotation}deg) translateX(calc(${xdis}px + 50%))`;
  imageDiv.appendChild(image);

  setTimeout(()=>image.remove(), 5000);
};
