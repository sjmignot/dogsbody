var post_names = {{ post_names|safe }}
var post_name = post_names[Math.floor(Math.random()*post_names.length)];
window.onload = function() {
  document.getElementById("dice").parentElement.href=`/post/{post_name}`;
}
