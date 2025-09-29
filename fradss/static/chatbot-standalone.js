/**
 * Standalone FRA Chatbot Integration for React Landing Page
 * This script can be added to any HTML page to integrate the chatbot
 */

(function() {
    'use strict';
    
    // Inject chatbot styles
    function injectStyles() {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '/static/chatbot.css';
        document.head.appendChild(link);
    }
    
    // Inject Material Icons if not present
    function injectMaterialIcons() {
        if (!document.querySelector('link[href*="material-icons"]')) {
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = 'https://fonts.googleapis.com/icon?family=Material+Icons';
            document.head.appendChild(link);
        }
    }
    
    // Load chatbot scripts
    function loadChatbotScripts() {
        return new Promise((resolve) => {
            let scriptsLoaded = 0;
            const scriptsNeeded = 2;
            
            function onScriptLoad() {
                scriptsLoaded++;
                if (scriptsLoaded === scriptsNeeded) {
                    resolve();
                }
            }
            
            // Load chatbot data
            const dataScript = document.createElement('script');
            dataScript.src = '/static/chatbot-data.js';
            dataScript.onload = onScriptLoad;
            document.head.appendChild(dataScript);
            
            // Load chatbot main script
            const mainScript = document.createElement('script');
            mainScript.src = '/static/chatbot.js';
            mainScript.onload = onScriptLoad;
            document.head.appendChild(mainScript);
        });
    }
    
    // Initialize chatbot
    async function initChatbot() {
        try {
            // Wait a bit for any React rendering to complete
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // Initialize with landing page context
            if (window.initializeFRAChatbot) {
                window.initializeFRAChatbot('landing');
            }
        } catch (error) {
            console.warn('Chatbot initialization error:', error);
        }
    }
    
    // Main initialization function
    async function init() {
        injectMaterialIcons();
        injectStyles();
        await loadChatbotScripts();
        await initChatbot();
    }
    
    // Start initialization when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();