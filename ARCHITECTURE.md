# Affiliate AI Pro - Complete System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AFFILIATE AI PRO - COMPLETE STACK                │
└─────────────────────────────────────────────────────────────────────┘

                         PHASE 1-4 ARCHITECTURE

┌──────────────────────────────────────────────────────────────────────┐
│                           USER DEVICES                               │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Desktop / Laptop          Tablet              Mobile Phone          │
│  ┌──────────────┐      ┌──────────────┐    ┌──────────────┐         │
│  │   Browser    │      │   Browser    │    │   PWA App    │         │
│  │   (React)    │      │   (React)    │    │   (React)    │         │
│  └──────────────┘      └──────────────┘    └──────────────┘         │
│         │                     │                     │                │
└─────────┼─────────────────────┼─────────────────────┼────────────────┘
          │                     │                     │
          └─────────────────────┼─────────────────────┘
                                │
                                ▼
        ┌──────────────────────────────────────────────┐
        │    FRONTEND (Phase 3 - React PWA)            │
        ├──────────────────────────────────────────────┤
        │                                               │
        │  Components:                                  │
        │  ├─ Login & Auth Pages                       │
        │  ├─ Dashboard with Stats                     │
        │  ├─ AI Chat Interface                        │
        │  ├─ Campaign Manager                         │
        │  ├─ Transaction Tracker                      │
        │  ├─ Stock Portfolio                          │
        │  ├─ Learning Manager                         │
        │  └─ Settings Panel                           │
        │                                               │
        │  Features:                                    │
        │  ├─ PWA (works offline)                      │
        │  ├─ Responsive Design                        │
        │  ├─ Dark/Light Theme                         │
        │  └─ Multi-language Support                   │
        │                                               │
        └──────────────────────────────────────────────┘
                          │
                          │ HTTPS/WebSocket
                          │ REST API Calls
                          │
                          ▼
        ┌──────────────────────────────────────────────┐
        │     BACKEND API (Phase 2 - Node.js)          │
        ├──────────────────────────────────────────────┤
        │                                               │
        │  Express.js Server (Port 3001)               │
        │                                               │
        │  Routes:                                      │
        │  ├─ POST   /auth/signup                      │
        │  ├─ POST   /auth/login                       │
        │  ├─ POST   /auth/logout                      │
        │  ├─ GET    /auth/verify                      │
        │  ├─ GET    /api/campaigns                    │
        │  ├─ POST   /api/campaigns                    │
        │  ├─ PUT    /api/campaigns/:id                │
        │  ├─ DELETE /api/campaigns/:id                │
        │  ├─ GET    /api/transactions                 │
        │  ├─ POST   /api/transactions                 │
        │  ├─ GET    /api/stocks                       │
        │  ├─ POST   /api/stocks                       │
        │  ├─ GET    /api/learning                     │
        │  ├─ POST   /api/learning                     │
        │  ├─ GET    /api/preferences                  │
        │  └─ PUT    /api/preferences                  │
        │                                               │
        │  Middleware:                                  │
        │  ├─ Authentication (Supabase)                │
        │  ├─ User Isolation (RLS)                     │
        │  ├─ CORS Handling                            │
        │  └─ Error Handling                           │
        │                                               │
        └──────────────────────────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
    ┌────────────┐  ┌────────────┐  ┌────────────┐
    │ Supabase   │  │   Python   │  │ (Future)   │
    │ Auth       │  │ AI Service │  │ Extensions │
    └────────────┘  └────────────┘  └────────────┘
         │                │
         │                │ gRPC/HTTP
         │                │
         └────────┬───────┘
                  │
                  ▼
    ┌──────────────────────────────────────────────┐
    │      CORE SERVICES & DATA LAYER             │
    ├──────────────────────────────────────────────┤
    │                                               │
    │  ┌─────────────────────────────────────┐    │
    │  │     Python AI Service               │    │
    │  │     (Multi-Persona Assistant)       │    │
    │  ├─────────────────────────────────────┤    │
    │  │                                     │    │
    │  │  6 Specialized Personas:            │    │
    │  │  ├─ Campaign Manager 🎯             │    │
    │  │  ├─ Stock Analyst 📈                │    │
    │  │  ├─ Learning Manager 🎓             │    │
    │  │  ├─ Financial Assistant 💰          │    │
    │  │  ├─ App Customizer ⚙️               │    │
    │  │  └─ Language Assistant 🌍           │    │
    │  │                                     │    │
    │  │  AI Engine:                         │    │
    │  │  ├─ Google Gemini 2.5 Flash        │    │
    │  │  ├─ Function Calling                │    │
    │  │  ├─ Tool Routing                    │    │
    │  │  └─ Conversation History            │    │
    │  │                                     │    │
    │  └─────────────────────────────────────┘    │
    │                                               │
    │  ┌─────────────────────────────────────┐    │
    │  │    Supabase (Cloud Database)        │    │
    │  │    PostgreSQL + Auth + Hosting      │    │
    │  ├─────────────────────────────────────┤    │
    │  │                                     │    │
    │  │  Tables:                            │    │
    │  │  ├─ user_profiles                   │    │
    │  │  ├─ campaigns                       │    │
    │  │  ├─ transactions                    │    │
    │  │  ├─ stocks                          │    │
    │  │  ├─ learning_modules                │    │
    │  │  ├─ user_preferences                │    │
    │  │  └─ conversation_history            │    │
    │  │                                     │    │
    │  │  Security:                          │    │
    │  │  ├─ Row Level Security (RLS)        │    │
    │  │  ├─ Authentication (OAuth/Email)    │    │
    │  │  └─ User Data Isolation             │    │
    │  │                                     │    │
    │  └─────────────────────────────────────┘    │
    │                                               │
    └──────────────────────────────────────────────┘
