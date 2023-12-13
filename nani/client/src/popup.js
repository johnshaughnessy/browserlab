const messageList = document.getElementById("message-list");

async function main() {
  const replies = await browser.runtime.sendMessage({ action: "read" });
  console.log(replies);

  // Empty the message list
  while (messageList.firstChild) {
    messageList.removeChild(messageList.firstChild);
  }

  // Iterate backwards through the messages, and add them to the list
  replies.replies.reverse().forEach((reply) => {
    const li = document.createElement("li");
    li.textContent = reply;
    messageList.appendChild(li);
  });
}

main();
