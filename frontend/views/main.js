const startButton = document.getElementById("start-button");
const urlInput = document.getElementById("video-url");
const inputScreen = document.getElementById("input-screen");
const chatScreen = document.getElementById("chat-screen");

// Function to generate a unique ID
function generateUniqueId() {
  return 'id-' + Date.now().toString(36) + '-' + Math.random().toString(36).substr(2, 9);
}

// Function to validate YouTube URL
// This regex checks for both youtube.com and youtu.be formats
function isValidYouTubeURL(url) {
  return /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$/.test(url);
}

function getVideoIdFromUrl(url) {
  if (url.includes("youtube.com/watch?v=")) {
    const videoId = url.split("v=")[1].split("&")[0];
    return videoId;
  } else if (url.includes("youtu.be/")) {
    const videoId = url.split("/")[-1];
    return videoId;
  } else {
    console.error("Invalid YouTube URL");
    return null;
  }
}

// Format Youtube URL to embed
function formatYouTubeEmbedUrl(url) {
  const videoId = getVideoIdFromUrl(url);
  return `https://www.youtube.com/embed/${videoId}?autoplay=1&mute=1`;
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

async function processQuery(query, videoId) {
  const res = await fetch("http://localhost:8000/query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query: query, video_id: videoId }),
  });
  return res.json();
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
      const videoPlayer = document.getElementById("video-player");
      videoPlayer.src = formatYouTubeEmbedUrl(videoUrl);
      videoPlayer.dataset.videoId = getVideoIdFromUrl(videoUrl);
    } else {
      console.error("Error processing video");
    }
  });
});

urlInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    startButton.click();
  }
});


const sendButton = document.getElementById("send-button");
const chatMessages = document.getElementById("chat-messages");
const chatInput = document.getElementById("chat-input");
const videoPlayer = document.getElementById("video-player");

// Initialize the Messages Array
const messages = [];

// Function to add a message to the chat
function addMessage(role, content) {
  const id = generateUniqueId();
  messages.push({ role, content, id });
  renderMessages();
  return id;
}

function updatePendingMessage(id, content) {
  const pendingMessage = document.getElementById(id);
  if (!pendingMessage) {
    return;
  }
  const intervalId = pendingMessage.dataset.typingInterval;
  if (intervalId) {
    clearInterval(intervalId);
  }
  pendingMessage.textContent = content;
}

function animateTypingDots(messageId) {
  const message = document.getElementById(messageId);
  if (!message) {
    return;
  }

  let dotCount = 0;

  const interval = setInterval(() => {
    dotCount = (dotCount + 1) % 3; // cycle: 0, 1, 2
    message.textContent = ".".repeat(dotCount + 1);
  }, 500);

  // Store interval ID on the element for later cleanup
  message.dataset.typingInterval = interval;
}

function renderMessages() {
  chatMessages.innerHTML = "";
  messages.forEach((message) => {
    const messageElement = document.createElement("div");
    messageElement.className = `${message.role}-message`;
    messageElement.textContent = message.content;
    messageElement.id = message.id;
    chatMessages.appendChild(messageElement);
  });
}

sendButton.addEventListener("click", async () => {
  if (chatInput.value.trim() === "") {
    return;
  }
  addMessage("user", chatInput.value);
  const pendingMessageId = addMessage("assistant", "...");
  animateTypingDots(pendingMessageId);

  chatInput.value = "";
  chatInput.disabled = true;
  sendButton.disabled = true;

  try {
    const assistantResponse = await processQuery(chatInput.value, videoPlayer.dataset.videoId);
    updatePendingMessage(pendingMessageId, assistantResponse.response);
  } catch (error) {
    console.error("Error processing query:", error);
    addMessage("assistant", "An error occurred while processing your query.");
  } finally {
    chatInput.disabled = false;
    sendButton.disabled = false;
    chatInput.focus();
  }
});

chatInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    document.getElementById("send-button").click();
  }
});
