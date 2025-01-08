import { displayMessage } from "./dialog";

const sockets = {};

function getSocket(chatId) {
  let socket = sockets[chatId];
  if (socket && socket.readyState === WebSocket.OPEN) {
    return socket;
  } else {
    if (socket) {
      socket.close();
    }
    socket = new WebSocket(
      `wss://${window.location.host}/communicate/${chatId}`,
    );
  }
  socket.onopen = () => {
    console.log(`Connected to WebSocket server for chat ${chatId}`);
  };

  socket.onclose = (event) => {
    console.log(
      `Disconnected from WebSocket server for chat ${chatId}. Reason: ${event.reason}`,
    );
    delete sockets[chatId];
  };

  socket.onerror = (error) => {
    console.error("WebSocket error:", error);
  };

  socket.onmessage = (message) => {
    const messageData = JSON.parse(message.data);
    displayMessage(messageData.text, "bot-message");
  };

  sockets[chatId] = socket;
  return socket;
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

export { getSocket, sendMessage };