```

---

## Data Flow Example: User Creates a Campaign

```
1. USER ACTION
   ┌─────────────────────────┐
   │ User: "Create Instagram │
   │ campaign: Summer Sale"  │
   └──────────┬──────────────┘
              │
              ▼
2. FRONTEND (React PWA)
   ┌─────────────────────────┐
   │ Parse input             │
   │ Format campaign data    │
   │ Send POST request       │
   └──────────┬──────────────┘
              │ POST /api/campaigns
              │ {user_id, name, platform, ...}
              │
              ▼
3. BACKEND (Node.js)
   ┌─────────────────────────────────┐
   │ Verify auth token               │
   │ Extract user_id from token      │
   │ Validate input                  │
   │ Call Supabase                   │
   └──────────┬──────────────────────┘
              │ INSERT campaigns table
              │ WHERE user_id = logged_in_user
              │
              ▼
4. DATABASE (Supabase)
   ┌──────────────────────────────────────┐
   │ RLS Policy Check:                    │
   │ "Can this user_id write to table?"   │
   │ ✅ YES - Insert allowed              │
   └──────────┬───────────────────────────┘
              │
              ▼
5. STORAGE
   ┌──────────────────────────────────────┐
   │ PostgreSQL:                          │
   │ ┌────────────────────────────────┐   │
   │ │ campaigns table               │   │
   │ ├────────────────────────────────┤   │
   │ │ id: abc123                    │   │
   │ │ user_id: user@example.com     │   │
   │ │ name: Summer Sale             │   │
   │ │ platform: Instagram           │   │
   │ │ created_at: 2026-01-27        │   │
   │ └────────────────────────────────┘   │
   └──────────┬───────────────────────────┘
              │
              ▼
6. RESPONSE
   ┌──────────────────────────────────────┐
   │ Backend returns:                     │
   │ {                                    │
   │   id: "abc123",                      │
   │   name: "Summer Sale",               │
   │   platform: "Instagram",             │
   │   status: "draft",                   │
   │   created_at: "2026-01-27T..."       │
   │ }                                    │
   └──────────┬───────────────────────────┘
              │
              ▼
7. FRONTEND UPDATE
   ┌──────────────────────────────────────┐
   │ Display success message              │
   │ Add campaign to list                 │
   │ Show new campaign card               │
   │ User sees "Campaign created! ✅"     │
   └──────────────────────────────────────┘
```

---

## AI Chat Flow with Persona Detection

```
USER INPUT
    │
    ├─ "Create an Instagram campaign"
    │
    ▼
FRONTEND: Send to Python AI Service
    │
    │ POST /chat
    │ {
    │   user_message: "Create an Instagram campaign",
    │   user_id: "current_user_id"
    │ }
    │
    ▼
