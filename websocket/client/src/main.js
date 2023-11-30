import { io } from "socket.io-client";

const status = document.getElementById("status");
const socket = io(`http://${window.location.hostname}:8005`);
socket.on("connect", () => {
  console.log("connected");
  status.innerText = "connected";
});

socket.on("disconnect", () => {
  console.log("disconnected");
  status.innerText = "disconnected";
});

socket.on("message", (message) => {
  console.log(message);
});

socket.on("error", (error) => {
  console.error(error);
});

socket.emit("message", JSON.stringify({ text: "hello world!" }));
