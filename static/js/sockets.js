import { displayMessage } from "./dialog";

const sockets = {};

function setSocket(chatId, socket) {
  sockets[chatId] = socket;
}

function getOrCreateSocket(chatId) {
  const ws = sockets[chatId];
  if (ws && ws.readyState === WebSocket.OPEN) {
    return ws;
  }
  const newSocket = new WebSocket(
    `wss://${window.location.host}/communicate/${chatId}`,
  );
  setSocket(chatId, newSocket);
  newSocket.onopen = function () {
    console.log("Connected to WebSocket server");
  };
  newSocket.onmessage = getMessage;
  newSocket.onclose = function () {
    console.log("Disconnected from WebSocket server");
  };
  newSocket.onerror = function (error) {
    console.error("WebSocket error:", error);
  };
  return newSocket;
}

function sendMessage() {
  const textarea = document.querySelector("textarea");
  const chatId = sessionStorage.getItem("currentChatId");
  const message = textarea.value.trim();
  const ws = getOrCreateSocket(chatId);
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

export { getOrCreateSocket, sendMessage };
