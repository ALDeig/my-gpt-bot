function displayMessage(text, className) {
  const messageDiv = document.createElement("div");
  const chatContainer = document.querySelector(".chat-container");
  messageDiv.className = "message " + className;
  messageDiv.insertAdjacentHTML("afterbegin", text);
  chatContainer.appendChild(messageDiv);
  const codeBlocks = messageDiv.querySelectorAll(".highlight");
  codeBlocks.forEach((codeBlock) => {
    if (codeBlock) {
      addButtonCopy(codeBlock);
    }
  });

  addCopyFunctionality();

  chatContainer.scrollTop = chatContainer.scrollHeight;
}

function addButtonCopy(preElement) {
  const button = document.createElement("button");
  button.className = "copy-btn";
  button.textContent = "Копировать";

  preElement.prepend(button);
}

function addCopyFunctionality() {
  const copyButtons = document.querySelectorAll(".copy-btn");
  if (copyButtons.length === 0) {
    return;
  }
  copyButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const codeBlock = button.nextElementSibling;
      const codeText = codeBlock.innerText;

      navigator.clipboard
        .writeText(codeText)
        .then(() => {
          button.textContent = "Скопировано!";
          setTimeout(() => {
            button.textContent = "Копировать";
          }, 2000);
        })
        .catch((err) => {
          console.error("Ошибка копирования: ", err);
        });
    });
  });
}

export { displayMessage };
