import { fillChatList } from "./chats_menu";
import { menuCreateChat, createChat } from "./create_chat";
import { sendMessage } from "./sockets";

document.addEventListener("DOMContentLoaded", async function () {
  const tg = window.Telegram.WebApp;
  let userId;
  if (tg.initDataUnsafe.user) {
    userId = tg.initDataUnsafe.user.id;
  } else {
    const url = new URL(window.location.href);
    userId = url.searchParams.get("user_id");
  }
  tg.expand();
  await fillChatList(userId);
  addEventListeners(userId);
});

function addEventListeners(userId) {
  // функция добавления обработчиков событий

  const hamburger = document.querySelector(".hamburger");
  const sidebar = document.querySelector(".sidebar");
  const btnNewChat = document.querySelector(".new-chat-btn");
  const modalOverlay = document.querySelector(".modal-overlay");
  const cancelModelBtn = document.querySelector("#cancelModelSelection");
  const confirmModelBtn = document.querySelector("#confirmModelSelection");
  const textarea = document.querySelector("textarea");
  const sendButton = document.querySelector(".send-btn");

  // открыть боковое меню при нажатии на гамбургер
  hamburger.addEventListener("click", function () {
    sidebar.classList.toggle("active");
  });

  // закрыть окно выбора модели при клике вне него
  document.addEventListener("click", function (e) {
    if (!sidebar.contains(e.target) && !hamburger.contains(e.target)) {
      sidebar.classList.remove("active");
    }
  });

  // открыть окно выбора модели при нажатии на кнопку "новый чат"
  btnNewChat.addEventListener("click", async () => {
    await menuCreateChat(modalOverlay);
  });

  // скрыть окно выбора модели при нажатии на кнопку "отмена"
  cancelModelBtn.addEventListener("click", function () {
    modalOverlay.style.display = "none";
  });

  // создать новый чат при нажатии на кнопку "подтвердить"
  confirmModelBtn.addEventListener("click", async function () {
    await createChat(userId);
  });

  textarea.addEventListener("input", function () {
    this.style.height = "auto";
    this.style.height = Math.min(this.scrollHeight, 200) + "px";
  });

  textarea.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  sendButton.addEventListener("click", sendMessage);
}
