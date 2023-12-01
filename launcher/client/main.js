async function send(route, payload) {
  const res = await fetch(route, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  return res.json();
}

const doodleStatusIndicator = document.getElementById(
  "doodle-status-indicator",
);
const doodleInitButton = document.getElementById("doodle-init-button");
const doodleRunButton = document.getElementById("doodle-run-button");
const doodleStopButton = document.getElementById("doodle-stop-button");
const doodleAnchor = document.getElementById("doodle-anchor");
const doodlePort = 8001;
doodleAnchor.href = `http://${location.hostname}:${doodlePort}`;
doodleInitButton.addEventListener("click", async () => {
  const response = await send("/api/doodle/init");
  console.log(response);
});
doodleRunButton.addEventListener("click", async () => {
  const response = await send("/api/doodle/run");
  console.log(response);
});
doodleStopButton.addEventListener("click", async () => {
  const response = await send("/api/doodle/stop");
  console.log(response);
});

const chatStatusIndicator = document.getElementById("chat-status-indicator");
const chatInitButton = document.getElementById("chat-init-button");
const chatRunButton = document.getElementById("chat-run-button");
const chatStopButton = document.getElementById("chat-stop-button");
const chatAnchor = document.getElementById("chat-anchor");
const chatPort = 8006;
chatAnchor.href = `http://${location.hostname}:${chatPort}`;
chatInitButton.addEventListener("click", async () => {
  const response = await send("/api/chat/init");
  console.log(response);
});
chatRunButton.addEventListener("click", async () => {
  const response = await send("/api/chat/run");
  console.log(response);
});
chatStopButton.addEventListener("click", async () => {
  const response = await send("/api/chat/stop");
  console.log(response);
});

const websocketStatusIndicator = document.getElementById(
  "websocket-status-indicator",
);
const websocketInitButton = document.getElementById("websocket-init-button");
const websocketRunButton = document.getElementById("websocket-run-button");
const websocketStopButton = document.getElementById("websocket-stop-button");
const websocketAnchor = document.getElementById("websocket-anchor");
const websocketPort = 8005;
websocketAnchor.href = `http://${location.hostname}:${websocketPort}`;
websocketInitButton.addEventListener("click", async () => {
  const response = await send("/api/websocket/init");
  console.log(response);
});
websocketRunButton.addEventListener("click", async () => {
  const response = await send("/api/websocket/run");
  console.log(response);
});
websocketStopButton.addEventListener("click", async () => {
  const response = await send("/api/websocket/stop");
  console.log(response);
});

async function updateStatus() {
  const raw = await fetch("/api/status");
  const response = await raw.json();

  doodleStatusIndicator.classList.remove(
    "running",
    "booting",
    "stopped",
    "error",
  );
  doodleStatusIndicator.classList.add(response.doodle);

  chatStatusIndicator.classList.remove(
    "running",
    "booting",
    "stopped",
    "error",
  );
  chatStatusIndicator.classList.add(response.chat);

  websocketStatusIndicator.classList.remove(
    "running",
    "booting",
    "stopped",
    "error",
  );
  websocketStatusIndicator.classList.add(response.websocket);
}

setInterval(updateStatus, 300);
