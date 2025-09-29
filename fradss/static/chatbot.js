/**
 * FRA WebGIS Chatbot Implementation
 * Modular chatbot system for Forest Rights Act assistance
 */

class FRAChatbot {
    constructor() {
        this.isOpen = false;
        this.isTyping = false;
        this.messageHistory = [];
        
        this.init();
    }
    
    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.createChatbot());
        } else {
            this.createChatbot();
        }
    }
    
    createChatbot() {
        // Create chatbot HTML structure
        const chatbotHTML = `
            <!-- Chatbot Toggle Button -->
            <button class="chatbot-toggle" id="chatbotToggle">
                <i class="material-icons">chat</i>
            </button>
            
            <!-- Chatbot Container -->
            <div class="chatbot-container" id="chatbotContainer">
                <!-- Header -->
                <div class="chatbot-header">
                    <div class="chatbot-header-info">
                        <div class="chatbot-avatar">
                            <i class="material-icons">support_agent</i>
                        </div>
                        <div class="chatbot-title">
                            <h4>Chitra</h4>
                            <span>Vanachitra.AI helper</span>
                        </div>
                    </div>
                    <button class="chatbot-close" id="chatbotClose">
                        <i class="material-icons">close</i>
                    </button>
                </div>
                
                <!-- Messages Area -->
                <div class="chatbot-messages" id="chatbotMessages">
                    <div class="welcome-message">
                        <i class="material-icons">forest</i>
                        <p>Welcome! I am Chitra - your FRA WebGIS Assistant</p>
                        <p>Ask me about Forest Rights Act claims, states covered, government schemes, or how to use this system.</p>
                    </div>
                </div>
                
                <!-- Input Area -->
                <div class="chatbot-input-area">
                    <div class="chatbot-input-container">
                        <textarea 
                            class="chatbot-input" 
                            id="chatbotInput" 
                            placeholder="Ask me about FRA claims, schemes, or anything else..."
                            rows="1"
                        ></textarea>
                        <button class="chatbot-send" id="chatbotSend">
                            <i class="material-icons">send</i>
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        // Add chatbot to page
        document.body.insertAdjacentHTML('beforeend', chatbotHTML);
        
        // Bind events
        this.bindEvents();
        
        // Add initial greeting after a short delay
        setTimeout(() => {
            this.addBotMessage("Hi! I'm here to help you with Forest Rights Act information. What would you like to know?");
        }, 1000);
    }
    
    bindEvents() {
        const toggle = document.getElementById('chatbotToggle');
        const container = document.getElementById('chatbotContainer');
        const close = document.getElementById('chatbotClose');
        const input = document.getElementById('chatbotInput');
        const send = document.getElementById('chatbotSend');
        
        // Toggle chatbot
        toggle.addEventListener('click', () => this.toggleChatbot());
        close.addEventListener('click', () => this.closeChatbot());
        
        // Send message events
        send.addEventListener('click', () => this.sendMessage());
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto-resize textarea
        input.addEventListener('input', (e) => {
            e.target.style.height = 'auto';
            e.target.style.height = Math.min(e.target.scrollHeight, 80) + 'px';
        });
        
        // Click outside to close
        document.addEventListener('click', (e) => {
            if (this.isOpen && !container.contains(e.target) && !toggle.contains(e.target)) {
                this.closeChatbot();
            }
        });
    }
    
    toggleChatbot() {
        if (this.isOpen) {
            this.closeChatbot();
        } else {
            this.openChatbot();
        }
    }
    
    openChatbot() {
        const toggle = document.getElementById('chatbotToggle');
        const container = document.getElementById('chatbotContainer');
        
        this.isOpen = true;
        toggle.classList.add('active');
        container.classList.add('active');
        
        // Focus input
        setTimeout(() => {
            document.getElementById('chatbotInput').focus();
        }, 300);
    }
    
    closeChatbot() {
        const toggle = document.getElementById('chatbotToggle');
        const container = document.getElementById('chatbotContainer');
        
        this.isOpen = false;
        toggle.classList.remove('active');
        container.classList.remove('active');
    }
    
    sendMessage() {
        const input = document.getElementById('chatbotInput');
        const message = input.value.trim();
        
        if (!message || this.isTyping) return;
        
        // Add user message
        this.addUserMessage(message);
        
        // Clear input
        input.value = '';
        input.style.height = 'auto';
        
        // Process and respond
        this.processMessage(message);
    }
    
    addUserMessage(message) {
        const messagesContainer = document.getElementById('chatbotMessages');
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chatbot-message user';
        messageDiv.innerHTML = `
            <div class="message-content">${this.escapeHtml(message)}</div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Store in history
        this.messageHistory.push({ type: 'user', content: message, timestamp: new Date() });
    }
    
    addBotMessage(message) {
        const messagesContainer = document.getElementById('chatbotMessages');
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chatbot-message bot';
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="material-icons">smart_toy</i>
            </div>
            <div class="message-content">${message}</div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Store in history
        this.messageHistory.push({ type: 'bot', content: message, timestamp: new Date() });
    }
    
    showTypingIndicator() {
        const messagesContainer = document.getElementById('chatbotMessages');
        
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chatbot-message bot typing-indicator';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <i class="material-icons">smart_toy</i>
            </div>
            <div class="message-content">
                <div class="typing-indicator">
                    <span>Thinking</span>
                    <div class="typing-dots">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(typingDiv);
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.remove();
        }
    }
    
    async processMessage(userMessage) {
        this.isTyping = true;
        this.showTypingIndicator();
        
        // Simulate processing delay
        await this.sleep(800 + Math.random() * 1200);
        
        this.hideTypingIndicator();
        
        // Find best response using chatbot data
        let response = "I'm sorry, I couldn't understand that. Could you please rephrase your question or ask about FRA claims, states covered, or government schemes?";
        
        if (window.ChatbotData) {
            const matchedQA = window.ChatbotData.findBestMatch(userMessage);
            if (matchedQA) {
                response = matchedQA.answer;
            } else {
                response = window.ChatbotData.getDefaultResponse();
            }
        }
        
        // Add bot response
        this.addBotMessage(response);
        
        this.isTyping = false;
    }
    
    scrollToBottom() {
        const messagesContainer = document.getElementById('chatbotMessages');
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    // Public methods for external integration
    addCustomMessage(message, isBot = true) {
        if (isBot) {
            this.addBotMessage(message);
        } else {
            this.addUserMessage(message);
        }
    }
    
    clearHistory() {
        const messagesContainer = document.getElementById('chatbotMessages');
        messagesContainer.innerHTML = `
            <div class="welcome-message">
                <i class="material-icons">forest</i>
                <p>Welcome to the FRA WebGIS Assistant!</p>
                <p>Ask me about Forest Rights Act claims, states covered, government schemes, or how to use this system.</p>
            </div>
        `;
        this.messageHistory = [];
    }
    
    getMessageHistory() {
        return this.messageHistory;
    }
    
    // Method to handle specific page context
    setPageContext(pageType) {
        this.pageContext = pageType;
        
        // Add page-specific welcome message
        setTimeout(() => {
            let contextMessage = "";
            
            switch (pageType) {
                case 'landing':
                    contextMessage = "Welcome to the FRA WebGIS portal! I can help you understand the system and navigate to different features.";
                    break;
                case 'map':
                    contextMessage = "You're viewing the FRA claims map. I can help you understand the layers, filtering options, and claim details.";
                    break;
                case 'dss':
                    contextMessage = "You're viewing the Decision Support System. I can explain the analytics, scheme recommendations, and development indicators.";
                    break;
                default:
                    contextMessage = "I'm here to help with any FRA-related questions you might have.";
            }
            
            if (contextMessage) {
                this.addBotMessage(contextMessage);
            }
        }, 1500);
    }
}

// Initialize chatbot when script loads
let fraChatbot = null;

// Initialize function that can be called from pages
function initializeFRAChatbot(pageType = null) {
    if (!fraChatbot) {
        fraChatbot = new FRAChatbot();
        
        if (pageType) {
            // Set page context after chatbot is fully initialized
            setTimeout(() => {
                fraChatbot.setPageContext(pageType);
            }, 500);
        }
    }
    return fraChatbot;
}

// Auto-initialize if Material Icons are available (indicating the page is ready)
function checkAndInitialize() {
    // Check if Material Icons or Font Awesome is loaded
    const iconsLoaded = document.querySelector('link[href*="material-icons"]') || 
                      document.querySelector('link[href*="font-awesome"]') ||
                      window.getComputedStyle(document.createElement('i')).fontFamily.includes('Material Icons');
    
    if (iconsLoaded) {
        initializeFRAChatbot();
    } else {
        // Retry after a short delay
        setTimeout(checkAndInitialize, 500);
    }
}

// Start initialization check
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', checkAndInitialize);
} else {
    checkAndInitialize();
}

// Global access
window.FRAChatbot = FRAChatbot;
window.initializeFRAChatbot = initializeFRAChatbot;