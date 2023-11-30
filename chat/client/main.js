const chatHistory = document.getElementById("chat-history");
const chatTextArea = document.getElementById("chat-textarea");
const sendButton = document.getElementById("send-button");

function ChatHistoryMessage(message) {
  const messageElement = document.createElement("div");
  messageElement.classList.add("chat-history-message");
  messageElement.innerText = message;
  return messageElement;
}

function send() {
  const message = chatTextArea.value;
  chatTextArea.value = "";

  chatHistory.appendChild(ChatHistoryMessage(message));

  // Scroll to the bottom of the chatHistory
  chatHistory.scrollTop = chatHistory.scrollHeight;

  // TODO: Send the message to the server
  console.log("Message sent to server: " + message);
}

sendButton.addEventListener("click", send);
// Also send the message when the user presses enter
// in the chat text area, but not shift+enter
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
    send();
  }
});
