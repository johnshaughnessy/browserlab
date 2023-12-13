const messageList = document.getElementById("message-list");

async function main() {
  const { replies } = await browser.runtime.sendMessage({ action: "read" });
  console.log(replies);

  // Empty the message list
  while (messageList.firstChild) {
    messageList.removeChild(messageList.firstChild);
  }

  // Iterate backwards through the messages, and add them to the list
  replies.reverse().forEach(({ reply, timestamp }) => {
    // Create a list item composed of both the timestamp and the reply as children

    console.log("timestamp:", timestamp);
    console.log("reply:", reply);
    const li = document.createElement("li");

    li.appendChild(
      document.createTextNode(new Date(timestamp).toLocaleString()),
    );
    li.appendChild(document.createElement("br"));
    li.appendChild(document.createTextNode(reply));
    messageList.appendChild(li);
  });
}

main();
