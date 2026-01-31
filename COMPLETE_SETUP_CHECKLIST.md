# Affiliate AI Pro - Complete Setup Checklist
# Follow this step-by-step to get your system fully operational

## ✅ PREREQUISITES (5 minutes)
- [ ] Have Node.js 18+ installed (`node --version`)
- [ ] Have Python 3.9+ installed (`python --version`)
- [ ] Have npm installed (`npm --version`)
- [ ] Have a GitHub account (for deployment)
- [ ] Have a Google account (for Gemini API)

## ✅ PHASE 0: API KEYS & ACCOUNTS (15 minutes)

### Google Gemini API
- [ ] Go to https://makersuite.google.com/app/apikey
- [ ] Click "Create API key"
- [ ] Copy the key
- [ ] Add to `.env`: `GOOGLE_API_KEY=AIzaSy...`

### Supabase Account
- [ ] Go to https://supabase.com
- [ ] Sign up with GitHub/email
- [ ] Create new organization
- [ ] Create new project named `affiliate-ai-pro`
- [ ] Wait for project to initialize (2-3 minutes)

## ✅ PHASE 1: DATABASE SETUP (10 minutes)

### Create Database Schema
- [ ] In Supabase, go to "SQL Editor"
- [ ] Click "New Query"
- [ ] Copy entire content from `SUPABASE_SCHEMA.sql`
- [ ] Paste into query editor
- [ ] Click "Run"
- [ ] Wait for tables to create
- [ ] Verify tables appear in "Tables" sidebar:
  - [ ] campaigns
  - [ ] transactions
  - [ ] stocks
  - [ ] learning_modules
  - [ ] user_preferences

### Get Supabase Credentials
- [ ] Go to Settings > API
- [ ] Copy `Project URL`: `https://xxxxx.supabase.co`
- [ ] Copy `anon public` key
- [ ] Copy `service_role` key (keep secret!)
- [ ] Add to `.env` file:
  ```
  SUPABASE_URL=https://xxxxx.supabase.co
  SUPABASE_ANON_KEY=eyJxxxxx
  SUPABASE_SERVICE_KEY=eyJxxxxx
  ```

## ✅ PHASE 2: ENVIRONMENT SETUP (5 minutes)

### Configure .env File
- [ ] Copy `.env.example` to `.env`
- [ ] Add all required API keys (Gemini, Supabase)
- [ ] Generate JWT_SECRET: `node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"`
- [ ] Add to `.env`: `JWT_SECRET=your_generated_secret`
- [ ] Verify file has all critical variables

### Install Dependencies
- [ ] Install Node packages: `npm install`
- [ ] Install Python packages: `pip install -r requirements.txt`
- [ ] Verify installations:
  ```bash
  npm list express cors dotenv
  pip list | grep supabase
  ```

## ✅ PHASE 3: BACKEND STARTUP (10 minutes)

### Terminal 1: Node.js Server
- [ ] Open new terminal in project root
- [ ] Run: `node server-supabase.js`
- [ ] Verify output shows:
  ```
  ✅ [Server]: Affiliate AI Backend is running
  📡 API Base URL: http://localhost:3001/api
  🔐 Authentication: Enabled (JWT)
  ```

### Terminal 2: Python AI Service
- [ ] Open new terminal in project root
- [ ] Run: `$env:GOOGLE_API_KEY='your-key'; python ai_service.py`
- [ ] Verify initialization completes

### Test Backend Health
- [ ] Run test script: `python test_api_key.py`
- [ ] All tests should pass with ✅ marks

## ✅ PHASE 4: USER AUTHENTICATION (Optional, for Multi-User)

### Enable Supabase Auth
- [ ] In Supabase, go to Authentication > Providers
- [ ] Enable "Email" provider
- [ ] Configure email settings if needed
- [ ] Go to Users tab
- [ ] Create test user:
  - [ ] Email: `test@example.com`
  - [ ] Password: `SecurePassword123!`

### Get Auth Token (for API testing)
- [ ] Use Supabase `auth.signInWithPassword()` in frontend
- [ ] Or use JWT manually for testing
- [ ] Add token to API calls in Authorization header

