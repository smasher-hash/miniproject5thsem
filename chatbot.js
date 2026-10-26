
const chatToggle = document.getElementById("chatbot-toggle");
const chatPanel = document.getElementById("chatbot-panel");
const chatClose = document.getElementById("chatbot-close");
const chatForm = document.getElementById("chatbot-form");
const chatInput = document.getElementById("chatbot-input");
const chatMessages = document.getElementById("chatbot-messages");
const chatSend = document.getElementById("chatbot-send");

chatToggle.addEventListener("click", () => {
  chatPanel.hidden = false;
  chatToggle.hidden = true;
  chatInput.focus();
});

chatClose.addEventListener("click", () => {
  chatPanel.hidden = true;
  chatToggle.hidden = false;
});

function addChatMessage(text, sender) {
  const message = document.createElement("div");
  message.className = `chat-message ${sender}-message`;

  // Use textContent to safely display text from the AI.
  message.textContent = text;

  chatMessages.appendChild(message);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return message;
}

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const message = chatInput.value.trim();
  if (!message || chatSend.disabled) return;

  addChatMessage(message, "user");
  chatInput.value = "";
  chatSend.disabled = true;

  const loading = addChatMessage("Thinking...", "bot");

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Unable to get a response.");
    }

    loading.textContent = data.reply;
  } catch (error) {
    loading.textContent =
      error.message || "Connection problem. Please try again.";
  } finally {
    chatSend.disabled = false;
    chatInput.focus();
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
});
