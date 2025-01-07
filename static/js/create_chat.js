import { addChatToList, setCurrentChat } from "./chats_menu";
import { getOrCreateSocket } from "./sockets";

async function menuCreateChat(modalOverlay) {
  // функция сбора данных для создания нового чата
  modalOverlay.style.display = "flex";
  const modelList = document.querySelector(".model-options");
  modelList.innerHTML = "";
  sessionStorage.setItem("selectedModel", null);

  const models = await getModels();
  addModelsInList(modelList, models);

  const modelOptions = document.querySelectorAll(".model-option");
  modelOptions.forEach((option) => {
    option.addEventListener("click", (e) => selectModel(e));
  });
}

function selectModel(e) {
  // функция выбора модели
  const modelOptions = document.querySelectorAll(".model-option");
  modelOptions.forEach((opt) => opt.classList.remove("selected"));
  e.currentTarget.classList.add("selected");
  sessionStorage.setItem("selectedModel", e.currentTarget.dataset.modelId);
}

async function getModels() {
  // функция получения списка моделей
  const response = await fetch("/ai_models");
  const models = await response.json();
  return models;
}

function addModelsInList(modelList, models) {
  // функция добавления модели в список для отображения
  models.forEach((model) => {
    const div = document.createElement("div");
    div.className = "model-option";
    div.setAttribute("data-model-id", model.id);
    div.innerHTML = `
        <h3>${model.model}</h3>
        <p>${model.description}</p>
    `;
    modelList.appendChild(div);
  });
}

async function createChat(userId) {
  // функция создания нового чата
  const chat = await newChatOnServer(userId);
  const modalOverlay = document.querySelector(".modal-overlay");
  const currentChat = document.querySelector("#currentModel");
  const chatContainer = document.querySelector(".chat-container");
  const chatList = document.querySelector(".chat-list");
  setCurrentChat(chat.id);
  getOrCreateSocket(chat.id);
  addChatToList(chatList, chat);
  currentChat.textContent = `${chat.id}. ${chat.model}`;
  chatContainer.innerHTML = "";
  modalOverlay.style.display = "none";
}

async function newChatOnServer(userId) {
  // функция создания нового чата на сервере
  const selectModel = sessionStorage.getItem("selectedModel");
  const chatData = {
    modelId: selectModel,
    userId: userId,
  };
  console.log(chatData);
  const resp = await fetch("/new_chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=utf-8",
    },
    body: JSON.stringify(chatData),
  });
  const newChat = await resp.json();
  return newChat;
}

export { createChat, menuCreateChat };
