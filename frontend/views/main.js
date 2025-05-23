const startButton = document.getElementById("start-button");
const urlInput = document.getElementById("video-url");
const inputScreen = document.getElementById("input-screen");
const chatScreen = document.getElementById("chat-screen");

// Function to validate YouTube URL
// This regex checks for both youtube.com and youtu.be formats
function isValidYouTubeURL(url) {
  return /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$/.test(url);
}

// Function to show error message
function showError(msg) {
  const errorElement = document.getElementById("error-message");
  errorElement.textContent = msg;
  errorElement.classList.add("visible");
}

// Function to hide error message
function hideError() {
  document.getElementById("error-message").classList.remove("visible");
}

async function processVideo(videoUrl) {
  const res = await fetch("http://localhost:8000/videos", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url: videoUrl }),
  });
  return res;
}

startButton.addEventListener("click", async () => {
  const videoUrl = urlInput.value;
  if (!isValidYouTubeURL(videoUrl)) {
    showError("Please enter a valid YouTube URL.");
    return;
  }
  hideError();
  startButton.disabled = true;
  urlInput.disabled = true;
  const inputSpinner = document.getElementById("input-spinner");
  inputSpinner.classList.add("visible");
  const res = await processVideo(videoUrl).then((res) => {
    if (res.status === 200) {
      console.log("Video processed successfully");
      inputScreen.classList.add("hidden");
      chatScreen.classList.remove("hidden");
    } else {
      console.error("Error processing video");
    }
  });
});
