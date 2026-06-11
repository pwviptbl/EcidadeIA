const state = {
  activeConversationId: window.INITIAL_CONVERSATION_ID,
  conversations: [],
  messages: [],
  busy: false,
};

const els = {
  sidebar: document.getElementById("sidebar"),
  menuBtn: document.getElementById("menuBtn"),
  newChatBtn: document.getElementById("newChatBtn"),
  conversationList: document.getElementById("conversationList"),
  messages: document.getElementById("messages"),
  form: document.getElementById("chatForm"),
  input: document.getElementById("messageInput"),
  sendBtn: document.getElementById("sendBtn"),
  statusText: document.getElementById("statusText"),
  deleteDialog: document.getElementById("deleteDialog"),
  deleteDialogText: document.getElementById("deleteDialogText"),
  cancelDeleteBtn: document.getElementById("cancelDeleteBtn"),
  confirmDeleteBtn: document.getElementById("confirmDeleteBtn"),
};

let pendingDeleteConversationId = null;

function escapeHtml(value) {
  return String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderMarkdownLite(text) {
  const escaped = escapeHtml(text);
  return escaped.replace(/```([a-z]*)\n([\s\S]*?)```/g, (_match, lang, code) => {
    return `<pre><code>${code.trim()}</code></pre>`;
  });
}

function renderConversations() {
  els.conversationList.innerHTML = "";
  state.conversations.forEach((conversation) => {
    const item = document.createElement("div");
    item.className = "conversation-item" + (conversation.id === state.activeConversationId ? " active" : "");

    const button = document.createElement("button");
    button.type = "button";
    button.className = "conversation-title";
    button.textContent = conversation.title || "Nova conversa";
    button.addEventListener("click", () => loadMessages(conversation.id));

    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.className = "conversation-delete";
    deleteButton.title = "Excluir conversa";
    deleteButton.setAttribute("aria-label", "Excluir conversa");
    deleteButton.textContent = "×";
    deleteButton.addEventListener("click", (event) => {
      event.stopPropagation();
      openDeleteDialog(conversation.id);
    });

    item.appendChild(button);
    item.appendChild(deleteButton);
    els.conversationList.appendChild(item);
  });
}

function renderMessages() {
  els.messages.innerHTML = "";

  if (!state.messages.length) {
    els.messages.innerHTML = `
      <div class="empty-state">
        <h2>Agente externo conectado ao e-Cidade</h2>
        <p>Use uma pergunta ou escolha uma acao rapida. O agente mantem a inteligencia aqui e consulta o e-Cidade apenas como fonte read-only.</p>
      </div>
    `;
    return;
  }

  state.messages.forEach((message) => {
    const row = document.createElement("article");
    row.className = `message ${message.role}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.innerHTML = renderMarkdownLite(message.content);

    row.appendChild(bubble);
    els.messages.appendChild(row);
  });

  els.messages.scrollTop = els.messages.scrollHeight;
}

function setBusy(busy) {
  state.busy = busy;
  els.sendBtn.disabled = busy;
  els.sendBtn.textContent = busy ? "Enviando" : "Enviar";
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: {"Content-Type": "application/json"},
    ...options,
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.message || `HTTP ${response.status}`);
  }
  return payload;
}

async function bootstrap() {
  const payload = await api("/api/bootstrap");
  state.activeConversationId = payload.active_conversation.id;
  state.conversations = payload.conversations;
  state.messages = payload.messages;
  renderConversations();
  renderMessages();
  refreshHealth();
}

async function refreshHealth() {
  try {
    const payload = await api("/api/health");
    if (payload.ok) {
      const service = payload.ecidade.service || payload.ecidade.database?.database || "MCP online";
      els.statusText.textContent = `Fonte online: ${service}`;
    } else {
      els.statusText.textContent = `e-Cidade indisponivel: ${payload.ecidade.message}`;
    }
  } catch (error) {
    els.statusText.textContent = `Falha ao consultar status: ${error.message}`;
  }
}

async function loadMessages(conversationId) {
  state.activeConversationId = conversationId;
  const payload = await api(`/api/conversations/${conversationId}/messages`);
  state.messages = payload.messages;
  renderConversations();
  renderMessages();
  els.sidebar.classList.remove("open");
}

async function createConversation() {
  const conversation = await api("/api/conversations", {method: "POST", body: "{}"});
  state.activeConversationId = conversation.id;
  state.conversations.unshift(conversation);
  state.messages = [];
  renderConversations();
  renderMessages();
  els.input.focus();
}

function openDeleteDialog(conversationId) {
  const conversation = state.conversations.find((item) => item.id === conversationId);
  const title = conversation?.title || "esta conversa";
  pendingDeleteConversationId = conversationId;
  els.deleteDialogText.textContent = `Excluir "${title}" do historico local?`;
  els.deleteDialog.hidden = false;
  els.confirmDeleteBtn.focus();
}

function closeDeleteDialog() {
  pendingDeleteConversationId = null;
  els.deleteDialog.hidden = true;
}

async function confirmDeleteConversation() {
  if (!pendingDeleteConversationId) {
    return;
  }

  const conversationId = pendingDeleteConversationId;
  els.confirmDeleteBtn.disabled = true;
  els.confirmDeleteBtn.textContent = "Excluindo";

  const payload = await api(`/api/conversations/${conversationId}`, {method: "DELETE"});
  state.activeConversationId = payload.active_conversation.id;
  state.conversations = payload.conversations;
  state.messages = payload.messages;
  els.confirmDeleteBtn.disabled = false;
  els.confirmDeleteBtn.textContent = "Excluir";
  closeDeleteDialog();
  renderConversations();
  renderMessages();
}

async function sendMessage(message) {
  const text = message.trim();
  if (!text || state.busy) {
    return;
  }

  state.messages.push({role: "user", content: text});
  renderMessages();
  els.input.value = "";
  setBusy(true);

  try {
    const payload = await api("/api/chat", {
      method: "POST",
      body: JSON.stringify({
        conversation_id: state.activeConversationId,
        message: text,
      }),
    });
    state.conversations = payload.conversations;
    state.messages = payload.messages;
    renderConversations();
    renderMessages();
  } catch (error) {
    state.messages.push({role: "assistant", content: `Falha: ${error.message}`});
    renderMessages();
  } finally {
    setBusy(false);
    els.input.focus();
  }
}

els.form.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(els.input.value);
});

els.input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendMessage(els.input.value);
  }
});

document.querySelectorAll("[data-prompt]").forEach((button) => {
  button.addEventListener("click", () => sendMessage(button.dataset.prompt || ""));
});

els.newChatBtn.addEventListener("click", createConversation);
els.menuBtn.addEventListener("click", () => els.sidebar.classList.toggle("open"));
els.cancelDeleteBtn.addEventListener("click", closeDeleteDialog);
els.confirmDeleteBtn.addEventListener("click", () => {
  confirmDeleteConversation().catch((error) => {
    els.confirmDeleteBtn.disabled = false;
    els.confirmDeleteBtn.textContent = "Excluir";
    state.messages.push({role: "assistant", content: `Falha ao excluir conversa: ${error.message}`});
    renderMessages();
    closeDeleteDialog();
  });
});
els.deleteDialog.addEventListener("click", (event) => {
  if (event.target === els.deleteDialog) {
    closeDeleteDialog();
  }
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !els.deleteDialog.hidden) {
    closeDeleteDialog();
  }
});

bootstrap().catch((error) => {
  els.statusText.textContent = `Falha ao iniciar: ${error.message}`;
});
