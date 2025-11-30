// ============================================
// Configuration
// ============================================
const CONFIG = {
    // Auto-detect API URL based on environment
    API_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:8001'  // Development
        : window.location.origin.replace(':8080', ':8001'),  // Production (adjust port if needed)
    MAX_RETRIES: 3,
    RETRY_DELAY: 1000,
    SESSION_STORAGE_KEY: 'aba_session_id'
};

// ============================================
// State Management
// ============================================
const state = {
    sessionId: null,
    recognition: null,
    isRecording: false,
    isProcessing: false,
    isOnline: navigator.onLine,
    retryCount: 0
};

// ============================================
// DOM Elements
// ============================================
const elements = {
    chatContainer: document.getElementById('chat-container'),
    micButton: document.getElementById('mic-button'),
    statusText: document.getElementById('status'),
    connectionStatus: document.getElementById('connection-status')
};

// ============================================
// Session Management
// ============================================
async function initSession() {
    try {
        // Try to restore session from localStorage
        const savedSessionId = localStorage.getItem(CONFIG.SESSION_STORAGE_KEY);
        if (savedSessionId) {
            state.sessionId = savedSessionId;
            console.log('Restored session:', savedSessionId);
            updateStatus('Session restored', 'success');
            return;
        }

        // Create new session
        updateStatus('Connecting...', 'info');
        const response = await fetchWithRetry(`${CONFIG.API_URL}/new-session`, {
            method: 'POST'
        });
        
        const data = await response.json();
        state.sessionId = data.session_id;
        localStorage.setItem(CONFIG.SESSION_STORAGE_KEY, state.sessionId);
        
        console.log('New session initialized:', state.sessionId);
        updateStatus('Connected', 'success');
        
        // Clear status after 2 seconds
        setTimeout(() => updateStatus('Ready', 'ready'), 2000);
    } catch (error) {
        console.error('Failed to init session:', error);
        updateStatus('Connection failed', 'error');
        addMessage('agent', '⚠️ Unable to connect to the server. Please check your connection and try again.');
        updateConnectionStatus(false);
    }
}

// ============================================
// Speech Recognition Setup
// ============================================
function initSpeechRecognition() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        showNotification('Speech recognition is not supported in this browser. Please use Chrome or Edge.', 'warning');
        elements.micButton.disabled = true;
        elements.micButton.style.opacity = '0.5';
        return false;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    state.recognition = new SpeechRecognition();
    state.recognition.continuous = false;
    state.recognition.interimResults = false;
    state.recognition.lang = 'en-US';

    state.recognition.onstart = () => {
        state.isRecording = true;
        elements.micButton.classList.add('listening');
        elements.micButton.setAttribute('aria-label', 'Listening... Release to stop');
        updateStatus('Listening...', 'listening');
    };

    state.recognition.onend = () => {
        state.isRecording = false;
        elements.micButton.classList.remove('listening');
        elements.micButton.setAttribute('aria-label', 'Hold to speak');
        
        if (!state.isProcessing) {
            updateStatus('Ready', 'ready');
        }
    };

    state.recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        const confidence = event.results[0][0].confidence;
        
        console.log('User said:', transcript, 'Confidence:', confidence);
        
        if (confidence > 0.5) {
            addMessage('user', transcript);
            sendMessage(transcript);
        } else {
            updateStatus('Could not understand. Please try again.', 'warning');
            setTimeout(() => updateStatus('Ready', 'ready'), 2000);
        }
    };
    
    state.recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        state.isRecording = false;
        elements.micButton.classList.remove('listening');
        
        let errorMessage = 'Error: ';
        switch (event.error) {
            case 'no-speech':
                errorMessage += 'No speech detected';
                break;
            case 'audio-capture':
                errorMessage += 'Microphone not found';
                break;
            case 'not-allowed':
                errorMessage += 'Microphone permission denied';
                showNotification('Please allow microphone access to use voice input.', 'error');
                break;
            default:
                errorMessage += event.error;
        }
        
        updateStatus(errorMessage, 'error');
        setTimeout(() => updateStatus('Ready', 'ready'), 3000);
    };

    return true;
}

// ============================================
// Recording Controls
// ============================================
function startRecording() {
    if (!state.isOnline) {
        showNotification('You are offline. Please check your internet connection.', 'error');
        return;
    }

    if (state.recognition && !state.isRecording && !state.isProcessing) {
        try {
            state.recognition.start();
        } catch (e) {
            console.error('Failed to start recording:', e);
            if (e.name === 'InvalidStateError') {
                // Recognition is already started, stop and restart
                state.recognition.stop();
                setTimeout(() => state.recognition.start(), 100);
            }
        }
    }
}

function stopRecording() {
    if (state.recognition && state.isRecording) {
        state.recognition.stop();
    }
}

