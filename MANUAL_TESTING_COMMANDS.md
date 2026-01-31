# 🧪 MANUAL TESTING GUIDE - Copy & Paste Commands

This guide provides ready-to-use PowerShell commands for testing your authentication system.

## Prerequisites

**Terminal 1 (Keep Running):**
```powershell
cd c:\Users\demon\Desktop\Gemini_api_backend
npm start
```

Wait for output showing: `✅ [Server]: Affiliate AI Backend is running`

---

## Testing Commands (Use Terminal 2)

### TEST 1: Health Check

```powershell
Write-Host "Testing Health Check..." -ForegroundColor Cyan
$response = Invoke-RestMethod -Uri "http://localhost:3001/api/health" -Method Get
$response | ConvertTo-Json
```

**Expected Output:**
```
message
-------
Backend is running!
```

---

### TEST 2: User Signup

```powershell
Write-Host "Testing User Signup..." -ForegroundColor Cyan

$email = "testuser-$(Get-Date -Format 'yyyyMMddHHmmss')@example.com"
Write-Host "Creating user: $email" -ForegroundColor Yellow

$body = @{
    email = $email
    password = "SecurePassword123!"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:3001/api/auth/signup" `
    -Method Post `
    -Headers @{"Content-Type" = "application/json"} `
    -Body $body

Write-Host "✅ Signup successful!" -ForegroundColor Green
$response | ConvertTo-Json
```

**Expected Output:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": "some-uuid",
    "email": "testuser-...@example.com"
  }
}
```

---

### TEST 3: User Login (GET JWT TOKEN)

**⚠️ IMPORTANT:** Use the same email from TEST 2!

```powershell
Write-Host "Testing User Login..." -ForegroundColor Cyan

$email = "testuser-YYYYMMDDHHMMSS@example.com"  # Use email from TEST 2
Write-Host "Logging in as: $email" -ForegroundColor Yellow

$body = @{
    email = $email
    password = "SecurePassword123!"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:3001/api/auth/login" `
    -Method Post `
    -Headers @{"Content-Type" = "application/json"} `
    -Body $body

Write-Host "✅ Login successful!" -ForegroundColor Green
$response | ConvertTo-Json

