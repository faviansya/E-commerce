$('.carousel').carousel({
  interval: 2000
})

function myFunction() {
  var x = document.getElementById("allItems");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

window.onload = function() {
  document.getElementById('allItems').style.display = 'none';
  document.getElementById('allUser').style.display = 'none';
};

function myFunctionUser() {
  var x = document.getElementById("allUser");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}
