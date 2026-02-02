# Security Hardening Checklist – Affiliate AI Pro

## ✅ Applied (current)
- [x] **Helmet** security headers on backend (CSP, HSTS, X-Frame-Options, etc.)
- [x] **CORS** locked to your frontend and Supabase domains only
- [x] **CSP meta tag** in frontend HTML
- [x] **Input validation** on many API routes
- [x] **Rate limiting** (basic)
- [x] **Authentication middleware** with Supabase JWTs

## 🔐 Immediate Actions (do before production)
- [ ] **Rotate all API keys** (Google Gemini, Supabase, PayPal, etc.)
- [ ] **Never commit keys** to git (use `.env`/`.env.local` and server env vars)
- [ ] **Enable HTTPS everywhere** (Render already provides it)
- [ ] **Set up backups** (Supabase and Render have built-in backups)

## 🛡️ Recommended Hardening
- [ ] **Add audit logging** (who did what, when)
- [ ] **Add request rate limiting per user** (prevent abuse)
- [ ] **Add IP allow-listing** for admin endpoints (if any)
- [ ] **Add WAF** (Render offers basic; upgrade if needed)
- [ ] **Add license headers** to all source files
- [ ] **Obfuscate production builds** (optional)

## 📦 Deployment Security
- [ ] **Use environment-specific configs** (`.env.production`)
- [ ] **Restrict database access** (Supabase RLS policies)
- [ ] **Use VPN/private networking** for backend-to-backend calls
- [ ] **Set up monitoring/alerts** for unusual traffic

## 🔑 Key Rotation Guide
1. **Supabase**
   - Go to Supabase Dashboard → Settings → API
   - Regenerate `anon` and `service_role` keys
   - Update Render env vars and frontend `.env.local`
2. **Google Gemini**
   - Go to Google Cloud Console → APIs & Services → Credentials
   - Regenerate API key
   - Update backend env var on Render
3. **PayPal**
   - Go to PayPal Developer → My Apps & Credentials
   - Regenerate client ID/secret
   - Update backend env var on Render

## 🚨 Incident Response
- If keys are leaked: rotate immediately
- Enable logging to detect abuse
- Have a rollback plan (revert to last known good deploy)

## 📞 Contacts
- Supabase Support
- Render Support
- Google Cloud Support

---
⚠️ Treat any API keys you’ve shared in chat as **compromised** and rotate them now.
