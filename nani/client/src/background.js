import { io } from "socket.io-client";

console.log("background.js loaded");

//const socket = { on: console.log, emit: console.log }; //
const socket = io(`http://osai.lan:7007`);
socket.on("connect", () => {
  console.log("connected");
});

socket.on("disconnect", () => {
  console.log("disconnected");
});

const replies = [];

socket.on("message", (raw) => {
  // Ignore the message if its length is zero
  if (raw.length === 0) {
    console.warn("Received empty message.");
    return;
  }

  // Limit the number of replies to 10
  if (replies.length > 10) {
    replies.shift();
  }

  console.log("Got reply from server:", raw.substring(0, 50));
  replies.push({ reply: JSON.parse(raw).reply, timestamp: Date.now() });
});

socket.on("error", (error) => {
  console.error(error);
});

//socket.emit("message", JSON.stringify({ text: "hello world!" }));

let fullContext = "";

browser.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message.action === "context") {
    fullContext = message.context;
    console.log("Updated context.");
  } else if (message.action === "read") {
    sendResponse({ replies });
  }
});

const MAX_CONTEXT_LENGTH = 300;
function narrowContext(context, focus) {
  // If the context is shorter than MAX_CONTEXT_LENGTH, return it
  if (context.length <= MAX_CONTEXT_LENGTH) {
    return context;
  }

  const focusIndex = context.indexOf(focus);
  if (focusIndex === -1) {
    console.warn("Couldn't find focus in context.");
    return context.slice(0, MAX_CONTEXT_LENGTH);
  }

  const start = Math.max(0, focusIndex - MAX_CONTEXT_LENGTH / 2);
  const end = Math.min(context.length, focusIndex + MAX_CONTEXT_LENGTH / 2);
  return context.slice(start, end);
}

function onContextMenuClicked(info, _tab) {
  console.log("info:", info);
  if (info.menuItemId === "nani") {
    const focus = info.selectionText;
    const context = narrowContext(fullContext, focus);
    ask(focus, context);
  }
}

async function ask(focus, context) {
  socket.emit("message", JSON.stringify({ text: focus, focus, context }));
}

browser.contextMenus.create({
  id: "nani",
  title: "Nani",
  contexts: ["selection"],
});

browser.contextMenus.onClicked.addListener(onContextMenuClicked);
