# 🔐 JWT Authentication - Quick Reference Card

## Installation & Setup

```bash
# 1. Install dependencies
npm install

# 2. Create .env file
echo 'SUPABASE_URL=your-url' > .env
echo 'SUPABASE_ANON_KEY=your-key' >> .env

# 3. Start server
npm start
```

---

## API Endpoints Cheat Sheet

### 🔓 Public - Authentication

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /api/auth/signup | Create account |
| POST | /api/auth/login | Get JWT token |
| POST | /api/auth/logout | Sign out |

### 🔐 Protected - Campaigns

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | /api/campaigns | ✅ Bearer | Create campaign |
| GET | /api/campaigns | ✅ Bearer | List campaigns |
| GET | /api/campaigns/:id | ✅ Bearer | Get campaign |
| PUT | /api/campaigns/:id | ✅ Bearer | Update campaign |
| DELETE | /api/campaigns/:id | ✅ Bearer | Delete campaign |

### 🔐 Protected - Transactions

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | /api/transactions | ✅ Bearer | Create transaction |
| GET | /api/transactions | ✅ Bearer | List transactions |

### ⚪ Public - Health Check

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /api/health | Server status |

---

## Common cURL Commands

### Signup
```bash
curl -X POST http://localhost:3001/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

### Login
```bash
curl -X POST http://localhost:3001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

**Copy the `token` from response**

### Create Campaign (Protected)
```bash
curl -X POST http://localhost:3001/api/campaigns \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "name": "Summer Sale",
    "platform": "Instagram",
    "status": "active"
  }'
```

### Get All Campaigns (Protected)
```bash
curl -X GET http://localhost:3001/api/campaigns \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Update Campaign (Protected)
```bash
curl -X PUT http://localhost:3001/api/campaigns/CAMPAIGN_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "status": "completed",
    "conversions": 25
  }'
```

### Delete Campaign (Protected)
```bash
curl -X DELETE http://localhost:3001/api/campaigns/CAMPAIGN_ID \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Logout (Protected)
```bash
curl -X POST http://localhost:3001/api/auth/logout \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## Error Codes & Solutions

| Status | Error | Cause | Solution |
|--------|-------|-------|----------|
| 201 | User registered | Success | N/A |
| 200 | Login successful | Success | Copy token |
| 400 | Email and password required | Missing fields | Add email + password |
| 400 | Email already exists | User exists | Use different email |
| 401 | Not authorized - no token | Missing header | Add: `Authorization: Bearer TOKEN` |
| 401 | Not authorized - invalid token | Bad token | Login again for new token |
| 401 | Token verification failed | Expired token | Refresh token via login |
| 401 | User not found with token | Token invalid | Create new account |
| 500 | Internal server error | Server error | Check server logs |
| 503 | Supabase not configured | Missing env vars | Add SUPABASE_URL and KEY |

---

## Bearer Token Format

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U
                ^^^^^^                                                                                             
              Bearer + space + actual JWT token
```

Parts:
- **Bearer** - Token type (always "Bearer" for JWT)
- **Space** - Required separator
- **Token** - JWT from login response

---

## Request/Response Examples

### Signup Request
```json
POST /api/auth/signup
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

### Signup Response (201)
```json
{
  "message": "User registered successfully",
  "user": {
    "id": "user-uuid-here",
    "email": "user@example.com"
  }
}
```

### Login Request
```json
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