PYTHON AI SERVICE (ai_service.py)
    │
    ├─ Step 1: DETECT PERSONA
    │   ├─ Check for explicit mention: "Campaign Manager" → Not found
    │   ├─ Check keywords: "instagram", "campaign" → Found!
    │   └─ Detected Persona: Campaign Manager 🎯
    │
    ├─ Step 2: GET PERSONA TOOLS
    │   ├─ Load tools for Campaign Manager:
    │   │   ├─ create_campaign
    │   │   ├─ read_campaign
    │   │   ├─ update_campaign
    │   │   └─ delete_campaign
    │   └─ Other personas' tools NOT included (prevents confusion)
    │
    ├─ Step 3: SEND TO GEMINI
    │   ├─ Contents: conversation history + new message
    │   ├─ Tools: campaign tools only
    │   ├─ System Instruction: Campaign Manager role definition
    │   └─ Model: gemini-2.5-flash
    │
    ├─ Step 4: GEMINI RESPONSE
    │   └─ "I'll help create that Instagram campaign. Let me use the tool..."
    │       ├─ Function Call: create_campaign({
    │       │   name: "Instagram Campaign",
    │       │   platform: "Instagram",
    │       │   status: "draft"
    │       │ })
    │
    ├─ Step 5: EXECUTE TOOL
    │   │
    │   ├─ Tool: create_campaign
    │   │   ├─ Add user_id to request
    │   │   ├─ Call backend: POST /api/campaigns
    │   │   ├─ Backend validates user_id
    │   │   ├─ Backend saves to Supabase
    │   │   └─ Return: {id: "abc123", name: "...", ...}
    │   │
    │   └─ Response to Gemini with tool output
    │
    ├─ Step 6: GEMINI SUMMARY
    │   └─ "Campaign created successfully! ✅
    │       ID: abc123
    │       Name: Instagram Campaign
    │       Platform: Instagram
    │       Status: Draft
    │       Ready to publish when you are!"
    │
    └─ Step 7: STORE CONVERSATION
        ├─ Save to Supabase conversation_history table
        ├─ user_id, persona, message, response, timestamp
        └─ Can retrieve chat history later
    
    ▼
RESPONSE TO USER
    │
    └─ Display: "Campaign created successfully! ✅"
       Plus campaign details
```

---

## Technology Stack

| Layer | Technology | Purpose | Status |
|-------|-----------|---------|--------|
| **Frontend** | React + Vite | User interface | Phase 3 |
| **Frontend Storage** | PWA (LocalStorage) | Offline access | Phase 3 |
| **Backend** | Node.js + Express | REST API | Phase 2 |
| **Backend Auth** | Supabase Auth | User authentication | Phase 2 |
| **AI Engine** | Python + Gemini 2.5 Flash | Persona routing & tool calling | ✅ Complete |
| **Database** | Supabase (PostgreSQL) | Persistent data storage | Phase 1 |
| **Hosting** | TBD (Vercel/AWS/Heroku) | Cloud deployment | Phase 4 |

---

## Security Architecture

```
┌─────────────────────────────────────────────┐
│           SECURITY LAYERS                   │
├─────────────────────────────────────────────┤
│                                             │
│ Layer 1: HTTPS/TLS                          │
│ └─ All traffic encrypted in transit         │
│                                             │
│ Layer 2: Authentication                     │
│ ├─ Supabase Auth (Email/OAuth)              │
│ ├─ JWT tokens                               │
│ └─ Session validation                       │
│                                             │
│ Layer 3: Authorization                      │
│ ├─ Backend middleware validates user        │
│ ├─ Check user_id matches token              │
│ └─ Reject if mismatch                       │
│                                             │
│ Layer 4: Database-Level (RLS)               │
│ ├─ PostgreSQL Row Level Security            │
│ ├─ Users can only SELECT own rows            │
│ ├─ Users can only INSERT with own user_id   │
│ ├─ Users can only UPDATE own rows            │
│ └─ Users can only DELETE own rows            │
│                                             │
│ Layer 5: Secrets Management                 │
│ ├─ Environment variables (never in code)    │
│ ├─ Service role key only in backend         │
│ ├─ API key in backend only                  │
│ └─ Anon key only in frontend (limited)      │
│                                             │
└─────────────────────────────────────────────┘

Example: User2 tries to access User1's campaign

    User2 Request
         │
         ▼
    Backend Middleware
    "Is user_id == token user?" 
         │
         ├─ YES ─→ Process request
         │
         └─ NO ──→ Reject (401 Unauthorized)
         
    Even if they bypass → Supabase RLS
    "Can user2_id SELECT from campaigns 
     WHERE user_id = user1_id?"
         │
         └─ NO ──→ Database level rejection
         
