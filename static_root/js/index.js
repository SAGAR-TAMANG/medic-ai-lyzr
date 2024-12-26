function showPage(page) {
  document.querySelector("#page-2").classList.add("d-none");
  document.querySelector("#page-1").classList.add("d-none");
  document.querySelector("#page-3").classList.add("d-none");

  document.querySelector(`#${page}`).classList.remove("d-none");
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("#menu").forEach((button) => {
    button.addEventListener("click", function () {
      document.querySelectorAll("#menu").forEach((button) => {
        button.classList.remove("btn-outline-primary");
        button.classList.add("btn-primary");
      });
      showPage(this.dataset.page);
      this.classList.add("btn-outline-primary");

      this.classList.remove("btn-primary");
      this.classList.add("btn-outline-primary");
    });
  });

  // Begins the DROP effect

  const dropArea = document.getElementById("dropArea");
  const dropArea2 = document.getElementById("dropArea2");

  dropArea.addEventListener("click", (e) => {
    document.getElementById("fileInput").click();
  });

  dropArea.addEventListener("mouseover", (e) => {
    dropArea.style.cursor = "pointer";
    dropArea.style.backgroundColor = "rgba(0, 0, 0, 0.1)";
  });

  dropArea.addEventListener("mouseleave", (e) => {
    dropArea.style.cursor = "auto";
    dropArea.style.backgroundColor = "rgba(0, 0, 0, 0 )";
  });

  dropArea2.addEventListener("mouseover", (e) => {
    dropArea2.style.cursor = "pointer";
    dropArea2.style.backgroundColor = "rgba(0, 0, 0, 0.1)";
  });

  dropArea2.addEventListener("mouseleave", (e) => {
    dropArea2.style.cursor = "auto";
    dropArea2.style.backgroundColor = "rgba(0, 0, 0, 0 )";
  });

  dropArea2.addEventListener("click", (e) => {
    document.getElementById("fileInput").click();
  });

  // Prevent default behavior for all drag events
  ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    dropArea.addEventListener(eventName, preventDefaults, false);
    dropArea2.addEventListener(eventName, preventDefaults, false);
  });

  // Highlight drop area when a file is dragged over it
  ["dragenter", "dragover"].forEach((eventName) => {
    dropArea.addEventListener(eventName, highlight, false);
    dropArea2.addEventListener(eventName, highlight, false);
  });

  // Remove highlight when a file is dragged out of the drop area
  ["dragleave", "drop"].forEach((eventName) => {
    dropArea.addEventListener(eventName, unhighlight, false);
    dropArea2.addEventListener(eventName, unhighlight, false);
  });

  // Handle dropping files
  dropArea.addEventListener("drop", handleDrop, false);
  dropArea2.addEventListener("drop", handleDrop, false);

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  function highlight(e) {
    dropArea.classList.add("bg-primary", "text-white");
    dropArea2.classList.add("bg-primary", "text-white");
  }

  function unhighlight(e) {
    dropArea.classList.remove("bg-primary", "text-white");
    dropArea2.classList.remove("bg-primary", "text-white");
  }

  // Handle dropped files here
  function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    console.log("DROPPED");

    const dt = e.dataTransfer;
    const files = dt.files;
    var file = files[0];
    
    console.log("Selected file:", file);
    const fileInput = document.getElementById("fileInput");
    fileInput.files = files;

    displayLoadingScreen();

    const form = document.getElementById("Uploadform");
    form.submit();
  }
});

var typed = new Typed("#autotype", {
  strings: [
    "Welcome to our medical report summarization tool.",
    "This tool helps you to understand your medical reports better.",
    "Easily summarize complex medical information with this AI-powered tool.",
    "Get key insights from your medical reports in a simplified format.",
  ],
  typeSpeed: 25,
  backSpeed: 25,
  smartBackspace: true,
  loop: true,
});

searchSpace = document.getElementById("search_space");
submitBtn = document.getElementById("submitBtn");

searchSpace.addEventListener("keypress", function (e) {
  if (e.key == "Enter") {
    console.log("Enter");
    e.preventDefault();
    submitBtn.click();
  }
});

function handleFileUpload(files) {
  if (files.length > 0) {
    var file = files[0];
    console.log("Selected file:", file);
    displayLoadingScreen();
    document.getElementById("Uploadform").submit();
  }
}

function takePicture() {
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then(function (stream) {
      var video = document.createElement("video");
      document.body.appendChild(video);
      video.srcObject = stream;
      video.play();

      // Create a canvas element to capture the picture
      var canvas = document.createElement("canvas");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      var context = canvas.getContext("2d");

      // Capture the picture from the video stream after a delay
      setTimeout(function () {
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        // Convert the picture to a data URL and trigger download
        var pictureDataUrl = canvas.toDataURL("image/jpeg");
        var link = document.createElement("a");
        link.href = pictureDataUrl;
        link.download = "picture.jpg";
        link.click();
        // Cleanup
        video.pause();
        stream.getVideoTracks()[0].stop();
        document.body.removeChild(video);
      }, 1000); // Adjust the delay as needed
    })
    .catch(function (error) {
      console.error("Error accessing camera:", error);
    });
}
