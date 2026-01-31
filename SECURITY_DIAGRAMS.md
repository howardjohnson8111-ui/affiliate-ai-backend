# Security Protocols - Visual Architecture Diagrams

## 1. Authentication Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                      USER AUTHENTICATION FLOW                         │
└─────────────────────────────────────────────────────────────────────┘

SIGNUP FLOW:
──────────
  User Input                Backend              Supabase Auth
       │                      │                       │
       ├─ email ────────────>│                       │
       ├─ password ─────────>│                       │
       │                      ├─ signUpWithPassword ─>│
       │                      │                       ├─ Hash password
       │                      │                       ├─ Create user
       │                      │<─ JWT token ────────>│
       │                      │                       │
       │<─ 201 Created ────<─ user_id, email ────────┤
       │   (Ready to login)   │                       │


LOGIN FLOW:
──────────
  User Input                Backend              Supabase Auth
       │                      │                       │
       ├─ email ────────────>│                       │
       ├─ password ─────────>│                       │
       │                      ├─ signInWithPassword ─>│
       │                      │                       ├─ Compare passwords
       │                      │                       ├─ Generate JWT
       │                      │<─ access_token ─────>│
       │                      │<─ refresh_token ────>│
       │                      │                       │
       │<─ 200 OK ─────────<─ tokens ───────────────┤
       │   (Authenticated)    │                       │


REFRESH TOKEN FLOW:
──────────────────
  Client                    Backend              Supabase Auth
       │                      │                       │
       ├─ refresh_token ────>│                       │
       │                      ├─ refreshSession ────>│
       │                      │                       ├─ Validate refresh
       │                      │<─ new access_token ─>│
       │                      │                       │
       │<─ 200 OK ─────────<─ tokens ───────────────┤
       │  (Continue session)  │                       │
```

---

## 2. Protected Route Access Pattern

```
┌─────────────────────────────────────────────────────────────────────┐
│              ACCESSING PROTECTED RESOURCES                            │
└─────────────────────────────────────────────────────────────────────┘

REQUEST WITH VALID TOKEN:
────────────────────────
  Frontend                  Backend                Database
       │                      │                       │
       │ GET /api/campaigns   │                       │
       ├─ Headers:            │                       │
       │ Authorization:       │                       │
       │ Bearer <token>       │                       │
       │                      │                       │
       ├─────────────────────>│                       │
       │                      ├─ Middleware:          │
       │                      │ ✓ Verify JWT         │
       │                      │ ✓ Extract user_id    │
       │                      │ ✓ req.user.id = "X"  │
       │                      │                       │
       │                      ├─ Query ──────────────>│
       │                      │ SELECT * FROM         │
       │                      │ campaigns             │
       │                      │ WHERE user_id = "X"  │
       │                      │ (RLS applied)         │
       │                      │                       │
       │                      │<─ User X's data only ─┤
       │<─ 200 OK ────────────┤                       │
       │ {campaigns: [...]}   │                       │
       │                      │                       │


REQUEST WITHOUT TOKEN:
──────────────────────
  Frontend                  Backend                Database
       │                      │                       │
       │ GET /api/campaigns   │                       │
       │ (No Authorization)   │                       │
       │                      │                       │
       ├─────────────────────>│                       │
       │                      ├─ Middleware:          │
       │                      │ ✗ No token found     │
       │                      │ ✗ Return 401         │
       │                      │                       │
       │<─ 401 Unauthorized ──┤                       │
       │ {error: "..."}       │                       │
       │                      │                       │


REQUEST WITH INVALID TOKEN:
──────────────────────────
  Frontend                  Backend                Supabase
       │                      │                       │
       │ GET /api/campaigns   │                       │
       ├─ Authorization:      │                       │
       │ Bearer invalid...    │                       │
       │                      │                       │
       ├─────────────────────>│                       │
       │                      ├─ Verify token ──────>│
       │                      │                       ├─ Invalid!
       │                      │<─ ✗ Invalid token ───┤
       │                      │                       │
       │<─ 401 Unauthorized ──┤                       │
       │ {error: "..."}       │                       │
       │                      │                       │