Result: DOUBLE PROTECTED ✅
```

---

## Deployment Architecture (Phase 4)

```
┌──────────────────────────────────────────────┐
│           PRODUCTION DEPLOYMENT              │
├──────────────────────────────────────────────┤
│                                              │
│  ┌─────────────────────────────────────┐    │
│  │      CDN + Frontend Hosting         │    │
│  │      (Vercel / Netlify)             │    │
│  │      affiliate-ai-pro.vercel.app    │    │
│  │      ✓ React PWA                    │    │
│  │      ✓ Auto-deploy on git push      │    │
│  │      ✓ Global edge locations        │    │
│  └─────────────────────────────────────┘    │
│              │                               │
│              │ HTTPS                        │
│              ▼                               │
│  ┌─────────────────────────────────────┐    │
│  │      Backend API Server             │    │
│  │      (AWS EC2 / Heroku / Railway)   │    │
│  │      api.affiliate-ai-pro.com       │    │
│  │      ✓ Express.js + Node.js         │    │
│  │      ✓ Auto-scaling on demand       │    │
│  │      ✓ Health checks & monitoring   │    │
│  └─────────────────────────────────────┘    │
│              │                               │
│              │ HTTPS                        │
│              ▼                               │
│  ┌─────────────────────────────────────┐    │
│  │      AI Service Server              │    │
│  │      (AWS Lambda / EC2)             │    │
│  │      ai.affiliate-ai-pro.com        │    │
│  │      ✓ Python + Gemini              │    │
│  │      ✓ Async job queue              │    │
│  │      ✓ Conversation logging         │    │
│  └─────────────────────────────────────┘    │
│              │                               │
│              │ HTTPS + Auth                 │
│              ▼                               │
│  ┌─────────────────────────────────────┐    │
│  │      Supabase Cloud                 │    │
│  │      PostgreSQL + Auth              │    │
│  │      db.affiliate-ai-pro.supabase   │    │
│  │      ✓ Automatic backups            │    │
│  │      ✓ Multi-region replication     │    │
│  │      ✓ 99.99% uptime SLA           │    │
│  └─────────────────────────────────────┘    │
│              │                               │
└──────────────┼───────────────────────────────┘
               │
        Monitor & Logs
        (DataDog / New Relic)
```

---

## Performance & Scalability

```
Current (MVP):
├─ Single backend instance
├─ In-memory data (ready for persistence)
└─ Direct API calls
Handles: ~100 concurrent users

Phase 2+ (With Supabase):
├─ Persistent database
├─ JWT-based auth
├─ RLS for data isolation
└─ Direct API calls
Handles: ~1,000 concurrent users

Phase 4 (Production Ready):
├─ Load balancer (distribute traffic)
├─ Auto-scaling backend instances
├─ Supabase managed database
├─ CDN for static assets
├─ Background job queue
├─ Caching layer (Redis)
└─ Real-time updates (WebSocket)
Handles: ~10,000+ concurrent users

Bottleneck Relief Strategies:
├─ Database connection pooling
├─ Query optimization & indexing
├─ API rate limiting
├─ Caching frequently accessed data
├─ Async processing for heavy tasks
└─ Monitoring & auto-scaling
```

---

## Development Timeline

```
Timeline:
├─ Phase 1: Supabase Setup          (25 min)  ← YOU ARE HERE
├─ Phase 2: Backend Auth & Supabase  (3-4 hrs)
├─ Phase 3: React PWA Frontend       (8-12 hrs)
├─ Phase 4: Deployment & Scaling     (4-6 hrs)
└─ Total Development Time:           ~20-25 hours

Maintenance:
├─ Monitoring & alerts              (ongoing)
├─ Security patches                 (monthly)
├─ Performance optimization         (quarterly)
└─ Feature additions                (as needed)
```

---

## Success Metrics

After all phases complete:

```
✅ Multi-User System
   ├─ Each user has unique account
   ├─ User data is isolated
   └─ Users can't see others' data

✅ Full AI Integration
   ├─ 6 personas working via web
   ├─ Conversation history saved
   └─ Tools execute correctly

✅ Production Ready
   ├─ 99.99% uptime
   ├─ < 200ms response time
   ├─ Zero data breaches
   └─ Automatic backups

✅ User Experience
   ├─ Works on all devices
   ├─ Responsive design
   ├─ Offline capability (PWA)
   └─ Dark/light theme support

✅ Maintainability
   ├─ Clean code structure
   ├─ Full documentation
   ├─ Automated tests
   └─ CI/CD pipeline
```

---

**Status:** ⏳ Waiting for Phase 1 completion!

Once you complete the Supabase setup, the entire system will come together. All the pieces are already built - we're just connecting them! 🚀
