const inputMessage = document.querySelector(".input-message");
const sendButton = document.querySelector(".send-button");
const chatContainer = document.querySelector(".chat-container");
const chatForm = document.querySelector("#chat-form");

function sendUserMessage(event) {
  event.preventDefault();
  const message = inputMessage.value.trim();
  if (message !== "") {
    const userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.textContent = message;
    chatContainer.appendChild(userMessage);
    inputMessage.value = "";
    
    // Send user message to server and receive response
    $.ajax({
      type: "POST",
      url: "/process_response",
      data: { message: message },
      success: function(response) {
        const botMessage = document.createElement("div");
        botMessage.className = "bot-message";
        botMessage.textContent = response.message;
        chatContainer.appendChild(botMessage);
      },
      error: function(xhr) {
        console.error(xhr.responseText);
      }
    });

  }
}

function handleKeyDown(event) {
  if (event.key === "Enter") {
    sendUserMessage();
  }
}

chatForm.addEventListener("submit", sendUserMessage);
inputMessage.addEventListener("keydown", handleKeyDown);
