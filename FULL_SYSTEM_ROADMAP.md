# Affiliate AI Pro - Complete System Implementation Roadmap

## Overview
Building a **production-ready, multi-user, secure AI executive assistant system** with full authentication, persistent database, and modern web UI.

---

## Phase 1: Supabase Setup & Database Schema

### 1.1 Create Supabase Project
1. Go to https://supabase.com
2. Sign up/login and create new project
3. Get your **Project URL** and **API Key** (anon key)
4. Save these in `.env` file

### 1.2 Database Schema

#### Users Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  username TEXT UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Campaigns Table
```sql
CREATE TABLE campaigns (
  id TEXT PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  platform TEXT NOT NULL,
  affiliate_link TEXT,
  clicks INTEGER DEFAULT 0,
  content TEXT,
  conversions INTEGER DEFAULT 0,
  earnings DECIMAL(10, 2) DEFAULT 0,
  image_url TEXT,
  scheduled_date TEXT,
  status TEXT DEFAULT 'draft',
  tags TEXT[],
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Transactions Table
```sql
CREATE TABLE transactions (
  id TEXT PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  amount DECIMAL(10, 2) NOT NULL,
  type TEXT NOT NULL,
  description TEXT,
  payment_method TEXT,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Stocks Table
```sql
CREATE TABLE stocks (
  id TEXT PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  ticker TEXT NOT NULL,
  shares DECIMAL(10, 4) NOT NULL,
  purchase_price DECIMAL(10, 2) NOT NULL,
  purchase_date TEXT,
  broker TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Learning Modules Table
```sql
CREATE TABLE learning_modules (
  id TEXT PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  platform TEXT,
  description TEXT,
  progress INTEGER DEFAULT 0,
  target_completion TEXT,
  status TEXT DEFAULT 'in_progress',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

#### User Preferences Table
```sql
CREATE TABLE user_preferences (
  id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::TEXT,
  user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
  theme TEXT DEFAULT 'dark',
  default_view TEXT DEFAULT 'dashboard',
  notifications_enabled BOOLEAN DEFAULT true,
  currency TEXT DEFAULT 'USD',
  language TEXT DEFAULT 'en',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## Phase 2: Backend Updates (Node.js + Supabase Integration)

### 2.1 Update server.js
- Remove in-memory storage
- Connect to Supabase
- Add Supabase auth middleware
- Add user_id to all endpoints
- Implement RLS (Row Level Security) policies

### 2.2 Update ai_service.py
- Connect to Supabase for data persistence
- Add user_id context to all function calls
- Update tools to work with user-specific data

---

## Phase 3: Frontend PWA (React)

### 3.1 Project Structure
```
affiliate-ai-pwa/
├── src/
│   ├── components/
│   │   ├── Auth/
│   │   │   ├── LoginPage.jsx
│   │   │   ├── SignupPage.jsx
│   │   │   └── AuthContext.jsx
│   │   ├── Dashboard/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── PersonaCard.jsx
│   │   │   └── StatsPanel.jsx
│   │   ├── Chat/
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── ChatMessage.jsx
│   │   │   └── InputBox.jsx
│   │   ├── Campaigns/
│   │   │   ├── CampaignList.jsx
│   │   │   ├── CampaignForm.jsx
│   │   │   └── CampaignDetail.jsx
│   │   ├── Transactions/
│   │   │   ├── TransactionList.jsx
│   │   │   ├── TransactionForm.jsx
│   │   │   └── TransactionChart.jsx
│   │   ├── Settings/
│   │   │   ├── SettingsPage.jsx
│   │   │   └── PreferencesPanel.jsx
│   │   └── Common/
│   │       ├── Header.jsx
│   │       ├── Sidebar.jsx
│   │       └── Navbar.jsx
│   ├── services/
│   │   ├── api.js
│   │   ├── auth.js
│   │   └── supabase.js
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── useCampaigns.js
│   │   └── useTransactions.js
│   ├── pages/
│   │   ├── HomePage.jsx
│   │   ├── LoginPage.jsx
│   │   ├── DashboardPage.jsx
│   │   └── SettingsPage.jsx
│   ├── App.jsx
│   ├── index.jsx
│   └── App.css
├── public/
│   ├── index.html
│   ├── manifest.json
│   └── favicon.ico
├── package.json
├── vite.config.js
└── README.md
```

### 3.2 Key Components to Build

**Auth System:**
- Login page (email + password)
- Signup page with validation
- Session persistence
- Protected routes

**Dashboard:**
- Welcome section
- 6 persona cards (clickable)
- Quick stats (campaigns, transactions, etc.)
- Recent activity feed

**Chat Interface:**
- Message display
- Input box with persona selector
- Real-time responses
- History management

**CRUD Interfaces:**
- Campaign manager with forms/lists
- Transaction tracker with charts
- Stock portfolio view
- Learning progress tracker

**Settings:**
- Theme toggle (light/dark/auto)
- Language selection
- Default view
- Account management

---

## Phase 4: Integration & Deployment

### 4.1 Environment Variables
```
# .env file setup for all services
GOOGLE_API_KEY=<your-key>
SUPABASE_URL=<your-supabase-url>
SUPABASE_ANON_KEY=<your-anon-key>
SUPABASE_SERVICE_ROLE_KEY=<your-service-role-key>
NODE_ENV=production
REACT_APP_API_URL=http://localhost:3001
```

### 4.2 Deployment Options
1. **Frontend:** Vercel, Netlify, or GitHub Pages
2. **Backend:** AWS EC2, Heroku, or Railway
3. **Database:** Supabase (cloud-hosted)
4. **Python Service:** Separate server or AWS Lambda

### 4.3 Testing Strategy
- Unit tests for API endpoints
- Integration tests for auth flow
- E2E tests for user workflows
- Load testing for scalability

---

## Technical Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React + Vite | Modern, fast PWA |
| **Backend** | Node.js + Express | REST API |
| **AI** | Python + Gemini | Multi-persona assistant |
| **Database** | Supabase + PostgreSQL | Persistent storage |
| **Auth** | Supabase Auth | User authentication |
| **Hosting** | Vercel/Netlify + AWS/Heroku | Cloud deployment |
| **Real-time** | Socket.io (optional) | Live chat updates |

---

## Timeline Estimate

- **Phase 1 (Supabase):** 1-2 hours
- **Phase 2 (Backend Updates):** 3-4 hours
- **Phase 3 (Frontend PWA):** 8-12 hours
- **Phase 4 (Integration):** 4-6 hours
- **Total:** ~20-25 hours of development

---

## Success Metrics

✅ Users can sign up and login  
✅ Each user sees only their own data  
✅ All 6 personas work via web interface  
✅ Campaigns can be created/updated/deleted  
✅ Transactions are logged and persisted  
✅ App works offline (PWA) and online  
✅ Responsive design (mobile/tablet/desktop)  
✅ No hardcoded secrets in code  

---

## Next Step

Start with **Phase 1: Supabase Setup** - Let me know once you're ready and I'll guide you through creating the project and schema!
