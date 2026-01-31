# Authentication Setup Guide

## Overview

The Affiliate AI Pro backend now includes **JWT-based authentication** with Supabase. All campaign and transaction endpoints are protected and require valid authentication tokens.

## Features

✅ **User Registration (Signup)** - Create new user accounts  
✅ **User Login** - Authenticate with email and password  
✅ **User Logout** - Sign out and invalidate session  
✅ **Route Protection** - All CRUD endpoints require authentication  
✅ **JWT Verification** - Secure token validation with Supabase  
✅ **User Context** - Authenticated user info available in all routes via `req.user`

## Installation

### 1. Install Dependencies

```bash
npm install
```

This installs:
- `express` - Web framework
- `cors` - Cross-origin requests
- `@supabase/supabase-js` - Supabase SDK for authentication

### 2. Configure Environment Variables

Copy the `.env.example` file to `.env` and add your Supabase credentials:

```bash
cp .env.example .env
```

Edit `.env` with:

```dotenv
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
PORT=3001
NODE_ENV=development
```

**Where to find these values:**
1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Select your project
3. Click **Settings** → **API**
4. Copy `Project URL` and `anon` public API key

### 3. Start the Server

```bash
npm start
```

Expected output:
```
✅ [Supabase]: Initialized
✅ [Server]: Affiliate AI Backend is running on http://localhost:3001
```

## API Endpoints

### Authentication Endpoints

#### 1. **POST /api/auth/signup** - Register a new user

```bash
curl -X POST http://localhost:3001/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securePassword123"
  }'
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com"
  }
}
```

#### 2. **POST /api/auth/login** - Authenticate and get JWT token

```bash
curl -X POST http://localhost:3001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securePassword123"
  }'
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com"
  },
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

#### 3. **POST /api/auth/logout** - Sign out (Protected)

```bash
curl -X POST http://localhost:3001/api/auth/logout \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

**Response (200 OK):**
```json
{
  "message": "Logged out successfully"
}
```

### Protected Campaign Endpoints

All campaign endpoints now require authentication. Include the JWT token in the `Authorization` header.

#### **POST /api/campaigns** - Create a campaign (Protected)

```bash
curl -X POST http://localhost:3001/api/campaigns \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "name": "Summer Sale Campaign",
    "platform": "Instagram",
    "affiliate_link": "https://example.com/ref/123",
    "status": "active"
  }'
```

#### **GET /api/campaigns** - Get all campaigns (Protected)

```bash
curl -X GET http://localhost:3001/api/campaigns \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

#### **GET /api/campaigns/:id** - Get campaign by ID (Protected)

```bash
curl -X GET http://localhost:3001/api/campaigns/1234567890 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

#### **PUT /api/campaigns/:id** - Update campaign (Protected)

```bash
curl -X PUT http://localhost:3001/api/campaigns/1234567890 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "status": "completed",
    "conversions": 25
  }'
```

#### **DELETE /api/campaigns/:id** - Delete campaign (Protected)

```bash
curl -X DELETE http://localhost:3001/api/campaigns/1234567890 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

### Protected Transaction Endpoints

All transaction endpoints require authentication tokens.

#### **POST /api/transactions** - Create transaction (Protected)

```bash
curl -X POST http://localhost:3001/api/transactions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{
    "amount": 150.50,
    "type": "commission",
    "description": "Campaign earnings",
    "status": "completed"
  }'
```

#### **GET /api/transactions** - Get all transactions (Protected)

```bash
curl -X GET http://localhost:3001/api/transactions \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

## Error Handling

### 401 - Unauthorized (No Token)
```json
{
  "error": "❌ Not authorized - no token provided"
}
```

**Solution:** Include the JWT token in the Authorization header:
```
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

### 401 - Unauthorized (Invalid Token)
```json
{
  "error": "❌ Not authorized - invalid token"
}
```

**Solution:** Login again to get a fresh token:
```bash
curl -X POST http://localhost:3001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password"
  }'
