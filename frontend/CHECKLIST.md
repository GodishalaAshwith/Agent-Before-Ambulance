# 🚀 Deployment Checklist

Use this checklist to ensure your frontend is ready for production deployment.

## Pre-Deployment

### Configuration
- [ ] Update `API_URL` in `app.js` to point to production backend
- [ ] Verify `manifest.json` has correct app name and description
- [ ] Update `robots.txt` with your actual domain

### Assets (Required for PWA)
- [ ] Create app icons in `/icons/` directory:
  - [ ] icon-72x72.png
  - [ ] icon-96x96.png
  - [ ] icon-128x128.png
  - [ ] icon-144x144.png
  - [ ] icon-152x152.png
  - [ ] icon-192x192.png
  - [ ] icon-384x384.png
  - [ ] icon-512x512.png
- [ ] Create favicon files in root:
  - [ ] favicon-16x16.png
  - [ ] favicon-32x32.png
  - [ ] apple-touch-icon.png (180x180)

### Testing
- [ ] Test locally with `python -m http.server 8080`
- [ ] Test voice recognition (hold mic button)
- [ ] Test on mobile device
- [ ] Test on different browsers (Chrome, Firefox, Safari, Edge)
- [ ] Run Lighthouse audit (aim for 90+ scores)
- [ ] Check browser console for errors
- [ ] Test offline behavior (disconnect network)
- [ ] Verify responsive design on different screen sizes

## Deployment

### Choose Your Platform
- [ ] **Option A**: Netlify (easiest)
  ```bash
  npm install -g netlify-cli
  cd frontend
  netlify deploy --prod
  ```
- [ ] **Option B**: Vercel
  ```bash
  npm install -g vercel
  cd frontend
  vercel --prod
  ```
- [ ] **Option C**: GitHub Pages
  - Push to GitHub
  - Enable Pages in settings
- [ ] **Option D**: Custom server (see DEPLOYMENT.md)

### SSL/HTTPS
- [ ] Set up HTTPS certificate (required for voice features)
- [ ] Use Let's Encrypt (free) or Cloudflare
- [ ] Verify HTTPS is working

### Domain & DNS
- [ ] Configure custom domain (optional)
- [ ] Update DNS records
- [ ] Wait for DNS propagation

## Post-Deployment

### Verification
- [ ] Visit production URL
- [ ] Test voice recognition (requires HTTPS)
- [ ] Test API connectivity
- [ ] Verify PWA installability
- [ ] Check connection status indicator
- [ ] Test on mobile device
- [ ] Verify all pages load correctly

### Performance
- [ ] Run Lighthouse on production URL
- [ ] Check loading times
- [ ] Verify CDN is working (if using)
- [ ] Test from different locations

### SEO
- [ ] Verify meta tags are correct
- [ ] Submit sitemap to Google Search Console
- [ ] Check Open Graph preview (Facebook, LinkedIn)
- [ ] Check Twitter Card preview

### Monitoring (Optional)
- [ ] Set up Google Analytics
- [ ] Configure error tracking (Sentry, etc.)
- [ ] Set up uptime monitoring
- [ ] Configure performance monitoring

## Backend Integration

### API Configuration
- [ ] Backend is deployed and accessible
- [ ] CORS is configured to allow frontend domain
- [ ] API endpoints are working
- [ ] Session management is working
- [ ] Error responses are handled correctly

### Testing Integration
- [ ] Create new session
- [ ] Send test message
- [ ] Verify triage works
- [ ] Test location extraction
- [ ] Test ambulance dispatch
- [ ] Test first aid guidance
- [ ] Verify session persistence

## Security

### Headers
- [ ] Add Content Security Policy (optional)
- [ ] Verify X-Frame-Options
- [ ] Check X-Content-Type-Options
- [ ] Verify HTTPS redirect

### Privacy
- [ ] Add privacy policy (if collecting data)
- [ ] Add terms of service
- [ ] Configure cookie consent (if needed)

## Documentation

- [ ] Update README with production URL
- [ ] Document any custom configuration
- [ ] Add deployment notes
- [ ] Update team on deployment

## Final Checks

- [ ] All features working on production
- [ ] No console errors
- [ ] Mobile experience is smooth
- [ ] Voice recognition works
- [ ] PWA can be installed
- [ ] Performance is acceptable
- [ ] Accessibility is maintained

---

## Quick Test Script

Run these commands in browser console on production:

```javascript
// Check configuration
console.log('API URL:', CONFIG.API_URL);

// Check PWA
console.log('Manifest:', document.querySelector('link[rel="manifest"]'));

// Check HTTPS
console.log('HTTPS:', window.location.protocol === 'https:');

// Check Speech API
console.log('Speech Recognition:', 'webkitSpeechRecognition' in window);
console.log('Speech Synthesis:', 'speechSynthesis' in window);
```

---

## Troubleshooting

### Voice not working
✅ Ensure HTTPS is enabled
✅ Check microphone permissions
✅ Use Chrome or Edge browser

### API errors
✅ Check API_URL in app.js
✅ Verify CORS on backend
✅ Check network tab in DevTools

### PWA not installing
✅ Verify HTTPS
✅ Check manifest.json is accessible
✅ Ensure all icons exist
✅ Run Lighthouse PWA audit

---

## Success Criteria

Your deployment is successful when:

✅ Site loads on production URL
✅ HTTPS is working
✅ Voice recognition works
✅ API calls succeed
✅ PWA can be installed
✅ Lighthouse scores > 90
✅ Works on mobile
✅ No console errors

---

**Ready to deploy! 🎉**

For detailed instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)
