import { displayMessage } from "./dialog";
import { getSocket } from "./sockets";

async function fillChatList(userId) {
  const chats = await getChats(userId);
  showChats(chats);
}

async function showChats(chats) {
  const chatList = document.querySelector(".chat-list");
  chats.forEach((chat) => addChatToList(chatList, chat));
}

async function getChats(userId) {
  const resp = await fetch(`/chats?user_id=${userId}`);
  const chats = await resp.json();
  return chats;
}

function addChatToList(chatList, chat) {
  const newChatItem = document.createElement("div");
  newChatItem.className = "chat-item";
  newChatItem.id = chat.id;
  newChatItem.innerHTML = `
        <span>${chat.id}. ${chat.model}</span>
        <button class="delete-chat-btn" id="${chat.id}">
            <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" height="16" width="16">
                <path d="M3 6h18"></path>
                <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
                <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
            </svg>
        </button>
    `;
  chatList.appendChild(newChatItem);
  const newDeleteBtn = newChatItem.querySelector(".delete-chat-btn");
  newDeleteBtn.addEventListener("click", async function (e) {
    e.stopPropagation();
    newChatItem.remove();
    await deleteChat(chat.id);
  });
  newChatItem.addEventListener("click", async function () {
    await selectChat(chat.id);
  });
}

async function selectChat(chatId) {
  const sidebar = document.querySelector(".sidebar");
  const resp = await fetch(`/chats/${chatId}`);
  const chat = await resp.json();
  getSocket(chat.id);
  const chatContainer = document.querySelector(".chat-container");
  const currentChat = document.querySelector("#currentModel");
  currentChat.textContent = `${chat.id}. ${chat.model}`;
  chatContainer.innerHTML = "";
  chat.messages.forEach((message) =>
    displayMessage(
      message.content,
      message.role == "assistant" ? "bot-message" : "user-message",
    ),
  );
  setCurrentChat(chat.id);
  sidebar.classList.toggle("active");
}

async function deleteChat(chatId) {
  const resp = await fetch(`/chats/${chatId}`, {
    method: "DELETE",
  });
  const chats = await resp.json();
  return chats;
}

function setCurrentChat(chatId) {
  // функция установки текущего чата
  sessionStorage.setItem("currentChatId", chatId);
  const textarea = document.querySelector("textarea");
  const sendButton = document.querySelector(".send-btn");
  textarea.disabled = false;
  sendButton.disabled = false;
}

export { addChatToList, fillChatList, setCurrentChat };