### Login Response (200)
```json
{
  "message": "Login successful",
  "user": {
    "id": "user-uuid-here",
    "email": "user@example.com"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Campaign Create Request
```json
POST /api/campaigns
Header: Authorization: Bearer {token}
{
  "name": "Summer Sale Campaign",
  "platform": "Instagram",
  "affiliate_link": "https://example.com/ref/123",
  "status": "active",
  "tags": ["seasonal", "high-roi"]
}
```

### Campaign Create Response (201)
```json
{
  "id": "1234567890",
  "name": "Summer Sale Campaign",
  "platform": "Instagram",
  "affiliate_link": "https://example.com/ref/123",
  "clicks": 0,
  "conversions": 0,
  "earnings": 0,
  "status": "active",
  "tags": ["seasonal", "high-roi"],
  "created_at": "2026-01-27T12:00:00.000Z"
}
```

### Error Response (401)
```json
{
  "error": "❌ Not authorized - no token provided"
}
```

---

## JavaScript/Fetch Examples

### Signup with Fetch
```javascript
async function signup(email, password) {
  const response = await fetch('http://localhost:3001/api/auth/signup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  
  if (response.ok) {
    const data = await response.json();
    console.log('User created:', data.user);
    return data;
  } else {
    const error = await response.json();
    console.error('Signup failed:', error.message);
  }
}
```

### Login with Fetch
```javascript
async function login(email, password) {
  const response = await fetch('http://localhost:3001/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  
  const data = await response.json();
  if (response.ok) {
    // Save token
    localStorage.setItem('authToken', data.token);
    console.log('Login successful');
    return data.token;
  } else {
    console.error('Login failed:', data.error);
  }
}
```

### Get Campaigns with Auth
```javascript
async function getCampaigns(token) {
  const response = await fetch('http://localhost:3001/api/campaigns', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  if (response.ok) {
    const campaigns = await response.json();
    console.log('Campaigns:', campaigns);
    return campaigns;
  } else if (response.status === 401) {
    console.error('Token invalid, please login again');
    localStorage.removeItem('authToken');
  }
}
```

### Logout
```javascript
async function logout(token) {
  const response = await fetch('http://localhost:3001/api/auth/logout', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  if (response.ok) {
    localStorage.removeItem('authToken');
    console.log('Logged out');
  }
}
```

---

## Environment Variables

```bash
# Required for authentication
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-public-api-key-here

# Optional
PORT=3001
NODE_ENV=development
```

Get from: [Supabase Dashboard](https://app.supabase.com) → Settings → API

---

## Middleware in Code

```javascript
// This is what protect() middleware does:
async function protect(req, res, next) {
  // 1. Extract token from header
  let token = req.headers.authorization?.split(' ')[1];
  
  // 2. Check if token exists
  if (!token) return res.status(401).json({ error: 'No token' });
  
  // 3. Verify with Supabase
  const { data: { user } } = await supabase.auth.getUser(token);
  
  // 4. Attach user to request
  req.user = user;
  
  // 5. Continue to route handler
  next();
}

// Usage on routes:
app.get('/api/campaigns', protect, (req, res) => {
  // req.user is now available!
  console.log('User:', req.user.id);
  // ... handle request
});
```

---

## Testing Workflow

```bash
# 1. Start server
npm start

# 2. Signup
curl -X POST http://localhost:3001/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'

# 3. Login (copy token)
curl -X POST http://localhost:3001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'

# 4. Use token
TOKEN="paste-token-from-step-3-here"
curl -X GET http://localhost:3001/api/campaigns \
  -H "Authorization: Bearer $TOKEN"

# 5. Run full test suite
python test_auth.py
```

---

## Quick Debugging

### Check if server is running
```bash
curl http://localhost:3001/api/health
# Should return: {"message":"Backend is running!"}
```

### Check if Supabase is configured
```bash
npm start
# Look for: ✅ [Supabase]: Initialized
```

### Verify token format
```bash
# Token should start with "eyJ" and have 3 parts separated by dots:
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
# .
# eyJzdWIiOiIxMjM0NTY3ODkwIn0
# .
# dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U
```

### View server logs for errors
```bash
# Logs show with emoji prefixes:
# 🚪 [Auth]: User logged in - email@example.com
# ❌ [Auth Error]: Error message
# ✅ [Supabase]: Initialized
```

---

## Security Checklist

- [ ] .env file created with Supabase credentials
- [ ] SUPABASE_URL and SUPABASE_ANON_KEY filled in
- [ ] .env file in .gitignore (don't commit)
- [ ] npm install completed
- [ ] server.js syntax valid (no errors on npm start)
- [ ] Can signup user
- [ ] Can login and receive token
- [ ] Can access protected routes with token
- [ ] Rejected without token (401 error)
- [ ] Rejected with invalid token (401 error)

---

**Print this card and keep it handy for reference!** 📋

Last Updated: January 27, 2026  
Status: ✅ Ready for Production
