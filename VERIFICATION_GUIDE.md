# 🧪 Authentication Verification Guide - Step by Step

## Overview

This guide walks you through verifying that your JWT authentication implementation is working correctly. Follow each step carefully.

---

## Prerequisites Checklist

Before starting, ensure you have:
- [ ] Node.js v14+ installed (we detected v24.13.0 ✅)
- [ ] npm installed (we detected v11.6.2 ✅)
- [ ] Supabase project created (optional, can use demo mode)
- [ ] .env file configured with Supabase credentials (optional)

---

## Step-by-Step Verification

### STEP 1: Configure Environment Variables

Create a `.env` file in your project root directory:

```bash
# On Windows (PowerShell):
Copy-Item .env.example .env

# Then edit .env and add your Supabase credentials:
```

**Option A: With Supabase (Recommended for Production)**

Edit `.env` and add:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-public-api-key-here
PORT=3001
NODE_ENV=development
```

Get these from: [Supabase Dashboard](https://app.supabase.com) → Settings → API

**Option B: Demo Mode (Testing Without Supabase)**

If you don't have Supabase credentials yet, the system works in demo mode:
```
PORT=3001
NODE_ENV=development
```

(SUPABASE_URL and SUPABASE_ANON_KEY can be omitted)

---

### STEP 2: Install Dependencies

```bash
cd c:\Users\demon\Desktop\Gemini_api_backend
npm install
```

Expected output:
```
> npm install
up to date, audited 3 packages in 0.5s
```

---

### STEP 3: Start the Backend Server

```bash
npm start
```

Expected output:
```
✅ [Supabase]: Initialized
✅ [Server]: Affiliate AI Backend is running on http://localhost:3001
📡 API Base URL: http://localhost:3001/api

Available endpoints:
  POST   /api/campaigns       - Create a campaign
  GET    /api/campaigns       - Get all campaigns
  GET    /api/campaigns/:id   - Get a campaign by ID
  PUT    /api/campaigns/:id   - Update a campaign
  DELETE /api/campaigns/:id   - Delete a campaign
  POST   /api/transactions    - Create a transaction
  GET    /api/transactions    - Get all transactions
  GET    /api/health          - Health check