## ✅ PHASE 5: FRONTEND SETUP (Optional, for Web UI)

### Create React App
- [ ] Run: `npx create-react-app frontend`
- [ ] Copy `frontend-package.json` to `frontend/package.json`
- [ ] Run: `cd frontend && npm install`

### Configure Frontend
- [ ] Copy Supabase credentials to `frontend/.env`:
  ```
  REACT_APP_API_URL=http://localhost:3001/api
  REACT_APP_SUPABASE_URL=https://xxxxx.supabase.co
  REACT_APP_SUPABASE_ANON_KEY=eyJxxxxx
  ```

### Start Frontend
- [ ] In `frontend/` directory, run: `npm start`
- [ ] Browser opens to http://localhost:3000
- [ ] See React default page (you'll build UI next)

## ✅ PHASE 6: TESTING THE SYSTEM (15 minutes)

### Test API Endpoints
- [ ] Test health check: `curl http://localhost:3001/api/health`
- [ ] Create campaign (need JWT token - see below)
- [ ] Get campaigns
- [ ] Create transaction
- [ ] Get transactions

### Test AI Personas
- [ ] Start `python ai_service.py` interactive mode
- [ ] Test command: `Create Instagram campaign called Summer Promo`
- [ ] Verify campaign created in database
- [ ] Test financial assistant: `Log $500 payout via PayPal`
- [ ] Verify transaction logged

### Test User Isolation
- [ ] Create 2 test users in Supabase
- [ ] Log in as user 1, create campaign
- [ ] Verify user 2 cannot see user 1's campaigns
- [ ] Create data for user 2
- [ ] Verify each user only sees their own data

## ✅ PHASE 7: PRODUCTION DEPLOYMENT (Optional)

### Choose Hosting Platform
- [ ] Option A: Railway (easiest)
- [ ] Option B: Heroku
- [ ] Option C: AWS/GCP/Azure

### Deploy with Docker (if using Railway/AWS)
- [ ] Verify Docker installed: `docker --version`
- [ ] Build image: `docker build -t affiliate-ai .`
- [ ] Test locally: `docker run -p 3001:3001 affiliate-ai`
- [ ] Push to container registry
- [ ] Deploy via platform

### Deploy with Git (if using Railway)
- [ ] Push repo to GitHub
- [ ] Connect GitHub to Railway
- [ ] Set environment variables in Railway dashboard
- [ ] Deploy with one click

## ✅ MONITORING & MAINTENANCE

### Set Up Logs
- [ ] Check Node.js logs: `tail -f logs/server.log`
- [ ] Check Python logs: `tail -f logs/ai_service.log`
- [ ] Set up error tracking (Sentry, DataDog)

### Regular Tasks
- [ ] Weekly: Review transaction logs
- [ ] Monthly: Check database backups
- [ ] Quarterly: Update dependencies: `npm update`, `pip install --upgrade`

### Troubleshooting
- [ ] If auth fails: check JWT_SECRET in .env
- [ ] If Supabase connection fails: verify URL and keys
- [ ] If AI service fails: check GOOGLE_API_KEY
- [ ] See `COMPLETE_IMPLEMENTATION_GUIDE.md` for detailed help

## ✅ NEXT FEATURES TO BUILD

- [ ] Real stock price integration (Alpha Vantage API)
- [ ] Email notifications (SendGrid)
- [ ] Analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Advanced reporting (PDF export)
- [ ] Team collaboration
- [ ] WebSocket for real-time updates

## 🎉 COMPLETION CHECKLIST

When you can do ALL of these, you're done:

- [ ] Backend running on http://localhost:3001
- [ ] Python AI service running
- [ ] Create campaign via API
- [ ] Campaign appears in Supabase
- [ ] Transaction logging works
- [ ] User data is isolated
- [ ] Frontend displays dashboard (optional)
- [ ] All tests pass
- [ ] Documentation is complete

---

**Estimated Total Time: 1-2 hours**

**Start with Phase 0 and work your way down. Don't skip steps!**

**Questions? See `COMPLETE_IMPLEMENTATION_GUIDE.md`**

**Let's go! 🚀**
