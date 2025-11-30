/**
 * Frontend Configuration
 * 
 * For static sites without build tools:
 * 1. Copy this file to config.js
 * 2. Update values for your environment
 * 3. Include in index.html BEFORE app.js:
 *    <script src="config.js"></script>
 *    <script src="app.js"></script>
 * 
 * For sites with build tools (Vite, Webpack):
 * Use .env files instead (see .env.example)
 */

window.APP_CONFIG = {
    // ===========================================
    // API Configuration
    // ===========================================
    
    /**
     * Backend API URL
     * Development: 'http://localhost:8001'
     * Production: 'https://api.yourdomain.com'
     */
    API_URL: 'http://localhost:8001',
    
    /**
     * API Request Timeout (milliseconds)
     */
    API_TIMEOUT: 10000,
    
    /**
     * Maximum API Retry Attempts
     */
    MAX_RETRIES: 3,
    
    /**
     * Retry Delay (milliseconds)
     */
    RETRY_DELAY: 1000,
    
    // ===========================================
    // Application Settings
    // ===========================================
    
    /**
     * Application Name
     */
    APP_NAME: 'Agent Before Ambulance',
    
    /**
     * Application Version
     */
    APP_VERSION: '1.0.0',
    
    /**
     * Environment
     * Options: 'development', 'staging', 'production'
     */
    ENV: 'development',
    
    /**
     * Enable Debug Mode
     */
    DEBUG: true,
    
    // ===========================================
    // Feature Flags
    // ===========================================
    
    FEATURES: {
        /**
         * Enable Voice Recognition
         */
        VOICE_RECOGNITION: true,
        
        /**
         * Enable Speech Synthesis
         */
        SPEECH_SYNTHESIS: true,
        
        /**
         * Enable Session Persistence
         */
        SESSION_PERSISTENCE: true,
        
        /**
         * Enable Offline Detection
         */
        OFFLINE_DETECTION: true,
        
        /**
         * Enable Toast Notifications
         */
        NOTIFICATIONS: true,
        
        /**
         * Enable Animations
         */
        ANIMATIONS: true,
    },
    
    // ===========================================
    // Speech Settings
    // ===========================================
    
    SPEECH: {
        /**
         * Recognition Language
         */
        LANG: 'en-US',
        
        /**
         * Confidence Threshold (0.0 - 1.0)
         * Lower = more permissive, Higher = more strict
         */
        CONFIDENCE_THRESHOLD: 0.5,
        
        /**
         * Synthesis Rate (0.1 - 10)
         * Lower = slower, Higher = faster
         */
        RATE: 0.9,
        
        /**
         * Synthesis Pitch (0 - 2)
         */
        PITCH: 1.0,
        
        /**
         * Synthesis Volume (0 - 1)
         */
        VOLUME: 1.0,
    },
    
    // ===========================================
    // Session Configuration
    // ===========================================
    
    SESSION: {
        /**
         * LocalStorage Key for Session ID
         */
        STORAGE_KEY: 'aba_session_id',
        
        /**
         * Session Timeout (milliseconds)
         * 0 = no timeout
         */
        TIMEOUT: 0,
    },
    
    // ===========================================
    // UI Configuration
    // ===========================================
    
    UI: {
        /**
         * Notification Auto-Dismiss Duration (milliseconds)
         */
        NOTIFICATION_DURATION: 5000,
        
        /**
         * Theme Color
         */
        THEME_COLOR: '#ef4444',
        
        /**
         * Background Color
         */
        BG_COLOR: '#0f172a',
    },
    
    // ===========================================
    // Analytics (Optional)
    // ===========================================
    
    ANALYTICS: {
        /**
         * Google Analytics Measurement ID
         * Set to null to disable
         */
        GA_MEASUREMENT_ID: null,
        
        /**
         * Enable Analytics
         */
        ENABLED: false,
    },
    
    // ===========================================
    // Error Tracking (Optional)
    // ===========================================
    
    ERROR_TRACKING: {
        /**
         * Sentry DSN
         * Set to null to disable
         */
        SENTRY_DSN: null,
        
        /**
         * Enable Error Tracking
         */
        ENABLED: false,
    },
    
    // ===========================================
    // Security
    // ===========================================
    
    SECURITY: {
        /**
         * Force HTTPS Redirect
         * Only enable in production
         */
        FORCE_HTTPS: false,
        
        /**
         * Allowed Origins (for CORS)
         */
        ALLOWED_ORIGINS: [
            'http://localhost:8001',
            'http://localhost:8000',
        ],
    },
};

// Freeze config to prevent modifications
Object.freeze(window.APP_CONFIG);
Object.freeze(window.APP_CONFIG.FEATURES);
Object.freeze(window.APP_CONFIG.SPEECH);
Object.freeze(window.APP_CONFIG.SESSION);
Object.freeze(window.APP_CONFIG.UI);
Object.freeze(window.APP_CONFIG.ANALYTICS);
Object.freeze(window.APP_CONFIG.ERROR_TRACKING);
Object.freeze(window.APP_CONFIG.SECURITY);
