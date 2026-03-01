# Key Rotation Guide – Immediate Action Required

## 🚨 What was exposed
- Supabase anon key: `sb_publishable_Idhx3ZRFfGcwK__JW7BxPw_mcHisQrA`
- Google Gemini API key in docs/scripts
- Various documentation contained real keys

## ✅ What we sanitized
- Replaced real keys in `.env.render`
- Replaced real keys in `frontend/.env.example`
- Replaced real keys in `START_HERE.md`, `startup.py`, `test_e2e.py`
- Added production-safe logger (no console logs in production)

## 🔑 Rotate these keys NOW

### 1) Supabase
1. Go to https://supabase.com/dashboard
2. Select your project
3. Settings → API
4. Click **Regenerate** next to:
   - `anon` key
   - `service_role` key
5. Copy the new keys

### 2) Google Gemini
1. Go to https://makersuite.google.com/app/apikey
2. Delete the old key
3. Create a new key
4. Copy the new key

## 🔄 Update services

### Render (backend)
- Go to your Render dashboard
- Environment variables
- Replace:
  - `GOOGLE_API_KEY`
  - `SUPABASE_ANON_KEY`
  - `SUPABASE_SERVICE_ROLE_KEY`
- Trigger redeploy

### Vercel (frontend)
- Go to your Vercel project
- Settings → Environment Variables
- Replace:
  - `REACT_APP_SUPABASE_ANON_KEY`
- Redeploy

### Local development
Update your local `.env` or `.env.local` with the new keys.

## ✅ Verify
- Backend health check passes
- Frontend can register/login
- AI chat works

## 🛡️ Future hygiene
- Never commit real keys
- Use placeholder keys in docs
- Use `.env.example` with placeholders
- Run `logger` in production (no console.log)

---
⏰ Do this now before continuing development.
