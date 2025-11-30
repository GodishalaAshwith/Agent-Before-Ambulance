# Environment Configuration Guide

This guide explains how to configure the frontend for different environments.

## 📋 Overview

Since this is a **static frontend** (no build process), environment variables work differently than in Node.js applications. We provide two approaches:

1. **JavaScript Config File** (Recommended for static sites)
2. **Environment Variables** (For build tools like Vite/Webpack)

---

## 🎯 Approach 1: JavaScript Config (Recommended)

### For Static Hosting (No Build Tools)

**Best for**: Netlify, Vercel, GitHub Pages, simple web servers

#### Setup Steps

1. **Copy the example config**:
   ```bash
   cp config.example.js config.js
   ```

2. **Edit `config.js`** with your settings:
   ```javascript
   window.APP_CONFIG = {
       API_URL: 'https://api.yourdomain.com',
       ENV: 'production',
       DEBUG: false,
       // ... other settings
   };
   ```

3. **Include in `index.html`** BEFORE `app.js`:
   ```html
   <script src="config.js"></script>
   <script src="app.js"></script>
   ```

4. **Update `app.js`** to use config:
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

5. **Add to `.gitignore`**:
   ```
   config.js
   ```

#### Different Environments

**Development** (`config.dev.js`):
```javascript
window.APP_CONFIG = {
    API_URL: 'http://localhost:8001',
    ENV: 'development',
    DEBUG: true,
};
```

**Production** (`config.prod.js`):
```javascript
window.APP_CONFIG = {
    API_URL: 'https://api.yourdomain.com',
    ENV: 'production',
    DEBUG: false,
};
```

Include the appropriate file in your HTML:
```html
<!-- Development -->
<script src="config.dev.js"></script>

<!-- Production -->
<script src="config.prod.js"></script>
```

---

## 🔧 Approach 2: Environment Variables

### For Build Tools (Vite, Webpack, etc.)

**Best for**: Projects using bundlers/build tools

#### Setup with Vite

1. **Install Vite** (if not already):
   ```bash
   npm install -D vite
   ```

2. **Copy `.env.example`**:
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env`**:
   ```env
   VITE_API_URL=http://localhost:8001
   VITE_ENV=development
   VITE_DEBUG=true
   ```

4. **Create `vite.config.js`**:
   ```javascript
   import { defineConfig } from 'vite';
   
   export default defineConfig({
       root: '.',
       build: {
           outDir: 'dist',
       },
   });
   ```

5. **Update `app.js`** to use env vars:
   ```javascript
   const CONFIG = {
       API_URL: import.meta.env.VITE_API_URL || 'http://localhost:8001',
       MAX_RETRIES: parseInt(import.meta.env.VITE_MAX_RETRIES) || 3,
       DEBUG: import.meta.env.VITE_DEBUG === 'true',
   };
   ```

6. **Add scripts to `package.json`**:
   ```json
   {
       "scripts": {
           "dev": "vite",
           "build": "vite build",
           "preview": "vite preview"
       }
   }
   ```

7. **Run development server**:
   ```bash
   npm run dev
   ```

8. **Build for production**:
   ```bash
   npm run build
   ```

#### Environment Files

- `.env` - Default (committed to git as example)
- `.env.local` - Local overrides (gitignored)
- `.env.development` - Development environment
- `.env.production` - Production environment

---

## 🚀 Deployment Configurations

### Netlify

**Option A: Build Command**
```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "dist"

[build.environment]
  VITE_API_URL = "https://api.yourdomain.com"
  VITE_ENV = "production"
```

**Option B: Environment Variables**
1. Go to Site Settings → Environment Variables
2. Add variables:
   - `VITE_API_URL` = `https://api.yourdomain.com`
   - `VITE_ENV` = `production`

### Vercel

**vercel.json**:
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "env": {
    "VITE_API_URL": "https://api.yourdomain.com",
    "VITE_ENV": "production"
  }
}
```

### GitHub Pages

**GitHub Actions** (`.github/workflows/deploy.yml`):
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
      - run: npm install
      - run: npm run build
        env:
          VITE_API_URL: ${{ secrets.API_URL }}
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

---

## 📝 Configuration Reference

### Required Settings

| Setting | Description | Example |
|---------|-------------|---------|
| `API_URL` | Backend API endpoint | `https://api.yourdomain.com` |
| `ENV` | Environment name | `production` |

### Optional Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `MAX_RETRIES` | API retry attempts | `3` |
| `RETRY_DELAY` | Retry delay (ms) | `1000` |
| `DEBUG` | Enable debug logs | `false` |
| `SPEECH_LANG` | Speech recognition language | `en-US` |
| `NOTIFICATION_DURATION` | Toast duration (ms) | `5000` |

---

## 🔒 Security Best Practices

### DO ✅

- Use environment variables for sensitive data
- Add `.env.local` to `.gitignore`
- Use different configs for dev/prod
- Validate configuration on app start
- Use HTTPS in production

### DON'T ❌

- Commit `.env` files with secrets
- Hardcode API keys in code
- Use production config in development
- Expose sensitive data in client-side code
- Store passwords in environment variables

---

## 🧪 Testing Configuration

### Verify Config is Loaded

Add to browser console:
```javascript
console.log('Config:', CONFIG);
console.log('API URL:', CONFIG.API_URL);
console.log('Environment:', CONFIG.ENV);
```

### Test Different Environments

**Development**:
```bash
# With Vite
npm run dev

# Without build tools
# Use config.dev.js in index.html
```

**Production**:
```bash
# With Vite
npm run build
npm run preview

# Without build tools
# Use config.prod.js in index.html
```

---

## 🐛 Troubleshooting

### Config not loading
- Check file path in `index.html`
- Verify `config.js` exists
- Check browser console for errors

### Environment variables not working
- Ensure using Vite (or similar build tool)
- Prefix with `VITE_` (for Vite)
- Restart dev server after changing `.env`

### API URL incorrect
- Check `CONFIG.API_URL` in console
- Verify environment-specific config
- Check for typos in URL

---

## 📚 Examples

### Minimal Config (Static Site)

**config.js**:
```javascript
window.APP_CONFIG = {
    API_URL: 'https://api.yourdomain.com',
};
```

### Full Config (With Build Tools)

**.env.production**:
```env
VITE_API_URL=https://api.yourdomain.com
VITE_ENV=production
VITE_DEBUG=false
VITE_MAX_RETRIES=3
VITE_ENABLE_ANALYTICS=true
VITE_GA_MEASUREMENT_ID=G-XXXXXXXXXX
```

---

## 🎯 Recommended Setup

### For Quick Deployment
Use **JavaScript Config** approach:
1. Copy `config.example.js` to `config.js`
2. Update `API_URL`
3. Include in `index.html`
4. Deploy!

### For Professional Projects
Use **Environment Variables** with Vite:
1. Set up Vite
2. Create `.env` files
3. Configure deployment platform
4. Use build pipeline

---

**Need help?** Check the [DEPLOYMENT.md](./DEPLOYMENT.md) guide!