```

---

## 3. Row Level Security (RLS) in Action

```
┌─────────────────────────────────────────────────────────────────────┐
│         ROW LEVEL SECURITY - DATA ISOLATION AT DATABASE LEVEL        │
└─────────────────────────────────────────────────────────────────────┘

DATABASE STATE (3 users, multiple campaigns):
────────────────────────────────────────────
  campaigns table:
  ┌────┬──────────────────────┬───────────────────┬──────────┐
  │ id │ name                 │ user_id          │ platform │
  ├────┼──────────────────────┼───────────────────┼──────────┤
  │ 1  │ Instagram Summer     │ user_id_AAA      │ Instagram│
  │ 2  │ TikTok Promo         │ user_id_AAA      │ TikTok   │
  │ 3  │ FB Ads Campaign      │ user_id_BBB      │ Facebook │
  │ 4  │ Twitter Thread       │ user_id_BBB      │ Twitter  │
  │ 5  │ LinkedIn Post        │ user_id_CCC      │ LinkedIn │
  └────┴──────────────────────┴───────────────────┴──────────┘


USER A (user_id = user_id_AAA) LOGS IN:
─────────────────────────────────────
  Query: SELECT * FROM campaigns
  
  ↓ RLS Policy Applied ↓
  CREATE POLICY "Users can read own campaigns"
  ON campaigns
  FOR SELECT
  USING (auth.uid() = user_id)
  
  ↓ Becomes ↓
  SELECT * FROM campaigns WHERE user_id = 'user_id_AAA'
  
  ↓ Result ↓
  ┌────┬──────────────────────┬───────────────────┐
  │ id │ name                 │ user_id           │
  ├────┼──────────────────────┼───────────────────┤
  │ 1  │ Instagram Summer     │ user_id_AAA      │
  │ 2  │ TikTok Promo         │ user_id_AAA      │
  └────┴──────────────────────┴───────────────────┘
  
  ✓ Only User A's campaigns visible
  ✓ Campaigns 3, 4, 5 never returned


USER B (user_id = user_id_BBB) LOGS IN:
─────────────────────────────────────
  Query: SELECT * FROM campaigns
  
  ↓ RLS Policy Applied ↓
  SELECT * FROM campaigns WHERE user_id = 'user_id_BBB'
  
  ↓ Result ↓
  ┌────┬──────────────────────┬───────────────────┐
  │ id │ name                 │ user_id           │
  ├────┼──────────────────────┼───────────────────┤
  │ 3  │ FB Ads Campaign      │ user_id_BBB      │
  │ 4  │ Twitter Thread       │ user_id_BBB      │
  └────┴──────────────────────┴───────────────────┘
  
  ✓ Only User B's campaigns visible
  ✓ Campaigns 1, 2, 5 never returned


USER C (user_id = user_id_CCC) LOGS IN:
─────────────────────────────────────
  Query: SELECT * FROM campaigns
  
  ↓ RLS Policy Applied ↓
  SELECT * FROM campaigns WHERE user_id = 'user_id_CCC'
  
  ↓ Result ↓
  ┌────┬──────────────────────┬───────────────────┐
  │ id │ name                 │ user_id           │
  ├────┼──────────────────────┼───────────────────┤
  │ 5  │ LinkedIn Post        │ user_id_CCC      │
  └────┴──────────────────────┴───────────────────┘
  
  ✓ Only User C's campaigns visible
  ✓ Campaigns 1, 2, 3, 4 never returned


KEY SECURITY PROPERTIES:
────────────────────────
  ✓ Enforced at database level (can't be bypassed)
  ✓ Works with hacked backend (still enforced)
  ✓ Works with manipulated JWT (still enforced)
  ✓ Zero configuration for app code
  ✓ Applied to ALL queries automatically
```

---

## 4. JWT Token Structure

```
┌─────────────────────────────────────────────────────────────────────┐
│                    JWT TOKEN ANATOMY                                 │
└─────────────────────────────────────────────────────────────────────┘

RAW JWT (what you send):
────────────────────────
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c


THREE PARTS (separated by dots):
────────────────────────────────

[HEADER].[PAYLOAD].[SIGNATURE]


DECODED - HEADER:
─────────────────
{
  "alg": "HS256",           ← Algorithm (HMAC SHA-256)
  "typ": "JWT"              ← Type (JSON Web Token)
}


DECODED - PAYLOAD (User Info):
───────────────────────────────
{
  "sub": "1234567890",      ← Subject (user_id)
  "email": "user@example.com",
  "iat": 1516239022,        ← Issued At (timestamp)
  "exp": 1516242622        ← Expires At (1 hour later)
}

⚠️ NOTE: Payload is readable (base64 encoded, not encrypted)
        Don't put sensitive data here!


SIGNATURE (Verification):
──────────────────────────
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  SECRET_KEY
)

