# Agent Before Ambulance - Frontend Deployment Guide

## 🚀 Production Deployment Checklist

### 1. Environment Configuration

The frontend automatically detects the environment:
- **Development**: Uses `http://localhost:8001` when running on localhost
- **Production**: Auto-configures based on deployment URL

To customize the API URL for production, edit `app.js`:
```javascript
const CONFIG = {
    API_URL: 'https://your-backend-api.com'  // Update this
};
```

### 2. Build Optimization (Optional)

For production, consider:
- Minifying JavaScript and CSS
- Compressing images
- Enabling gzip/brotli compression on server

### 3. PWA Setup

#### Generate Icons
You need to create app icons in the `/icons/` directory:
- icon-72x72.png
- icon-96x96.png
- icon-128x128.png
- icon-144x144.png
- icon-152x152.png
- icon-192x192.png
- icon-384x384.png
- icon-512x512.png

Use a tool like [PWA Asset Generator](https://www.pwabuilder.com/imageGenerator) or create them manually.

#### Favicon Files
Place in the root directory:
- favicon-16x16.png
- favicon-32x32.png
- apple-touch-icon.png (180x180)

### 4. Deployment Options

#### Option A: Static Hosting (Netlify, Vercel, GitHub Pages)

1. **Netlify**:
   ```bash
   # Install Netlify CLI
   npm install -g netlify-cli
   
   # Deploy
   cd frontend
   netlify deploy --prod
   ```

2. **Vercel**:
   ```bash
   # Install Vercel CLI
   npm install -g vercel
   
   # Deploy
   cd frontend
   vercel --prod
   ```

3. **GitHub Pages**:
   - Push frontend folder to a GitHub repository
   - Enable GitHub Pages in repository settings
   - Set source to main branch / docs folder

#### Option B: Traditional Web Server (Apache, Nginx)

1. **Nginx Configuration**:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       root /var/www/agent-before-ambulance/frontend;
       index index.html;

       # Enable gzip compression
       gzip on;
       gzip_types text/css application/javascript application/json;

       # Cache static assets
       location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
           expires 1y;
           add_header Cache-Control "public, immutable";
       }

       # SPA fallback
       location / {
           try_files $uri $uri/ /index.html;
       }

       # Security headers
       add_header X-Frame-Options "SAMEORIGIN" always;
       add_header X-Content-Type-Options "nosniff" always;
       add_header X-XSS-Protection "1; mode=block" always;
   }
   ```

2. **Apache Configuration** (.htaccess):
   ```apache
   # Enable compression
   <IfModule mod_deflate.c>
       AddOutputFilterByType DEFLATE text/html text/css application/javascript
   </IfModule>

   # Cache static assets
   <IfModule mod_expires.c>
       ExpiresActive On
       ExpiresByType image/png "access plus 1 year"
       ExpiresByType text/css "access plus 1 year"
       ExpiresByType application/javascript "access plus 1 year"
   </IfModule>

   # Security headers
   Header set X-Frame-Options "SAMEORIGIN"
   Header set X-Content-Type-Options "nosniff"
   Header set X-XSS-Protection "1; mode=block"
   ```

#### Option C: Docker Deployment

Create `Dockerfile` in frontend directory:
```dockerfile
FROM nginx:alpine
COPY . /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Deploy:
```bash
docker build -t aba-frontend .
docker run -d -p 80:80 aba-frontend
```

### 5. HTTPS/SSL Setup

**Always use HTTPS in production!**

- **Let's Encrypt** (Free): Use Certbot
  ```bash
  sudo certbot --nginx -d yourdomain.com
  ```

- **Cloudflare**: Free SSL with CDN benefits

### 6. Performance Optimization

1. **Enable CDN**: Use Cloudflare or similar
2. **Lazy Loading**: Already implemented for fonts
3. **Service Worker** (Optional): Add for offline support
4. **Image Optimization**: Compress all images

### 7. Monitoring & Analytics

Add to `index.html` before `</head>`:

```html
<!-- Google Analytics (Optional) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### 8. Testing Before Deployment

```bash
# Test locally with production-like server
npx serve frontend -p 8080

# Check PWA readiness
# Use Chrome DevTools > Lighthouse > PWA audit

# Test on mobile devices
# Use Chrome DevTools > Device Mode
```

### 9. Post-Deployment Checklist

- [ ] Test on multiple browsers (Chrome, Firefox, Safari, Edge)
- [ ] Test on mobile devices (iOS, Android)
- [ ] Verify PWA installability
- [ ] Check HTTPS certificate
- [ ] Test offline behavior
- [ ] Verify API connectivity
- [ ] Check console for errors
- [ ] Test voice recognition
- [ ] Verify responsive design
- [ ] Run Lighthouse audit (aim for 90+ scores)

### 10. Environment Variables

For different environments, create config files:

**config.dev.js**:
```javascript
window.APP_CONFIG = {
    API_URL: 'http://localhost:8001'
};
```

**config.prod.js**:
```javascript
window.APP_CONFIG = {
    API_URL: 'https://api.yourdomain.com'
};
```

Load appropriate config in `index.html`:
```html
<script src="config.prod.js"></script>
```

## 🔒 Security Considerations

1. **Content Security Policy**: Add to HTML
   ```html
   <meta http-equiv="Content-Security-Policy" 
         content="default-src 'self'; 
                  connect-src 'self' https://api.yourdomain.com;
                  style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
                  font-src 'self' https://fonts.gstatic.com;">
   ```

2. **CORS**: Ensure backend allows your frontend domain

3. **Rate Limiting**: Implement on backend

4. **Input Validation**: Already handled in app.js

## 📱 PWA Installation

Users can install the app:
- **Desktop**: Click install icon in address bar
- **Mobile**: "Add to Home Screen" from browser menu

## 🐛 Troubleshooting

### Issue: API not connecting
- Check `CONFIG.API_URL` in app.js
- Verify CORS settings on backend
- Check browser console for errors

### Issue: Voice recognition not working
- Ensure HTTPS (required for microphone access)
- Check browser compatibility (Chrome/Edge recommended)
- Verify microphone permissions

### Issue: PWA not installing
- Ensure HTTPS
- Verify manifest.json is accessible
- Check all required icons exist
- Run Lighthouse PWA audit

## 📊 Performance Targets

- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3.5s
- **Lighthouse Performance**: > 90
- **Lighthouse Accessibility**: > 95
- **Lighthouse Best Practices**: > 90
- **Lighthouse SEO**: > 90
- **Lighthouse PWA**: > 90

---

**Ready for deployment! 🎉**