# SAVE THE TOKEN
$TOKEN = $response.token
Write-Host "Token saved: $($TOKEN.Substring(0, 50))..." -ForegroundColor Magenta
```

**Expected Output:**
```json
{
  "message": "Login successful",
  "user": {
    "id": "some-uuid",
    "email": "testuser-...@example.com"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**⚠️ CRITICAL:** Copy the token value. You'll need it for all remaining tests.

---

### TEST 4: Protected Route WITHOUT Token (Should Fail)

```powershell
Write-Host "Testing Protected Route WITHOUT token..." -ForegroundColor Cyan
Write-Host "(Should return 401 Unauthorized)" -ForegroundColor Yellow

try {
    $response = Invoke-RestMethod -Uri "http://localhost:3001/api/campaigns" `
        -Method Get `
        -ErrorAction Stop
    
    Write-Host "❌ FAILED: Should have been rejected!" -ForegroundColor Red
} catch {
    if ($_.Exception.Response.StatusCode -eq 401) {
        Write-Host "✅ Correctly rejected!" -ForegroundColor Green
        Write-Host "Status: 401 Unauthorized"
        Write-Host "Error: $($_.ErrorDetails.Message)"
    } else {
        Write-Host "❌ Unexpected error: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    }
}
```

**Expected Output:**
```
✅ Correctly rejected!
Status: 401 Unauthorized
Error: ❌ Not authorized - no token provided
```

---

### TEST 5: Protected Route WITH Token (Should Succeed)

**⚠️ REQUIRED:** Paste the token from TEST 3!

```powershell
Write-Host "Testing Protected Route WITH token..." -ForegroundColor Cyan

$TOKEN = "PASTE_YOUR_TOKEN_HERE"  # From TEST 3

Write-Host "Using token: $($TOKEN.Substring(0, 50))..." -ForegroundColor Yellow

$response = Invoke-RestMethod -Uri "http://localhost:3001/api/campaigns" `
    -Method Get `
    -Headers @{"Authorization" = "Bearer $TOKEN"}

Write-Host "✅ Success!" -ForegroundColor Green
$response | ConvertTo-Json
```

**Expected Output:**
```json
[]
```

(Empty array is fine - you haven't created campaigns yet)

---

### TEST 6: Create Campaign (Protected)

**⚠️ REQUIRED:** Use token from TEST 3!

```powershell
Write-Host "Creating a campaign..." -ForegroundColor Cyan

$TOKEN = "PASTE_YOUR_TOKEN_HERE"  # From TEST 3

$body = @{
    name = "Test Campaign $(Get-Date -Format 'yyyyMMdd-HHmmss')"
    platform = "Instagram"
    status = "active"
    clicks = 5
    conversions = 2
    earnings = 50.00
    affiliate_link = "https://example.com/ref/123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:3001/api/campaigns" `
    -Method Post `
    -Headers @{
        "Content-Type" = "application/json"
        "Authorization" = "Bearer $TOKEN"
    } `
    -Body $body

Write-Host "✅ Campaign created!" -ForegroundColor Green
$response | ConvertTo-Json

# SAVE THE ID
$CAMPAIGN_ID = $response.id
Write-Host "Campaign ID: $CAMPAIGN_ID" -ForegroundColor Magenta
```

**Expected Output:**
```json
{
  "id": "1234567890",
  "name": "Test Campaign 20260127-120000",
  "platform": "Instagram",
  "status": "active",
  "clicks": 5,
  "conversions": 2,
  "earnings": 50,
  ...
}
```

---

### TEST 7: Get Campaign (Protected)

**⚠️ REQUIRED:** Use token from TEST 3 and ID from TEST 6!

```powershell
Write-Host "Getting campaign details..." -ForegroundColor Cyan

$TOKEN = "PASTE_YOUR_TOKEN_HERE"      # From TEST 3
$CAMPAIGN_ID = "PASTE_CAMPAIGN_ID"    # From TEST 6

Write-Host "Getting campaign: $CAMPAIGN_ID" -ForegroundColor Yellow

$response = Invoke-RestMethod -Uri "http://localhost:3001/api/campaigns/$CAMPAIGN_ID" `
    -Method Get `
    -Headers @{"Authorization" = "Bearer $TOKEN"}

Write-Host "✅ Campaign retrieved!" -ForegroundColor Green
$response | ConvertTo-Json
```

**Expected Output:**
```json
{
  "id": "1234567890",
  "name": "Test Campaign 20260127-120000",
  "platform": "Instagram",
  ...
}
```

---

### TEST 8: Update Campaign (Protected)

**⚠️ REQUIRED:** Use token from TEST 3 and ID from TEST 6!

```powershell
Write-Host "Updating campaign..." -ForegroundColor Cyan

$TOKEN = "PASTE_YOUR_TOKEN_HERE"      # From TEST 3
$CAMPAIGN_ID = "PASTE_CAMPAIGN_ID"    # From TEST 6

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

Write-Host "✅ Campaign updated!" -ForegroundColor Green
$response | ConvertTo-Json
```

**Expected Output:**
```json
{
  "id": "1234567890",
  "name": "Test Campaign 20260127-120000",
  "status": "completed",
  "conversions": 10,
  "earnings": 100,
  ...
}
```

---

### TEST 9: Delete Campaign (Protected)

**⚠️ REQUIRED:** Use token from TEST 3 and ID from TEST 6!

```powershell
Write-Host "Deleting campaign..." -ForegroundColor Cyan

$TOKEN = "PASTE_YOUR_TOKEN_HERE"      # From TEST 3
$CAMPAIGN_ID = "PASTE_CAMPAIGN_ID"    # From TEST 6

$response = Invoke-RestMethod -Uri "http://localhost:3001/api/campaigns/$CAMPAIGN_ID" `
    -Method Delete `
    -Headers @{"Authorization" = "Bearer $TOKEN"}

Write-Host "✅ Campaign deleted!" -ForegroundColor Green
$response | ConvertTo-Json
```

**Expected Output:**
```json
{
  "message": "Campaign deleted successfully",
  "id": "1234567890"
}
```

---

### TEST 10: Create Transaction (Protected)

**⚠️ REQUIRED:** Use token from TEST 3!

```powershell
Write-Host "Creating a transaction..." -ForegroundColor Cyan

$TOKEN = "PASTE_YOUR_TOKEN_HERE"  # From TEST 3

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

Write-Host "✅ Transaction created!" -ForegroundColor Green
$response | ConvertTo-Json
```

**Expected Output:**
```json
{
  "id": "1234567890",
  "amount": 150.5,
  "type": "commission",
  "status": "completed",
  ...
}
```

---

### TEST 11: Get All Transactions (Protected)

**⚠️ REQUIRED:** Use token from TEST 3!

```powershell
Write-Host "Getting all transactions..." -ForegroundColor Cyan

$TOKEN = "PASTE_YOUR_TOKEN_HERE"  # From TEST 3

$response = Invoke-RestMethod -Uri "http://localhost:3001/api/transactions" `
    -Method Get `
    -Headers @{"Authorization" = "Bearer $TOKEN"}

Write-Host "✅ Transactions retrieved!" -ForegroundColor Green
$response | ConvertTo-Json -Depth 2
```

**Expected Output:**
```json
[
  {
    "id": "1234567890",
    "amount": 150.5,
    "type": "commission",
    ...
  }
]
```

---

## Quick Copy-Paste Template

For repeated testing, use this template:

```powershell
# Configuration
$BASE_URL = "http://localhost:3001"
$TOKEN = "PASTE_TOKEN_FROM_LOGIN"
$CAMPAIGN_ID = "PASTE_ID_FROM_CREATE"

# Health Check
Invoke-RestMethod -Uri "$BASE_URL/api/health" -Method Get | ConvertTo-Json

# Get Campaigns
Invoke-RestMethod -Uri "$BASE_URL/api/campaigns" -Method Get `
    -Headers @{"Authorization" = "Bearer $TOKEN"} | ConvertTo-Json

# Create Campaign
$body = @{name="Test"; platform="Instagram"} | ConvertTo-Json
Invoke-RestMethod -Uri "$BASE_URL/api/campaigns" -Method Post `
    -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $TOKEN"} `
    -Body $body | ConvertTo-Json
```

---

## Success Criteria

You're all set when you see:
- ✅ Health check returns 200
- ✅ Signup creates user
- ✅ Login returns JWT token
- ✅ Test 4 returns 401 (no token)
- ✅ Test 5 returns 200 (with token)
- ✅ Campaign CRUD works with token
- ✅ Transactions CRUD works with token

---

## Troubleshooting

**"No connection could be made"**
- Is server running? Check Terminal 1
- Run: `npm start` in Terminal 1
- Wait 2-3 seconds for startup

**"Not authorized - no token provided"**
- This is correct! Add Authorization header
- Use: `-Headers @{"Authorization" = "Bearer $TOKEN"}`

**"Invalid token"**
- Token expired? Get new one from login
- Supabase not configured? Use demo mode (it works!)

**"Email already exists"**
- Use new email with timestamp:
- `"test-$(Get-Date -Format 'yyyyMMddHHmmss')@example.com"`

---

**Ready?** Start with TEST 1 and work through sequentially! 🚀