✓ Prevents tampering (if signature doesn't match, token invalid)
✓ Can be verified without secret (using public key)
✓ Proves token wasn't modified


TOKEN FLOW:
───────────
1. Login successful → Server generates JWT
2. JWT sent to client → Client stores in localStorage/sessionStorage
3. Client makes request → Sends JWT in Authorization header
4. Backend receives → Verifies signature with secret key
5. If valid → Extract user_id from payload → Proceed
6. If invalid → Return 401 Unauthorized


TOKEN EXPIRATION:
─────────────────
Access Token:  15 minutes (iat + 900 seconds)
Refresh Token: 7 days (iat + 604800 seconds)

When access token expires:
  → Client uses refresh token to get new access token
  → No need to login again
  → Balances security (short-lived) with UX (no re-login)
```

---

## 5. Security Layers - Defense in Depth

```
┌─────────────────────────────────────────────────────────────────────┐
│          DEFENSE IN DEPTH - MULTIPLE SECURITY LAYERS                 │
└─────────────────────────────────────────────────────────────────────┘

ATTACK SCENARIO 1: User tries to access another user's campaign
─────────────────────────────────────────────────────────────

Attacker: "I want to see User B's campaigns"

LAYER 1: Frontend Validation
  ├─ Check: Is user logged in? ✓
  └─ If not: Redirect to login (UX layer)

LAYER 2: API Authentication
  ├─ Check: Authorization header present? ✓
  ├─ Check: JWT signature valid? ✓
  ├─ Check: Token not expired? ✓
  └─ Extract: user_id = "attacker_id"

LAYER 3: Backend Authorization
  ├─ Check: Ownership verified? ✓
  │ SELECT * FROM campaigns
  │ WHERE id = "campaign_id"
  │ AND user_id = "attacker_id"
  │ → Returns NULL (no match)
  └─ Return: 403 Forbidden

LAYER 4: Database (RLS)
  ├─ Query: SELECT * FROM campaigns WHERE campaign_id = "X"
  ├─ RLS Policy: WHERE auth.uid() = user_id
  ├─ Applied: WHERE user_id = "attacker_id"
  └─ Result: NULL (not attacker's campaign)

RESULT: ✓ Attack prevented by ANY layer
        (Multiple layers = robust security)


ATTACK SCENARIO 2: Hacker gets database access directly
────────────────────────────────────────────────────────

Hacker: "I'll read database directly, bypass the API"

Can they get all data?
  ├─ RLS enforced? YES ✓
  ├─ RLS prevents: SELECT * FROM campaigns (without auth.uid())
  ├─ Hacker gets: NULL (no rows returned)
  └─ Result: Even with DB access, data protected!

RESULT: ✓ RLS prevents data leak
        (Database-level protection)


ATTACK SCENARIO 3: Hacker modifies JWT token
──────────────────────────────────────────

Hacker: "I'll change user_id in JWT from B to A"

Modified JWT: {
  "sub": "user_a",         ← Changed from user_b
  "email": "user@...
  "signature": "invalid"   ← Signature doesn't match!
}

What happens?
  ├─ Check: Signature valid? NO ✗
  ├─ Action: Return 401 Unauthorized
  └─ Result: Request rejected

RESULT: ✓ Signature prevents tampering
        (Cryptographically secured)
```

---

## 6. Complete Request Lifecycle

```
┌─────────────────────────────────────────────────────────────────────┐
│         COMPLETE LIFECYCLE: USER ACTION TO DATA RESPONSE             │
└─────────────────────────────────────────────────────────────────────┘

1. USER INTERACTION (Frontend)
   User clicks: "View My Campaigns"
            │
            ▼
2. PREPARE REQUEST
   • Read access_token from localStorage
   • Create HTTP GET request
   • Add header: Authorization: Bearer <token>
            │
            ▼
3. NETWORK TRANSMISSION
   HTTP Request travels to server:
   GET /api/campaigns
   Authorization: Bearer eyJh...
            │
            ▼
4. SERVER RECEIVES REQUEST
   Request arrives at Node.js backend
            │
            ▼
5. AUTHENTICATION MIDDLEWARE (verifyToken)
   • Extract token from header
   • Call Supabase to verify JWT signature
   ├─ Signature valid? YES ✓
   ├─ Token expired? NO ✓
   ├─ User exists? YES ✓
   └─ Extract: req.user.id = "user_123"
            │
            ▼
6. ROUTE HANDLER
   app.get('/api/campaigns', verifyToken, handler)
   
   handler() executes with req.user = { id: "user_123" }
   
   Build query:
   const { data } = await supabase
     .from('campaigns')
     .select('*')
     .eq('user_id', req.user.id)
            │
            ▼
7. SUPABASE RECEIVES QUERY
   Query: SELECT * FROM campaigns WHERE user_id = 'user_123'
   
   Context: JWT token says user_id = 'user_123'
            auth.uid() = 'user_123'
            │
            ▼
8. RLS POLICY EVALUATION
   Policy: "Users can read own campaigns"
   USING (auth.uid() = user_id)
   
   Evaluate:
   auth.uid() = 'user_123'  ← From JWT
   user_id = 'user_123'     ← From table
   'user_123' = 'user_123'  ✓ TRUE
   
   Allow row to be included
            │
            ▼
9. DATABASE EXECUTION
   SELECT * FROM campaigns
   WHERE user_id = 'user_123'
   AND (auth.uid() = user_id)  ← RLS applied
   
   Result:
   [
     { id: 1, name: "Campaign 1", user_id: "user_123" },
     { id: 2, name: "Campaign 2", user_id: "user_123" }
   ]
            │
            ▼
10. RESPONSE SENT
    HTTP 200 OK
    {
      "success": true,
      "campaigns": [
        { id: 1, name: "Campaign 1", ... },
        { id: 2, name: "Campaign 2", ... }
      ],
      "count": 2
    }
            │
            ▼
11. FRONTEND RECEIVES DATA
    Parse JSON response
    Render campaigns to UI
            │
            ▼
12. USER SEES DATA
    Display: "Your Campaigns"
    1. Campaign 1
    2. Campaign 2

SECURITY CHECKPOINTS PASSED:
✓ Signature verified (step 5)
✓ User identified (step 5)
✓ RLS policy evaluated (step 8)
✓ Only own data returned (step 9)
✓ User sees only their campaigns (step 12)
```

---

## 7. Multi-User Data Isolation Example

```
┌─────────────────────────────────────────────────────────────────────┐
│         MULTI-USER SCENARIO - THREE USERS, ONE TABLE                │
└─────────────────────────────────────────────────────────────────────┘

COMPANY: Affiliate AI Pro
USERS: Demo Company (Demon), TechStart (Sarah), Shop Plus (Ahmed)


SHARED DATABASE (One campaigns table):
──────────────────────────────────────

campaigns:
┌──────┬────────────────────┬──────────────────────┬──────────────┐
│ id   │ name               │ user_id              │ platform     │
├──────┼────────────────────┼──────────────────────┼──────────────┤
│ 1    │ Summer Sale        │ user_demon_123       │ Instagram    │
│ 2    │ Black Friday       │ user_demon_123       │ Facebook     │
│ 3    │ New Product Launch │ user_sarah_456       │ TikTok       │
│ 4    │ Tech Tuesday       │ user_sarah_456       │ LinkedIn     │
│ 5    │ Holiday Deals      │ user_ahmed_789       │ Instagram    │
│ 6    │ Flash Sale         │ user_ahmed_789       │ Twitter      │
└──────┴────────────────────┴──────────────────────┴──────────────┘


SCENARIO A: Demon logs in
──────────────────────────

Login:
  ├─ Email: demon@affliate-pro.com
  └─ Password: ••••••••

Authentication:
  ├─ Credentials verified ✓
  └─ JWT created: {sub: "user_demon_123", exp: ...}

Request campaigns:
  GET /api/campaigns
  Authorization: Bearer eyJh...
       │
       ├─ Middleware verifies JWT
       │ → user_id = "user_demon_123"
       │
       ├─ Query database:
       │ SELECT * FROM campaigns
       │ WHERE user_id = auth.uid()
       │ → user_id = "user_demon_123"
       │
       └─ RLS Policy applied:
         WHERE (auth.uid() = user_id)
         WHERE "user_demon_123" = "user_demo_123" ✓

Result for Demon:
  ┌──────┬────────────────────┬──────────────────────┐
  │ id   │ name               │ platform             │
  ├──────┼────────────────────┼──────────────────────┤
  │ 1    │ Summer Sale        │ Instagram            │
  │ 2    │ Black Friday       │ Facebook             │
  └──────┴────────────────────┴──────────────────────┘


SCENARIO B: Sarah logs in (same database)
──────────────────────────────────────────

Login:
  ├─ Email: sarah@techstart.com
  └─ Password: ••••••••

Authentication:
  ├─ Credentials verified ✓
  └─ JWT created: {sub: "user_sarah_456", exp: ...}

Request campaigns:
  GET /api/campaigns
  Authorization: Bearer eyJh...
       │
       ├─ Middleware verifies JWT
       │ → user_id = "user_sarah_456"
       │
       ├─ Query database:
       │ SELECT * FROM campaigns
       │ WHERE user_id = auth.uid()
       │ → user_id = "user_sarah_456"
       │
       └─ RLS Policy applied:
         WHERE (auth.uid() = user_id)
         WHERE "user_sarah_456" = "user_sarah_456" ✓

Result for Sarah:
  ┌──────┬────────────────────┬──────────────────────┐
  │ id   │ name               │ platform             │
  ├──────┼────────────────────┼──────────────────────┤
  │ 3    │ New Product Launch │ TikTok               │
  │ 4    │ Tech Tuesday       │ LinkedIn             │
  └──────┴────────────────────┴──────────────────────┘


SCENARIO C: Ahmed logs in (same database)
──────────────────────────────────────────

Login:
  ├─ Email: ahmed@shopplus.com
  └─ Password: ••••••••

Authentication:
  ├─ Credentials verified ✓
  └─ JWT created: {sub: "user_ahmed_789", exp: ...}

Request campaigns:
  GET /api/campaigns
  Authorization: Bearer eyJh...
       │
       ├─ Middleware verifies JWT
       │ → user_id = "user_ahmed_789"
       │
       ├─ Query database:
       │ SELECT * FROM campaigns
       │ WHERE user_id = auth.uid()
       │ → user_id = "user_ahmed_789"
       │
       └─ RLS Policy applied:
         WHERE (auth.uid() = user_id)
         WHERE "user_ahmed_789" = "user_ahmed_789" ✓

Result for Ahmed:
  ┌──────┬────────────────────┬──────────────────────┐
  │ id   │ name               │ platform             │
  ├──────┼────────────────────┼──────────────────────┤
  │ 5    │ Holiday Deals      │ Instagram            │
  │ 6    │ Flash Sale         │ Twitter              │
  └──────┴────────────────────┴──────────────────────┘


KEY INSIGHT:
────────────
✓ Same database, same table
✓ Same API server serving all users
✓ Each user sees only their data
✓ Zero cross-contamination
✓ Enforced at database level (RLS)
✓ Scales to 1000s of users without code changes
```

---

## Summary

These diagrams show:

1. **Authentication Flow** - How users sign up and log in
2. **Protected Routes** - How access control works
3. **Row Level Security** - How data is isolated at database level
4. **JWT Structure** - What's in the token and how it's verified
5. **Defense in Depth** - Multiple layers of security
6. **Request Lifecycle** - Complete flow from user action to data display
7. **Multi-User Isolation** - How multiple users share infrastructure safely

**All three layers work together to create enterprise-grade security:**

```
Frontend Auth + API Verification + Database RLS = Unbreakable Security
```

---

**Your Affiliate AI Pro now has production-ready security architecture!** 🔐
