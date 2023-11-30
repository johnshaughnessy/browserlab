const WebSocket = require("ws");
const server = new WebSocket.Server({ port: 8003 });

server.on("connection", (ws) => {
  ws.on("message", (message) => {
    message = JSON.parse(message);
    console.log(`Received message:`, message);
    message.isNewMessage = true;

    // Send the message to the LLM and stream the response back to the client

    ws.send(JSON.stringify(message));
  });

  ws.send(
    JSON.stringify({ message: "Connected to server", isNewMessage: true }),
  );
});
