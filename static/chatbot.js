document.addEventListener("DOMContentLoaded", function () {
    const chatbotToggle = document.getElementById("chatbot-toggle");
    const chatbotContainer = document.getElementById("chatbot-container");
    const chatbotClose = document.getElementById("chatbot-close");
    const sendBtn = document.getElementById("send-btn");
    const userInput = document.getElementById("user-input");
    const messagesContainer = document.getElementById("chatbot-messages");

    // Function to toggle chatbot visibility
    function toggleChatbot() {
        chatbotContainer.classList.toggle("hidden");
    }

    // Function to close chatbot
    function closeChatbot() {
        chatbotContainer.classList.add("hidden");
    }

    function addMessage(content, type = "user") {
        const messageDiv = document.createElement("div");
        messageDiv.className = `mb-3 flex ${type === "user" ? "justify-end" : "justify-start"}`;
    
        const messageBubble = document.createElement("div");
        messageBubble.className = `px-4 py-3 max-w-xs md:max-w-md rounded-xl shadow-lg border ${
            type === "user"
                ? "bg-orange-500 text-white border-orange-600"  // User messages (Orange)
                : "bg-white text-gray-900 border-orange-300 prose prose-sm" // Bot messages with Markdown styling
        }`;
    
        // Convert Markdown to HTML and apply custom Tailwind styles
        if (type === "bot") {
            messageBubble.innerHTML = marked.parse(content);
    
            // Apply additional Tailwind classes for better styling
            messageBubble.querySelectorAll("h1").forEach(el => el.classList.add("text-2xl", "font-bold", "text-orange-600", "mb-2"));
            messageBubble.querySelectorAll("h2").forEach(el => el.classList.add("text-xl", "font-semibold", "text-orange-500", "mb-2"));
            messageBubble.querySelectorAll("h3").forEach(el => el.classList.add("text-lg", "font-medium", "text-orange-400", "mb-2"));
            messageBubble.querySelectorAll("ul").forEach(el => el.classList.add("list-disc", "list-inside", "space-y-1"));
            messageBubble.querySelectorAll("ol").forEach(el => el.classList.add("list-decimal", "list-inside", "space-y-1"));
            messageBubble.querySelectorAll("li").forEach(el => el.classList.add("ml-4"));
            messageBubble.querySelectorAll("strong").forEach(el => el.classList.add("font-bold", "text-orange-700"));
            messageBubble.querySelectorAll("em").forEach(el => el.classList.add("italic", "text-gray-600"));
            messageBubble.querySelectorAll("p").forEach(el => el.classList.add("mb-2"));
        } else {
            messageBubble.textContent = content;
        }
    
        messageDiv.appendChild(messageBubble);
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight; // Auto-scroll to latest message
    }
    
    
    // Function to handle message sending
    async function sendMessage() {
        const userMessage = userInput.value.trim();
        if (!userMessage) return;

        addMessage(userMessage, "user");
        userInput.value = "";

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userMessage })
            });

            const data = await response.json();
            addMessage(data.response || "🤖 Sorry, I couldn't understand that.", "bot");
        } catch (error) {
            addMessage("❌ Error fetching response. Please try again.", "bot");
        }
    }

    // Event listeners
    chatbotToggle.addEventListener("click", toggleChatbot);
    chatbotClose.addEventListener("click", closeChatbot);
    sendBtn.addEventListener("click", sendMessage);

    // Allow sending messages with Enter key
    userInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});
