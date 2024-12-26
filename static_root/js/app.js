// Hide loading screen when the page finishes loading
document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("loading-screen").style.display = "flex";
  document.getElementById("body-wrapper").style.display = "none";
});

window.addEventListener("load", function() {
  document.getElementById("loading-screen").style.display = "none";
  document.getElementById("body-wrapper").style.display = "block";
});


const displayLoadingScreen = () => {
  document.getElementById("body-wrapper").style.display = "none";
  document.getElementById("loading-screen").style.display = "flex";
}
