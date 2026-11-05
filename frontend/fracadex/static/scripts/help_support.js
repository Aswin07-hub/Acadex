
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const chatMessages = document.getElementById("chatMessages");
const sendButton = document.getElementById("sendButton");
const newChatButton = document.getElementById("newChatButton");

let conversationId = null;

// Display messages in chat
function addMessage(sender, message) {
    const wrapper = document.createElement("div");

    wrapper.className = sender === "AI"
        ? "message ai-message"
        : "message student-message";

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = sender === "AI" ? "A" : "S";

    const content = document.createElement("div");
    content.className = "message-content";

    const name = document.createElement("span");
    name.textContent = sender === "AI"
        ? "ACADEX Assistant"
        : "You";

    const paragraph = document.createElement("p");
    paragraph.textContent = message;

    content.appendChild(name);
    content.appendChild(paragraph);

    wrapper.appendChild(avatar);
    wrapper.appendChild(content);

    chatMessages.appendChild(wrapper);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Send student message
chatForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    addMessage("STUDENT", message);

    messageInput.value = "";
    sendButton.disabled = true;
    sendButton.textContent = "Sending...";

    const formData = new URLSearchParams();

    formData.append("message", message);

    if (conversationId) {
        formData.append("conversation_id", conversationId);
    }

    try {
        const response = await fetch(SEND_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": document.querySelector(
                    "[name=csrfmiddlewaretoken]"
                )?.value || ""
            },
            body: formData
        });

        // Read server response
        let result;

        try {
            result = await response.json();
        } catch {
            throw new Error(
                `Invalid server response. HTTP ${response.status}`
            );
        }

        // Check server errors
        if (!response.ok || !result.success) {
            console.error(
                "ACADEX API Error:",
                response.status,
                result
            );

            throw new Error(
                result.message || `Server error: ${response.status}`
            );
        }

        // Save conversation ID
        conversationId = result.conversation_id;

        // Display AI response
        addMessage("AI", result.answer);

    } catch (error) {
        console.error("Support Chat Error:", error);

        addMessage(
            "AI",
            error.message || "Something went wrong. Please try again."
        );

    } finally {
        sendButton.disabled = false;
        sendButton.textContent = "Send";
        messageInput.focus();
    }
});

// Suggestion buttons
document.querySelectorAll(".suggestion").forEach(button => {
    button.addEventListener("click", function () {
        messageInput.value = this.textContent.trim();
        messageInput.focus();
    });
});

// Start a new conversation
newChatButton.addEventListener("click", function () {
    conversationId = null;

    chatMessages.innerHTML = "";

    addMessage(
        "AI",
        "Hello! Welcome to ACADEX Help & Support. How can I help you today?"
    );
});

// Load previous chat history
async function loadSupportHistory() {
    try {
        const response = await fetch(HISTORY_URL);

        const result = await response.json();

        if (!response.ok || !result.success) {
            console.error("History API Error:", result);
            return;
        }

        if (
            Array.isArray(result.conversations) &&
            result.conversations.length > 0
        ) {
            const latest = result.conversations[0];

            conversationId = latest.conversation_id;

            chatMessages.innerHTML = "";

            latest.messages.forEach(message => {
                addMessage(
                    message.sender,
                    message.message
                );
            });
        }

    } catch (error) {
        console.error(
            "Unable to load support history:",
            error
        );
    }
}

// Load chat history when page opens
loadSupportHistory();
