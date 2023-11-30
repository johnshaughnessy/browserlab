const chatHistory = document.getElementById("chat-history");
const chatTextArea = document.getElementById("chat-textarea");
const sendButton = document.getElementById("send-button");

function ChatHistoryMessage(message) {
  const messageElement = document.createElement("div");
  messageElement.classList.add("chat-history-message");
  messageElement.innerText = message;
  return messageElement;
}

const socket = new WebSocket(`ws://${window.location.hostname}:8003/chat`);

socket.addEventListener("open", (event) => {
  console.log("Connected to server");
});
socket.addEventListener("close", (event) => {
  console.log("Disconnected from server");
});

let nextChatMessage = ChatHistoryMessage("Hello!");
chatHistory.appendChild(nextChatMessage);
socket.addEventListener("message", (event) => {
  console.log("Received message from server:", event.data);
  const message = JSON.parse(event.data);

  if (message.isNewMessage) {
    nextChatMessage = ChatHistoryMessage("");
    chatHistory.appendChild(nextChatMessage);
  }

  nextChatMessage.innerText += message.message;
  // We don't scroll to the bottom while the server is sending us messages.
});

function sendChatMessage() {
  const message = chatTextArea.value;
  chatTextArea.value = "";

  chatHistory.appendChild(ChatHistoryMessage(message));

  // Scroll to the bottom of the chatHistory
  chatHistory.scrollTop = chatHistory.scrollHeight;

  // Send the message to the server
  socket.send(JSON.stringify({ message })); // This will be sent as a JSON string

  console.log("Message sent to server: " + message);
}

let isShiftPressed = false;
chatTextArea.addEventListener("keydown", (event) => {
  if (event.key === "Shift") {
    isShiftPressed = true;
  }
});
chatTextArea.addEventListener("keyup", (event) => {
  if (event.key === "Shift") {
    isShiftPressed = false;
  }
});
chatTextArea.addEventListener("input", (event) => {
  if (event.inputType === "insertLineBreak" && !isShiftPressed) {
    sendChatMessage();
  }
});
sendButton.addEventListener("click", sendChatMessage);