```

### 400 - Bad Request
```json
{
  "error": "Email and password are required"
}
```

**Solution:** Check that all required fields are included in the request.

## How Authentication Works

### 1. **User Registration**
```
User sends: email + password
     ↓
Supabase creates account & JWT
     ↓
Backend responds with user data
```

### 2. **User Login**
```
User sends: email + password
     ↓
Supabase validates credentials & generates JWT
     ↓
Backend returns JWT token to user
```

### 3. **Accessing Protected Routes**
```
User sends: GET /api/campaigns + Authorization header with JWT
     ↓
Express `protect` middleware extracts & verifies JWT with Supabase
     ↓
Middleware attaches user info to request (req.user)
     ↓
Route handler executes with authenticated user context
     ↓
Response sent back
```

## Code Implementation

### The `protect` Middleware

```javascript
async function protect(req, res, next) {
  try {
    // Extract JWT from Authorization header
    let token;
    if (req.headers.authorization && req.headers.authorization.startsWith('Bearer ')) {
      token = req.headers.authorization.split(' ')[1];
    }

    if (!token) {
      return res.status(401).json({ error: '❌ Not authorized - no token provided' });
    }

    // Verify token with Supabase
    const { data: { user }, error } = await supabase.auth.getUser(token);

    if (error || !user) {
      return res.status(401).json({ error: '❌ Not authorized - invalid token' });
    }

    req.user = user; // Attach user to request
    next(); // Continue to route handler
  } catch (err) {
    res.status(401).json({ error: '❌ Not authorized - token verification failed' });
  }
}
```

### Using `protect` on Routes

```javascript
// Protected route - requires valid JWT
app.get('/api/campaigns', protect, (req, res) => {
  // req.user is available here
  console.log('User:', req.user.id);
  
  // Typically filter campaigns by user
  // const userCampaigns = campaigns.filter(c => c.user_id === req.user.id);
});
```

## Testing

### 1. Run Tests

```bash
python test_auth.py
```

### 2. Manual Testing with cURL

**Step 1: Sign up**
```bash
curl -X POST http://localhost:3001/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123456!"
  }'
```

**Step 2: Login**
```bash
curl -X POST http://localhost:3001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123456!"
  }'
```

**Step 3: Copy the `token` from response**

**Step 4: Create a campaign with token**
```bash
curl -X POST http://localhost:3001/api/campaigns \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN_FROM_STEP_3" \
  -d '{
    "name": "Test Campaign",
    "platform": "TikTok"
  }'
```

## Security Best Practices

✅ **Always use HTTPS in production** - Tokens must be transmitted securely  
✅ **Store tokens securely** - Use localStorage (browser) or secure cookies  
✅ **Never commit .env** - Add to .gitignore  
✅ **Rotate tokens regularly** - Implement token refresh logic  
✅ **Validate on frontend** - Check token before making requests  
✅ **Use strong passwords** - Enforce password requirements  

## Troubleshooting

### "Supabase not configured"
- Check that `.env` file exists
- Verify `SUPABASE_URL` and `SUPABASE_ANON_KEY` are set
- Restart the server: `npm start`

### "Token verification failed"
- Token may have expired - login again
- Token may be malformed - check format
- Supabase credentials may be invalid

### CORS errors when testing from browser
- CORS middleware is already enabled
- Check that request includes proper headers
- Ensure frontend URL is allowed in Supabase settings

## Next Steps

1. ✅ **Frontend Integration** - Connect React frontend to auth endpoints
2. ✅ **Row Level Security** - Set up RLS policies in Supabase
3. ✅ **Token Refresh** - Implement token refresh logic
4. ✅ **Password Reset** - Add forgot password functionality
5. ✅ **Multi-factor Auth** - Enable 2FA support

## Resources

- [Supabase Auth Docs](https://supabase.com/docs/guides/auth)
- [Express Middleware](https://expressjs.com/en/guide/using-middleware.html)
- [JWT Tokens](https://jwt.io/)
- [CORS Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

---

**Questions?** Check the logs: `npm start` shows detailed error messages  
**Ready to deploy?** See `DEPLOYMENT.md` for production setup
