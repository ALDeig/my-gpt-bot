import { displayMessage } from "./dialog";

const sockets = {};

function openSocket(chatId) {
  if (chatId in sockets) {
    return;
  }
  const ws = new WebSocket(`wss://${window.location.host}/communicate/${chatId}`);
  setSocket(chatId, ws);
  ws.onopen = function () {
    console.log("Connected to WebSocket server");
  };
  ws.onmessage = getMessage;
  ws.onclose = function () {
    console.log("Disconnected from WebSocket server");
  };
  ws.onerror = function (error) {
    console.error("WebSocket error:", error);
  };
}

function setSocket(chatId, socket) {
  sockets[chatId] = socket;
}

function sendMessage() {
  const textarea = document.querySelector("textarea");
  const chatId = sessionStorage.getItem("currentChatId");
  const message = textarea.value.trim();
  const ws = sockets[chatId];
  if (message) {
    displayMessage(message, "user-message");
    ws.send(
      JSON.stringify({
        type: "message",
        text: message,
      }),
    );
    textarea.value = "";
    textarea.style.height = "auto";
  }
}

function getMessage(event) {
  const message = JSON.parse(event.data);
  displayMessage(message.text, "bot-message");
}

export { openSocket, sendMessage };