// ============================================
// Message Handling
// ============================================
async function sendMessage(text) {
    if (!state.sessionId) {
        await initSession();
        if (!state.sessionId) return; // Still no session, abort
    }

    state.isProcessing = true;
    updateStatus('Processing...', 'processing');

    try {
        const response = await fetchWithRetry(`${CONFIG.API_URL}/agent`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                session_id: state.sessionId, 
                message: text 
            })
        });

        if (response.status === 404) {
            console.log('Session expired. Re-initializing...');
            localStorage.removeItem(CONFIG.SESSION_STORAGE_KEY);
            await initSession();
            
            // Retry with new session
            const retryResponse = await fetchWithRetry(`${CONFIG.API_URL}/agent`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    session_id: state.sessionId, 
                    message: text 
                })
            });
            
            const retryData = await retryResponse.json();
            addMessage('agent', retryData.text);
            speak(retryData.text);
        } else if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        } else {
            const data = await response.json();
            addMessage('agent', data.text);
            speak(data.text);
        }

        updateStatus('Ready', 'ready');
        state.retryCount = 0; // Reset retry count on success
    } catch (error) {
        console.error('API Error:', error);
        handleApiError(error);
    } finally {
        state.isProcessing = false;
    }
}

// ============================================
// Network & Error Handling
// ============================================
async function fetchWithRetry(url, options, retries = CONFIG.MAX_RETRIES) {
    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(url, {
                ...options,
                signal: AbortSignal.timeout(10000) // 10 second timeout
            });
            return response;
        } catch (error) {
            if (i === retries - 1) throw error;
            
            console.log(`Retry ${i + 1}/${retries} after error:`, error.message);
            await new Promise(resolve => setTimeout(resolve, CONFIG.RETRY_DELAY * (i + 1)));
        }
    }
}

function handleApiError(error) {
    state.retryCount++;
    
    let userMessage = '⚠️ ';
    if (error.name === 'AbortError' || error.message.includes('timeout')) {
        userMessage += 'Request timed out. The server might be busy. Please try again.';
    } else if (!state.isOnline) {
        userMessage += 'You appear to be offline. Please check your internet connection.';
    } else if (state.retryCount >= CONFIG.MAX_RETRIES) {
        userMessage += 'Unable to reach the server after multiple attempts. Please try again later.';
    } else {
        userMessage += 'Error communicating with the agent. Retrying...';
    }
    
    addMessage('agent', userMessage);
    updateStatus('Error - Ready to retry', 'error');
}

// ============================================
// UI Helpers
// ============================================
function addMessage(role, text) {
    const div = document.createElement('div');
    div.className = `message ${role}-message`;
    div.textContent = text;
    div.setAttribute('role', 'log');
    div.setAttribute('aria-live', 'polite');
    
    elements.chatContainer.appendChild(div);
    elements.chatContainer.scrollTop = elements.chatContainer.scrollHeight;
}

function updateStatus(text, type = 'ready') {
    elements.statusText.textContent = text;
    elements.statusText.className = `status-text status-${type}`;
}

function updateConnectionStatus(isOnline) {
    state.isOnline = isOnline;
    
    if (elements.connectionStatus) {
        elements.connectionStatus.textContent = isOnline ? '🟢 Online' : '🔴 Offline';
        elements.connectionStatus.className = `connection-status ${isOnline ? 'online' : 'offline'}`;
    }
    
    if (!isOnline) {
        showNotification('You are offline. Some features may not work.', 'warning');
    }
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.setAttribute('role', 'alert');
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => notification.classList.add('show'), 10);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

function speak(text) {
    if ('speechSynthesis' in window) {
        // Cancel any ongoing speech
        window.speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.pitch = 1;
        utterance.volume = 1;
        
        window.speechSynthesis.speak(utterance);
    }
}

// ============================================
// Event Listeners
// ============================================
function setupEventListeners() {
    // Microphone button events
    elements.micButton.addEventListener('mousedown', startRecording);
    elements.micButton.addEventListener('mouseup', stopRecording);
    elements.micButton.addEventListener('touchstart', (e) => { 
        e.preventDefault(); 
        startRecording(); 
    });
    elements.micButton.addEventListener('touchend', (e) => { 
        e.preventDefault(); 
        stopRecording(); 
    });

    // Prevent context menu on long press
    elements.micButton.addEventListener('contextmenu', (e) => e.preventDefault());

    // Online/Offline detection
    window.addEventListener('online', () => {
        updateConnectionStatus(true);
        showNotification('Connection restored', 'success');
        if (!state.sessionId) initSession();
    });

    window.addEventListener('offline', () => {
        updateConnectionStatus(false);
    });

    // Visibility change - pause speech when tab is hidden
    document.addEventListener('visibilitychange', () => {
        if (document.hidden && 'speechSynthesis' in window) {
            window.speechSynthesis.cancel();
        }
    });

    // Keyboard accessibility
    elements.micButton.addEventListener('keydown', (e) => {
        if (e.key === ' ' || e.key === 'Enter') {
            e.preventDefault();
            startRecording();
        }
    });

    elements.micButton.addEventListener('keyup', (e) => {
        if (e.key === ' ' || e.key === 'Enter') {
            e.preventDefault();
            stopRecording();
        }
    });
}

// ============================================
// Initialization
// ============================================
async function init() {
    console.log('🚀 Agent Before Ambulance - Initializing...');
    console.log('Environment:', window.location.hostname);
    console.log('API URL:', CONFIG.API_URL);
    
    // Setup event listeners
    setupEventListeners();
    
    // Initialize speech recognition
    const speechAvailable = initSpeechRecognition();
    if (!speechAvailable) {
        console.warn('Speech recognition not available');
    }
    
    // Initialize session
    await initSession();
    
    // Update connection status
    updateConnectionStatus(navigator.onLine);
    
    console.log('✅ Initialization complete');
}

// Start the application
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