```

**⚠️ If you see:** `⚠️ [Supabase]: Not configured...`
- This is normal! The system works in demo mode
- Add Supabase credentials to .env to enable full authentication

---

### STEP 4: Test Authentication Endpoints

Open a **new terminal window** (keep the server running in the first window).

#### Test 4A: Health Check

```powershell
$response = Invoke-RestMethod -Uri "http://localhost:3001/api/health" -Method Get
$response
```

Expected:
```
message
-------
Backend is running!
```

#### Test 4B: User Signup

```powershell
$body = @{
    email = "testuser@example.com"
    password = "SecurePassword123!"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:3001/api/auth/signup" `
    -Method Post `
    -Headers @{"Content-Type" = "application/json"} `
    -Body $body

$response | ConvertTo-Json
```

Expected (201 Created):
```json
{
  "message": "User registered successfully",
  "user": {
    "id": "user-uuid-here",
    "email": "testuser@example.com"
  }
}
```

**Error:** If you get `{ "error": "Email already exists" }`
- Use a different email like `testuser-$(Get-Date -Format 'yyyyMMddHHmmss')@example.com`

#### Test 4C: User Login

```powershell
$body = @{
    email = "testuser@example.com"
    password = "SecurePassword123!"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:3001/api/auth/login" `
    -Method Post `
    -Headers @{"Content-Type" = "application/json"} `
    -Body $body

$response | ConvertTo-Json
```

Expected (200 OK):
```json
{
  "message": "Login successful",
  "user": {
    "id": "user-uuid-here",
    "email": "testuser@example.com"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**✅ IMPORTANT:** Copy the `token` value - you'll need it for the next tests!

---

### STEP 5: Test Protected Routes WITHOUT Token

This should fail with 401 Unauthorized.

```powershell
try {
    $response = Invoke-RestMethod -Uri "http://localhost:3001/api/campaigns" `
        -Method Get
    Write-Host "❌ FAILED: Should have been rejected" -ForegroundColor Red
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-Host "✅ PASSED: Correctly rejected without token (401)" -ForegroundColor Green
        Write-Host "Error message: $($_.ErrorDetails.Message)"
    }
}
```

Expected error:
```
❌ Not authorized - no token provided
```

---

### STEP 6: Test Protected Routes WITH Token

This should succeed with 200 OK.

```powershell
# Replace YOUR_TOKEN_HERE with the token from Step 4C
$TOKEN = "YOUR_TOKEN_HERE"

$response = Invoke-RestMethod -Uri "http://localhost:3001/api/campaigns" `
    -Method Get `
    -Headers @{"Authorization" = "Bearer $TOKEN"}

$response | ConvertTo-Json
```

Expected (200 OK):
```json
[]
```

(Empty array because no campaigns created yet, but the request succeeded!)

---

### STEP 7: Test Protected Route - Create Campaign

```powershell
$TOKEN = "YOUR_TOKEN_HERE"

$body = @{
    name = "Test Campaign"
    platform = "Instagram"
    affiliate_link = "https://example.com/ref/123"
    status = "active"
    clicks = 5
    conversions = 2
    earnings = 50.00
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:3001/api/campaigns" `
    -Method Post `
    -Headers @{
        "Content-Type" = "application/json"
        "Authorization" = "Bearer $TOKEN"
    } `
    -Body $body

$response | ConvertTo-Json
```

Expected (201 Created):
```json
{
  "id": "1234567890",
  "name": "Test Campaign",
  "platform": "Instagram",
  "affiliate_link": "https://example.com/ref/123",
  "status": "active",
  "clicks": 5,
  "conversions": 2,
  "earnings": 50,
  "created_at": "2026-01-27T12:00:00.000Z"
}
```

---

### STEP 8: Test Protected Route - Get Campaign

```powershell
$TOKEN = "YOUR_TOKEN_HERE"
$CAMPAIGN_ID = "1234567890"  # Use the ID from Step 7

$response = Invoke-RestMethod -Uri "http://localhost:3001/api/campaigns/$CAMPAIGN_ID" `
    -Method Get `
    -Headers @{"Authorization" = "Bearer $TOKEN"}

$response | ConvertTo-Json
```

Expected (200 OK):
```json
{
  "id": "1234567890",
  "name": "Test Campaign",
  "platform": "Instagram",
  ...
}
```

---

### STEP 9: Test Protected Route - Update Campaign

```powershell
$TOKEN = "YOUR_TOKEN_HERE"
$CAMPAIGN_ID = "1234567890"

$body = @{
    status = "completed"
    conversions = 10
    earnings = 100.00
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:3001/api/campaigns/$CAMPAIGN_ID" `
    -Method Put `
    -Headers @{
        "Content-Type" = "application/json"
        "Authorization" = "Bearer $TOKEN"
    } `
    -Body $body

$response | ConvertTo-Json
```

Expected (200 OK):
```json
{
  "id": "1234567890",
  "name": "Test Campaign",
  "status": "completed",
  "conversions": 10,
  "earnings": 100,
  ...
}
```

---

### STEP 10: Test Transaction Endpoints

```powershell
$TOKEN = "YOUR_TOKEN_HERE"

# Create transaction
$body = @{
    amount = 150.50
    type = "commission"
    description = "Campaign earnings"
    payment_method = "stripe"
    status = "completed"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:3001/api/transactions" `
    -Method Post `
    -Headers @{
        "Content-Type" = "application/json"
        "Authorization" = "Bearer $TOKEN"
    } `
    -Body $body

$response | ConvertTo-Json

# Get all transactions
$response = Invoke-RestMethod -Uri "http://localhost:3001/api/transactions" `
    -Method Get `
    -Headers @{"Authorization" = "Bearer $TOKEN"}

$response | ConvertTo-Json
```

---

## Test Results Checklist

Go through each test and mark it:

- [ ] **Step 1:** ✅ Environment variables configured
- [ ] **Step 2:** ✅ npm install completed
- [ ] **Step 3:** ✅ Server started successfully
- [ ] **Step 4A:** ✅ Health check returned 200
- [ ] **Step 4B:** ✅ Signup successful (201)
- [ ] **Step 4C:** ✅ Login successful, JWT token received
- [ ] **Step 5:** ✅ Protected route rejected without token (401)
- [ ] **Step 6:** ✅ Protected route accepted with token (200)
- [ ] **Step 7:** ✅ Campaign created successfully (201)
- [ ] **Step 8:** ✅ Campaign retrieved successfully (200)
- [ ] **Step 9:** ✅ Campaign updated successfully (200)
- [ ] **Step 10:** ✅ Transactions working with auth

---

## Automated Testing

### Option 1: Run PowerShell Script

```powershell
# Make sure server is running first (npm start in another terminal)
# Then run:
./test_auth_verification.ps1
```

This runs all tests automatically and shows a summary.

### Option 2: Run Python Tests

```bash
python test_auth.py
```

This runs comprehensive tests with detailed output.

---

## Error Troubleshooting

### Error: "Server not responding"
```
❌ Server not responding. Start with: npm start
```
**Solution:**
- Run `npm start` in a terminal
- Verify it shows: `✅ [Server]: Affiliate AI Backend is running`
- Wait a few seconds for server to fully start

### Error: "Connection refused"
```
Connect-to-Host : Unable to connect to the remote server
```
**Solution:**
- Make sure server is running: `npm start`
- Check server is on port 3001
- Verify no other process is using port 3001

### Error: "Not authorized - no token provided"
```
{
  "error": "❌ Not authorized - no token provided"
}
```
**Solution:**
- This is correct behavior! The route is protected
- Include the Authorization header: `Authorization: Bearer TOKEN`
- Get token from login response

### Error: "Invalid token"
```
{
  "error": "❌ Not authorized - invalid token"
}
```
**Solution:**
- Token may have expired
- Login again to get fresh token
- Verify token format (should start with "eyJ")
- Check Supabase credentials in .env

### Error: "Supabase not configured"
```
⚠️ [Supabase]: Not configured. Set SUPABASE_URL and SUPABASE_ANON_KEY
```
**Solution:**
- This is normal if you don't have Supabase set up yet
- System works in demo mode without it
- To enable Supabase auth:
  1. Get credentials from https://app.supabase.com
  2. Add to .env: SUPABASE_URL and SUPABASE_ANON_KEY
  3. Restart server: npm start

---

## What's Working?

✅ **Server is running**
- Health check working
- Server responding to requests

✅ **Authentication endpoints working**
- Signup creating users
- Login returning tokens
- Logout signing out users

✅ **Route protection working**
- 401 without token
- 200 with valid token
- User context available (req.user)

✅ **Data endpoints working**
- Campaigns CRUD protected
- Transactions CRUD protected
- All require valid JWT

---

## Next Steps

Once all tests pass:

### 1. **Immediate Next:** Row Level Security (RLS)
Set up database-level protection so even if someone bypassed your backend, the database would still enforce user isolation.

See: SECURITY_IMPLEMENTATION_GUIDE.md → Step 3: RLS Policies

### 2. **Frontend Development:** Vue.js PWA
Build login/signup screens and integrate with your authenticated backend.

### 3. **Production Deployment**
- Use HTTPS (never HTTP)
- Store tokens securely (httpOnly cookies or localStorage with caution)
- Implement token refresh
- Enable CORS properly

---

## Summary

Your authentication system is **working correctly** if:
1. ✅ Health check returns 200
2. ✅ Signup creates users
3. ✅ Login returns tokens
4. ✅ Protected routes reject without token (401)
5. ✅ Protected routes accept with token (200)
6. ✅ CRUD operations work with token

**If all 6 are working:** You're ready for production! 🚀

---

## Quick Reference

### Signup
```powershell
$body = @{email="user@example.com"; password="Pass123!"} | ConvertTo-Json
Invoke-RestMethod "http://localhost:3001/api/auth/signup" -Method Post -Headers @{"Content-Type"="application/json"} -Body $body
```

### Login
```powershell
$body = @{email="user@example.com"; password="Pass123!"} | ConvertTo-Json
$login = Invoke-RestMethod "http://localhost:3001/api/auth/login" -Method Post -Headers @{"Content-Type"="application/json"} -Body $body
$token = $login.token
```

### Protected Request
```powershell
Invoke-RestMethod "http://localhost:3001/api/campaigns" -Method Get -Headers @{"Authorization"="Bearer $token"}
```

---

**Status:** Ready for verification
**Time to complete:** 15-30 minutes
**Difficulty:** Easy

Let's test it! 🧪
