const API_URL = 'http://localhost:8000';

// Helper function to escape HTML
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function scrollToBottom() {
    const messagesContainer = document.getElementById('conversation-area');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function adjustTextareaHeight() {
    const textarea = document.getElementById('chatInput');
    if (textarea) {
        textarea.style.height = 'auto';
        const scrollHeight = textarea.scrollHeight;
        textarea.style.height = `${Math.min(scrollHeight, 120)}px`;
    }
}

function showLoadingIndicator() {
    const messagesContainer = document.getElementById('conversation-area');
    const loadingMessage = document.createElement('div');
    loadingMessage.id = 'loading-indicator';
    loadingMessage.className = 'message-container assistant-message-container';
    loadingMessage.innerHTML = `
        <div class="message-content">
            <div class="loading-dots">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>
    `;
    messagesContainer.appendChild(loadingMessage);
    scrollToBottom();
}

function hideLoadingIndicator() {
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) loadingIndicator.remove();
}

function addChatMessage(sender, text, isMarkdown = false) {
    const messagesContainer = document.getElementById('conversation-area');
    const initialMessage = document.getElementById('initial-message');
    if (initialMessage) initialMessage.style.display = 'none';

    const messageContainer = document.createElement('div');
    messageContainer.className = 'message-container';

    const timeHtml = `<div class="message-time">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>`;

    if (sender.toLowerCase() === 'you') {
        messageContainer.classList.add('user-message-container');
        messageContainer.innerHTML = `
            <div class="message-content">${escapeHtml(text)}</div>
            ${timeHtml}
        `;
    } else {
        messageContainer.classList.add('assistant-message-container');

        if (isMarkdown && text) {
            // Render markdown content with proper styling
            const md = marked.parse(text, { 
                breaks: true,
                gfm: true,
                headerIds: false
            });
            
            // Clean up the markdown output and add custom styling
            const cleaned = md
                .replace(/<p>/g, '<p class="md-paragraph">')
                .replace(/<h1>/g, '<h1 class="md-heading">')
                .replace(/<h2>/g, '<h2 class="md-heading">')
                .replace(/<h3>/g, '<h3 class="md-heading">')
                .replace(/<strong>/g, '<strong class="md-bold">')
                .replace(/<em>/g, '<em class="md-italic">')
                .replace(/<ul>/g, '<ul class="md-list">')
                .replace(/<ol>/g, '<ol class="md-list">')
                .replace(/<li>/g, '<li class="md-list-item">')
                .replace(/<code>/g, '<code class="md-code">')
                .replace(/<pre>/g, '<pre class="md-pre">')
                .replace(/<blockquote>/g, '<blockquote class="md-blockquote">');
            
            messageContainer.innerHTML = `
                <div class="message-content markdown-content">${cleaned}</div>
                ${timeHtml}
            `;
        } else {
            // Fallback for plain text
            messageContainer.innerHTML = `
                <div class="message-content">${escapeHtml(text || '')}</div>
                ${timeHtml}
            `;
        }
    }

    messagesContainer.appendChild(messageContainer);
    scrollToBottom();
}

function clearChat() {
    if (!confirm('Are you sure you want to clear the chat history?')) return;
    const messagesContainer = document.getElementById('conversation-area');
    messagesContainer.innerHTML = `
        <div id="initial-message" class="flex flex-col items-center justify-center h-full">
            <div class="w-16 h-16 rounded-full bg-[#20B2AA] flex items-center justify-center mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-8 h-8 text-white">
                    <path d="M9 11H1l3-7 3 7zM21 11h-6l3-7 3 7z"/>
                    <path d="M4 15h16"/>
                    <path d="M2 19h20"/>
                </svg>
            </div>
            <h2 class="text-3xl font-light text-white mb-4">Todo List AI Agent</h2>
            <p class="text-[#888888] text-center max-w-lg leading-relaxed mb-6">
                I'm your friendly AI task manager! I can help you create, organize, and track your tasks with natural language.
            </p>
            <div class="text-[#A0A0A0] text-sm text-center max-w-md">
                <p class="mb-2">Try saying:</p>
                <ul class="space-y-1 text-left">
                    <li>• "Create a task called 'Buy groceries'"</li>
                    <li>• "Show me all my tasks"</li>
                    <li>• "Mark task 1 as complete"</li>
                    <li>• "Update task 2 description"</li>
                </ul>
            </div>
        </div>
    `;
}

async function sendChatMessage() {
    const inputEl = document.getElementById('chatInput');
    const message = inputEl.value.trim();
    if (!message) return;

    addChatMessage('You', message);
    inputEl.value = '';
    document.getElementById('sendChatBtn').disabled = true;

    showLoadingIndicator();

    try {
        const response = await fetch(`${API_URL}/agent/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            const err = await response.json().catch(() => ({}));
            throw new Error(err.reply || `HTTP error ${response.status}`);
        }

        const data = await response.json();
        const reply = data.reply || '';

        if (!reply || reply.trim() === '') {
            addChatMessage('Assistant', "I'm here to help with your tasks! You can ask me to show your tasks, create a new task, or update/delete tasks. What would you like to do?");
        } else {
            addChatMessage('Assistant', reply, true);
        }
    } catch (error) {
        console.error('Error:', error);
        let errMsg = error.message || String(error);
        if (errMsg.includes('Failed to fetch')) {
            errMsg = 'Failed to connect to server. Is the API running?';
        }
        addChatMessage('Assistant', `Sorry, there was an error: ${escapeHtml(errMsg)}`);
    } finally {
        hideLoadingIndicator();
        document.getElementById('sendChatBtn').disabled = false;
    }
}

// DOM bindings
document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('sendChatBtn');
    if (sendButton) sendButton.addEventListener('click', sendChatMessage);

    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendChatMessage();
            }
        });
        chatInput.addEventListener('input', adjustTextareaHeight);
    }

    // Add clear chat button functionality
    const clearButton = document.getElementById('clearChatBtn');
    if (clearButton) {
        clearButton.addEventListener('click', clearChat);
    }

    // small UX: focus input on load
    const inputEl = document.getElementById('chatInput');
    if (inputEl) inputEl.focus();
});
    