function send(context) {
  const message = { action: "context", context };
  console.log("message:", message);
  console.log("action:", message.action);
  browser.runtime.sendMessage(message);
}

function gatherContext(e) {
  e.stopPropagation();
  const node = e.target;
  switch (node.type) {
    case "textarea":
      send(node.value);
      break;
    default:
      send(node.innerText);
      break;
  }
}

const nodes = [];

function attachClickListeners() {
  document.querySelectorAll("*").forEach((node) => {
    nodes.push(node);
    node.addEventListener("mousedown", gatherContext);
  });
}

setInterval(() => {
  console.log("content script doing its thing");
  nodes.forEach((node) => {
    node.removeEventListener("mousedown", gatherContext);
  });
  nodes.length = 0;
  attachClickListeners();
}, 5000);

if (document.readyState === "complete") {
  attachClickListeners();
} else {
  document.addEventListener("DOMContentLoaded", attachClickListeners);
}
