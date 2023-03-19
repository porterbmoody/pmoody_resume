const inputMessage = document.querySelector(".input-message");
const sendButton = document.querySelector(".send-button");
const chatContainer = document.querySelector(".chat-container");

function sendUserMessage() {
  const message = inputMessage.value.trim();
  if (message !== "") {
    const userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.textContent = message;
    chatContainer.appendChild(userMessage);
    inputMessage.value = "";
    
    const botMessage = document.createElement("div");
    botMessage.className = "bot-message";
    botMessage.textContent = message;
    chatContainer.appendChild(botMessage);
    botMessage.value = "";
  }
}

function handleKeyDown(event) {
  if (event.key === "Enter") {
    sendUserMessage();
  }
}

sendButton.addEventListener("click", sendUserMessage);
inputMessage.addEventListener("keydown", handleKeyDown);
