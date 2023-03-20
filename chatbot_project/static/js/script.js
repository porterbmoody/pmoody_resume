const inputMessage = document.querySelector(".input-message");
const sendButton = document.querySelector(".send-button");
const chatContainer = document.querySelector(".chat-container");
const chatForm = document.querySelector("#chat-form");

function sendUserMessage(event) {
  event.preventDefault();
  const message = inputMessage.value.trim();
  if (message !== "") {
    console.log(message);
    const userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.textContent = message;
    chatContainer.appendChild(userMessage);
    inputMessage.value = "";
    
    $.ajax({
      type: "POST",
      url: "/process_response",
      contentType: "application/json",
      dataType: 'json',
      data: JSON.stringify({ message: message }),
      success: function(response) {
        console.log("ajax request");
        const botMessage = document.createElement("div");
        botMessage.className = "bot-message";
        botMessage.textContent = response.message;
        chatContainer.appendChild(botMessage);
      },
      error: function(xhr) {
        console.log("epic failure");
        console.error(xhr.responseText);
      }
    });
  }
}

function handleKeyDown(event) {
  if (event.key === "Enter") {
    sendUserMessage(event);
  }
}

chatForm.addEventListener("submit", sendUserMessage);
inputMessage.addEventListener("keydown", handleKeyDown);
