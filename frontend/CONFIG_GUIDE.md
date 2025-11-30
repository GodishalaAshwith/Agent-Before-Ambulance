# Environment Configuration - Quick Reference

## 📦 Files Created

1. ✅ **`.env.example`** - Environment variables template (for build tools)
2. ✅ **`config.example.js`** - JavaScript config template (for static sites)
3. ✅ **`ENV_SETUP.md`** - Comprehensive setup guide
4. ✅ **`.gitignore`** - Updated to exclude config files

---

## 🚀 Quick Start

### Option 1: Static Site (No Build Tools) - RECOMMENDED

**For simple deployment to Netlify, Vercel, GitHub Pages:**

1. **Copy the example**:
   ```bash
   cp config.example.js config.js
   ```

2. **Edit `config.js`**:
   ```javascript
   window.APP_CONFIG = {
       API_URL: 'https://your-backend-api.com',  // ← Change this
       ENV: 'production',
       DEBUG: false,
   };
   ```

3. **Include in `index.html`** (before app.js):
   ```html
   <script src="config.js"></script>
   <script src="app.js"></script>
   ```

4. **Update `app.js`** (line 6):
   ```javascript
   const CONFIG = window.APP_CONFIG || {
       API_URL: window.location.hostname === 'localhost' 
           ? 'http://localhost:8001'
           : window.location.origin.replace(':8080', ':8001'),
       MAX_RETRIES: 3,
       RETRY_DELAY: 1000,
       SESSION_STORAGE_KEY: 'aba_session_id'
   };
   ```

5. **Deploy!** 🎉

---

### Option 2: With Build Tools (Vite/Webpack)

**For projects using bundlers:**

1. **Install Vite**:
   ```bash
   npm init -y
   npm install -D vite
   ```

2. **Copy `.env.example`**:
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env`**:
   ```env
   VITE_API_URL=https://your-backend-api.com
   VITE_ENV=production
   ```

4. **Update `app.js`** to use env vars:
   ```javascript
   const CONFIG = {
       API_URL: import.meta.env.VITE_API_URL || 'http://localhost:8001',
       MAX_RETRIES: parseInt(import.meta.env.VITE_MAX_RETRIES) || 3,
   };
   ```

5. **Build and deploy**:
   ```bash
   npm run build
   ```

---

## 🎯 What to Configure

### Minimum Required
- `API_URL` - Your backend API endpoint

### Commonly Changed
- `ENV` - Environment name (development/production)
- `DEBUG` - Enable/disable debug logs
- `MAX_RETRIES` - API retry attempts
- `SPEECH_LANG` - Language for voice recognition

### Optional
- Analytics IDs
- Feature flags
- UI customization
- Security settings

---

## 📝 Configuration Values

### Development
```javascript
API_URL: 'http://localhost:8001'
ENV: 'development'
DEBUG: true
```

### Production
```javascript
API_URL: 'https://api.yourdomain.com'
ENV: 'production'
DEBUG: false
```

---

## 🔒 Security

### ✅ DO
- Add `config.js` to `.gitignore` ✓ (already done)
- Use different configs for dev/prod
- Keep `.env.example` as template only
- Never commit API keys

### ❌ DON'T
- Commit `config.js` or `.env` with secrets
- Hardcode production URLs in code
- Share production config files
- Store passwords in config

---

## 🧪 Testing

**Verify config is loaded:**
```javascript
// In browser console
console.log('Config:', CONFIG);
console.log('API URL:', CONFIG.API_URL);
```

**Expected output:**
```
Config: {API_URL: "https://...", MAX_RETRIES: 3, ...}
API URL: https://your-backend-api.com
```

---

## 🐛 Troubleshooting

### Config not loading
1. Check `config.js` exists
2. Verify it's included in `index.html` BEFORE `app.js`
3. Check browser console for errors

### Wrong API URL
1. Check `CONFIG.API_URL` in console
2. Verify `config.js` has correct URL
3. Clear browser cache

### Environment variables not working
1. Ensure using Vite or similar build tool
2. Prefix with `VITE_` (for Vite)
3. Restart dev server after changing `.env`

---

## 📚 Full Documentation

For detailed instructions, see:
- **[ENV_SETUP.md](./ENV_SETUP.md)** - Complete setup guide
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Deployment instructions
- **[CHECKLIST.md](./CHECKLIST.md)** - Deployment checklist

---

## 🎯 Recommended Approach

For **most users** deploying to Netlify/Vercel/GitHub Pages:
👉 **Use Option 1 (JavaScript Config)** - Simple and works everywhere!

For **advanced users** with build pipelines:
👉 **Use Option 2 (Environment Variables)** - More flexible and secure

---

**Need help?** Check [ENV_SETUP.md](./ENV_SETUP.md) for detailed instructions!
