# Agent Before Ambulance - Frontend

Production-ready emergency assistance web application with AI-powered triage, first aid guidance, and ambulance dispatch.

## ✨ Features

- 🎤 **Voice-First Interface**: Hands-free interaction using Web Speech API
- 🤖 **AI-Powered Triage**: Intelligent severity assessment
- 🚑 **Smart Dispatch**: Automatic ambulance coordination
- 📍 **Location Services**: Integrated geocoding
- 💊 **First Aid Guidance**: Step-by-step medical instructions
- 📱 **PWA Support**: Installable on mobile and desktop
- 🌐 **Offline Detection**: Connection status monitoring
- ♿ **Accessible**: WCAG 2.1 compliant
- 📱 **Responsive**: Works on all devices

## 🚀 Quick Start

### Development

```bash
# Serve locally
python -m http.server 8080

# Or use any static server
npx serve . -p 8080
```

Visit `http://localhost:8080`

### Production

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

## 🛠️ Tech Stack

- **HTML5**: Semantic markup with ARIA labels
- **CSS3**: Modern styling with CSS Grid/Flexbox
- **Vanilla JavaScript**: No frameworks, pure ES6+
- **Web Speech API**: Voice recognition and synthesis
- **PWA**: Progressive Web App capabilities

## 📁 File Structure

```
frontend/
├── index.html          # Main HTML file with SEO meta tags
├── app.js              # Application logic with state management
├── style.css           # Responsive styles with animations
├── manifest.json       # PWA manifest
├── DEPLOYMENT.md       # Deployment guide
└── README.md           # This file
```

## 🔧 Configuration

Edit `app.js` to configure:

```javascript
const CONFIG = {
    API_URL: 'http://localhost:8001',  // Backend API URL
    MAX_RETRIES: 3,                     // API retry attempts
    RETRY_DELAY: 1000,                  // Retry delay in ms
    SESSION_STORAGE_KEY: 'aba_session_id'
};
```

## 🎨 Customization

### Colors

Edit CSS variables in `style.css`:

```css
:root {
    --primary-color: #ef4444;
    --accent-color: #3b82f6;
    --bg-color: #0f172a;
    /* ... */
}
```

### Branding

Update `manifest.json` for PWA branding:
- App name
- Icons
- Theme colors
- Description

## 🧪 Testing

### Browser Compatibility

- ✅ Chrome 90+ (Recommended)
- ✅ Edge 90+
- ⚠️ Firefox 88+ (No voice recognition)
- ⚠️ Safari 14+ (Limited voice support)

### Mobile Testing

```bash
# Use Chrome DevTools Device Mode
# Or test on actual devices
```

### PWA Testing

1. Open Chrome DevTools
2. Go to Lighthouse tab
3. Run PWA audit
4. Aim for 90+ score

## 📱 Installation

### Desktop
1. Visit the site in Chrome/Edge
2. Click install icon in address bar
3. App opens in standalone window

### Mobile
1. Visit the site
2. Tap browser menu
3. Select "Add to Home Screen"
4. App icon appears on home screen

## 🔒 Security

- HTTPS required for microphone access
- Content Security Policy headers
- XSS protection
- CORS configured for API
- No sensitive data stored locally

## ♿ Accessibility

- ARIA labels on interactive elements
- Keyboard navigation support
- Screen reader compatible
- High contrast mode support
- Reduced motion support
- Focus indicators

## 📊 Performance

- First Contentful Paint: < 1.5s
- Time to Interactive: < 3.5s
- Lighthouse Score: 90+
- Optimized assets
- Lazy loading
- Minimal dependencies

## 🐛 Troubleshooting

### Voice not working
- Ensure HTTPS connection
- Check microphone permissions
- Use Chrome or Edge browser

### API connection failed
- Verify backend is running
- Check API_URL in app.js
- Inspect browser console

### PWA not installing
- Ensure HTTPS
- Check manifest.json
- Verify all icons exist

## 📝 License

See main project LICENSE file.

## 🤝 Contributing

1. Test on multiple browsers
2. Maintain accessibility
3. Follow existing code style
4. Update documentation

## 📞 Support

For issues, see the main project repository.

---

**Built with ❤️ for emergency response**
