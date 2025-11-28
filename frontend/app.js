const chatContainer = document.getElementById('chat-container');
const micButton = document.getElementById('mic-button');
const statusText = document.getElementById('status');

let sessionId = null;
let recognition = null;
let isRecording = false;

// Initialize Session
async function initSession() {
    try {
        const response = await fetch('http://localhost:8001/new-session', { method: 'POST' });
        const data = await response.json();
        sessionId = data.session_id;
        console.log('Session initialized:', sessionId);
    } catch (error) {
        console.error('Failed to init session:', error);
        addMessage('agent', 'Error connecting to server. Please check if the backend is running.');
    }
}

// Initialize Speech Recognition
if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
        isRecording = true;
        micButton.classList.add('listening');
        statusText.textContent = 'Listening...';
    };

    recognition.onend = () => {
        isRecording = false;
        micButton.classList.remove('listening');
        statusText.textContent = 'Processing...';
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        console.log('User said:', transcript);
        addMessage('user', transcript);
        sendMessage(transcript);
    };
    
    recognition.onerror = (event) => {
        console.error('Speech recognition error', event.error);
        statusText.textContent = 'Error: ' + event.error;
        isRecording = false;
        micButton.classList.remove('listening');
    };
} else {
    alert('Web Speech API is not supported in this browser. Please use Chrome or Edge.');
}

// Button Events
micButton.addEventListener('mousedown', startRecording);
micButton.addEventListener('mouseup', stopRecording);
micButton.addEventListener('touchstart', (e) => { e.preventDefault(); startRecording(); });
micButton.addEventListener('touchend', (e) => { e.preventDefault(); stopRecording(); });

function startRecording() {
    if (recognition && !isRecording) {
        try {
            recognition.start();
        } catch (e) {
            console.error(e);
        }
    }
}

function stopRecording() {
    if (recognition && isRecording) {
        recognition.stop();
    }
}

// Send Message to Backend
async function sendMessage(text) {
    if (!sessionId) await initSession();

    try {
        let response = await fetch('http://localhost:8001/agent', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId, message: text })
        });

        if (response.status === 404) {
            console.log('Session expired or not found. Re-initializing...');
            await initSession();
            // Retry once
            response = await fetch('http://localhost:8001/agent', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: sessionId, message: text })
            });
        }
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        addMessage('agent', data.text);
        speak(data.text);
        statusText.textContent = 'Ready';
    } catch (error) {
        console.error('API Error:', error);
        addMessage('agent', 'Error communicating with the agent.');
        statusText.textContent = 'Error';
    }
}

// UI Helpers
function addMessage(role, text) {
    const div = document.createElement('div');
    div.className = `message ${role}-message`;
    div.textContent = text;
    chatContainer.appendChild(div);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function speak(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        window.speechSynthesis.speak(utterance);
    }
}

// Start
initSession();
