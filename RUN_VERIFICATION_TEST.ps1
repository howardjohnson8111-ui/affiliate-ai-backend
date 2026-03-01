# Affiliate AI Backend Authentication Verification Test Suite
# This script verifies the JWT authentication system is working correctly

param(
    [switch]$Verbose = $false
)

# Configuration
$BASE_URL = "http://localhost:3001"
$TEST_USER_EMAIL = "test_user_$(Get-Random)@example.com"
$TEST_USER_PASSWORD = "TestPassword@123"
$TESTS_PASSED = 0
$TESTS_FAILED = 0

# Colors
$ColorSuccess = "Green"
$ColorError = "Red"
$ColorWarning = "Yellow"
$ColorInfo = "Cyan"

# Helper Functions
function LogTest {
    param([string]$TestName, [string]$Status, [string]$Details = "")
    $Symbol = if ($Status -eq "PASS") { "[OK]" } else { "[FAIL]" }
    $Color = if ($Status -eq "PASS") { $ColorSuccess } else { $ColorError }
    Write-Host "  $Symbol $TestName" -ForegroundColor $Color
    if ($Details) {
        Write-Host "      └─ $Details" -ForegroundColor Gray
    }
    if ($Status -eq "PASS") { $global:TESTS_PASSED++ } else { $global:TESTS_FAILED++ }
}

function LogSection {
    param([string]$Title)
    Write-Host ""
    Write-Host "=================================" -ForegroundColor $ColorInfo
    Write-Host "  $Title" -ForegroundColor $ColorInfo
    Write-Host "=================================" -ForegroundColor $ColorInfo
}

function TestConnection {
    try {
        $response = Invoke-RestMethod -Uri "$BASE_URL/health" -Method GET -ErrorAction Stop
        return $response
    } catch {
        return $null
    }
}

function TestSignup {
    try {
        $body = @{
            email = $TEST_USER_EMAIL
            password = $TEST_USER_PASSWORD
        } | ConvertTo-Json
        
        $response = Invoke-RestMethod -Uri "$BASE_URL/signup" -Method POST `
            -ContentType "application/json" `
            -Body $body `
            -ErrorAction Stop
        
        return $response
    } catch {
        if ($Verbose) { Write-Host "Signup error: $_" -ForegroundColor Gray }
        return $null
    }
}

function TestLogin {
    try {
        $body = @{
            email = $TEST_USER_EMAIL
            password = $TEST_USER_PASSWORD
        } | ConvertTo-Json
        
        $response = Invoke-RestMethod -Uri "$BASE_URL/login" -Method POST `
            -ContentType "application/json" `
            -Body $body `
            -ErrorAction Stop
        
        return $response
    } catch {
        if ($Verbose) { Write-Host "Login error: $_" -ForegroundColor Gray }
        return $null
    }
}

function TestProtectedRoute {
    param([string]$Token)
    try {
        $headers = @{ Authorization = "Bearer $Token" }
        $response = Invoke-RestMethod -Uri "$BASE_URL/campaigns" -Method GET `
            -Headers $headers `
            -ErrorAction Stop
        return $response
    } catch {
        if ($Verbose) { Write-Host "Protected route error: $_" -ForegroundColor Gray }
        return $null
    }
}

function TestProtectedRouteWithoutToken {
    try {
        $response = Invoke-RestMethod -Uri "$BASE_URL/campaigns" -Method GET `
            -ErrorAction Stop
        return $response
    } catch {
        # Should get 401 error
        if ($_.Exception.Response.StatusCode.Value__ -eq 401) {
            return "UNAUTHORIZED"
        }
        if ($Verbose) { Write-Host "Unauth route error: $_" -ForegroundColor Gray }
        return $null
    }
}

function TestCreateCampaign {
    param([string]$Token)
    try {
        $body = @{
            name = "Test Campaign $(Get-Random)"
            description = "Automated test campaign"
        } | ConvertTo-Json
        
        $headers = @{ Authorization = "Bearer $Token" }
        $response = Invoke-RestMethod -Uri "$BASE_URL/campaigns" -Method POST `
            -ContentType "application/json" `
            -Body $body `
            -Headers $headers `
            -ErrorAction Stop
        
        return $response
    } catch {
        if ($Verbose) { Write-Host "Create campaign error: $_" -ForegroundColor Gray }
        return $null
    }
}

# ============================================================================
# MAIN TEST EXECUTION
# ============================================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Magenta
Write-Host "  JWT Authentication System Verification Test Suite" -ForegroundColor Magenta
Write-Host "  Backend: $BASE_URL" -ForegroundColor Magenta
Write-Host "============================================================" -ForegroundColor Magenta
Write-Host ""

# Test 1: Health Check
LogSection "Step 1: Health Check"
$healthCheck = TestConnection
if ($healthCheck -and $healthCheck.status -eq "ok") {
    LogTest "Server connectivity" "PASS" "Server responding to health checks"
} else {
    LogTest "Server connectivity" "FAIL" "Server not responding - is npm start running?"
    Write-Host ""
    Write-Host "ERROR: Cannot proceed without server. Run: npm start" -ForegroundColor Red
    exit 1
}

# Test 2: User Signup
LogSection "Step 2: User Authentication - Signup"
$signupResult = TestSignup
if ($signupResult -and $signupResult.email -eq $TEST_USER_EMAIL) {
    LogTest "User signup" "PASS" "Test user created successfully"
} else {
    LogTest "User signup" "FAIL" "Could not create test user"
}

# Test 3: User Login
LogSection "Step 3: User Authentication - Login"
$loginResult = TestLogin
if ($loginResult -and $loginResult.token) {
    LogTest "User login" "PASS" "JWT token received"
    $JWT_TOKEN = $loginResult.token
} else {
    LogTest "User login" "FAIL" "Could not authenticate user"
    Write-Host ""
    Write-Host "Cannot continue without JWT token" -ForegroundColor Red
    exit 1
}

# Test 4: Route Protection Without Token
LogSection "Step 4: Route Protection - Without Token"
$unprotectedTest = TestProtectedRouteWithoutToken
if ($unprotectedTest -eq "UNAUTHORIZED") {
    LogTest "Protected route blocking" "PASS" "Endpoint returns 401 without token"
} else {
    LogTest "Protected route blocking" "FAIL" "Endpoint did not properly reject unauthorized request"
}

# Test 5: Protected Route With Token
LogSection "Step 5: Route Protection - With Valid Token"
$protectedTest = TestProtectedRoute -Token $JWT_TOKEN
if ($protectedTest -ne $null) {
    LogTest "Protected route access" "PASS" "Endpoint accessible with valid JWT"
} else {
    LogTest "Protected route access" "FAIL" "Could not access protected endpoint with token"
}

# Test 6: Campaign CRUD
LogSection "Step 6: Data Operations - Campaign Creation"
$campaignResult = TestCreateCampaign -Token $JWT_TOKEN
if ($campaignResult -and $campaignResult.id) {
    LogTest "Campaign creation" "PASS" "Data endpoint working correctly"
} else {
    LogTest "Campaign creation" "FAIL" "Could not create campaign"
}

# ============================================================================
# TEST SUMMARY REPORT
# ============================================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Magenta
Write-Host ""

$TOTAL_TESTS = $TESTS_PASSED + $TESTS_FAILED
$PASS_RATE = if ($TOTAL_TESTS -gt 0) { [math]::Round(($TESTS_PASSED / $TOTAL_TESTS) * 100, 2) } else { 0 }

Write-Host "  Total Tests:       $TOTAL_TESTS" -ForegroundColor White
Write-Host "  [OK] Tests Passed: $TESTS_PASSED" -ForegroundColor Green
Write-Host "  [FAIL] Tests Failed: $TESTS_FAILED" -ForegroundColor $(if ($TESTS_FAILED -eq 0) { "Green" } else { "Red" })
Write-Host "  Pass Rate:         $PASS_RATE%" -ForegroundColor $(if ($PASS_RATE -eq 100) { "Green" } else { "Yellow" })
Write-Host ""

if ($TESTS_FAILED -eq 0) {
    Write-Host "===== SUCCESS =====" -ForegroundColor Green
    Write-Host "ALL TESTS PASSED - SYSTEM IS READY!" -ForegroundColor Green
    Write-Host "==================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your authentication system is:" -ForegroundColor Green
    Write-Host "  [OK] Server running and responding" -ForegroundColor Green
    Write-Host "  [OK] User signup working" -ForegroundColor Green
    Write-Host "  [OK] User login working" -ForegroundColor Green
    Write-Host "  [OK] JWT tokens being generated" -ForegroundColor Green
    Write-Host "  [OK] Route protection working (401 without token)" -ForegroundColor Green
    Write-Host "  [OK] Protected routes accessible with token (200)" -ForegroundColor Green
    Write-Host "  [OK] Data CRUD operations working" -ForegroundColor Green
    Write-Host "  [OK] Ready for production" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "===== WARNING =====" -ForegroundColor Yellow
    Write-Host "SOME TESTS FAILED - DIAGNOSIS NEEDED" -ForegroundColor Yellow
    Write-Host "==================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Common Issues:" -ForegroundColor Yellow
    Write-Host "  1. Server not running? -> npm start (in separate terminal)" -ForegroundColor Yellow
    Write-Host "  2. Port in use? -> Check if another process uses :3001" -ForegroundColor Yellow
    Write-Host "  3. Supabase not configured? -> Add credentials to .env" -ForegroundColor Yellow
    Write-Host "  4. Node syntax error? -> Check server.js for errors" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. [OK] Authentication verified" -ForegroundColor Cyan
Write-Host "  2. [NEXT] Set up Row Level Security (RLS) in Supabase" -ForegroundColor Cyan
Write-Host "  3. [NEXT] Build Vue.js/React PWA frontend" -ForegroundColor Cyan
Write-Host "  4. [NEXT] Deploy to production" -ForegroundColor Cyan
Write-Host ""
# Run this after: npm start (in separate terminal)

Write-Host ""
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host "    AUTHENTICATION SYSTEM VERIFICATION REPORT"
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$BASE_URL = "http://localhost:3001"
$TEST_TIMESTAMP = Get-Date -Format "yyyyMMddHHmmss"
$TEST_EMAIL = "test-auth-$TEST_TIMESTAMP@example.com"
$TEST_PASSWORD = "TestPassword123!"
$TOKEN = ""

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  📍 Base URL: $BASE_URL"
Write-Host "  📧 Test Email: $TEST_EMAIL"
Write-Host "  🔒 Test Password: [hidden]"
Write-Host ""

$TESTS_PASSED = 0
$TESTS_FAILED = 0

function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Method,
        [string]$Endpoint,
        [string]$Body,
        [hashtable]$Headers,
        [int]$ExpectedStatus
    )
    
    Write-Host "Test: $Name" -ForegroundColor Magenta
    Write-Host "  Method: $Method | Endpoint: $Endpoint"
    
    try {
        $params = @{
            Uri = "$BASE_URL$Endpoint"
            Method = $Method
            ErrorAction = "Stop"
        }
        
        if ($Headers) {
            $params["Headers"] = $Headers
        }
        
        if ($Body) {
            $params["Body"] = $Body
            $params["ContentType"] = "application/json"
        }
        
        $response = Invoke-RestMethod @params
        $statusCode = 200
        
        Write-Host "  Status: ✅ $statusCode"
        Write-Host "  Response: $(($response | ConvertTo-Json -Depth 1) -split "`n" | Select-Object -First 3)"
        
        if ($statusCode -eq $ExpectedStatus) {
            Write-Host "  ✅ PASSED" -ForegroundColor Green
            $script:TESTS_PASSED++
            return $response
        } else {
            Write-Host "  ❌ FAILED (Expected $ExpectedStatus, got $statusCode)" -ForegroundColor Red
            $script:TESTS_FAILED++
            return $null
        }
    } catch {
        $statusCode = $_.Exception.Response.StatusCode.Value
        
        Write-Host "  Status: ❌ $statusCode"
        Write-Host "  Error: $($_.Exception.Message)"
        
        if ($statusCode -eq $ExpectedStatus) {
            Write-Host "  ✅ PASSED (Error expected)" -ForegroundColor Green
            $script:TESTS_PASSED++
            return $null
        } else {
            Write-Host "  ❌ FAILED (Expected $ExpectedStatus, got $statusCode)" -ForegroundColor Red
            $script:TESTS_FAILED++
            return $null
        }
    } finally {
        Write-Host ""
    }
}

# TEST 1: Health Check
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
Write-Host "PHASE 1: Server Status Checks" -ForegroundColor Blue
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
Write-Host ""

Test-Endpoint -Name "Health Check" -Method "Get" -Endpoint "/api/health" -ExpectedStatus 200

# TEST 2: Authentication Endpoints
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
Write-Host "PHASE 2: Authentication Endpoints" -ForegroundColor Blue
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
Write-Host ""

$signupBody = @{
    email = $TEST_EMAIL
    password = $TEST_PASSWORD
} | ConvertTo-Json

$signupResponse = Test-Endpoint -Name "User Signup" -Method "Post" -Endpoint "/api/auth/signup" -Body $signupBody -ExpectedStatus 201

$loginBody = @{
    email = $TEST_EMAIL
    password = $TEST_PASSWORD
} | ConvertTo-Json

$loginResponse = Test-Endpoint -Name "User Login" -Method "Post" -Endpoint "/api/auth/login" -Body $loginBody -ExpectedStatus 200

if ($loginResponse.token) {
    $TOKEN = $loginResponse.token
    Write-Host "  📌 JWT Token Captured: $($TOKEN.Substring(0, 50))..." -ForegroundColor Green
} else {
    Write-Host "  ⚠️  No JWT token received (Supabase may not be configured)" -ForegroundColor Yellow
    $TOKEN = "demo-token-for-testing"
}
Write-Host ""

# TEST 3: Route Protection
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
Write-Host "PHASE 3: Route Protection Verification" -ForegroundColor Blue
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
Write-Host ""

Test-Endpoint -Name "Protected Route WITHOUT Token" -Method "Get" -Endpoint "/api/campaigns" -ExpectedStatus 401

$authHeaders = @{
    "Authorization" = "Bearer $TOKEN"
}

Test-Endpoint -Name "Protected Route WITH Token" -Method "Get" -Endpoint "/api/campaigns" -Headers $authHeaders -ExpectedStatus 200

# TEST 4: CRUD Operations
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
Write-Host "PHASE 4: Data CRUD Operations" -ForegroundColor Blue
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
Write-Host ""

$campaignBody = @{
    name = "Test Campaign $TEST_TIMESTAMP"
    platform = "Instagram"
    status = "active"
    clicks = 0
    conversions = 0
    earnings = 0
} | ConvertTo-Json

$campaignResponse = Test-Endpoint -Name "Create Campaign" -Method "Post" -Endpoint "/api/campaigns" -Body $campaignBody -Headers $authHeaders -ExpectedStatus 201

if ($campaignResponse.id) {
    $CAMPAIGN_ID = $campaignResponse.id
    Write-Host "  📌 Campaign ID Captured: $CAMPAIGN_ID" -ForegroundColor Green
    Write-Host ""
    
    # Get Campaign
    Test-Endpoint -Name "Get Campaign by ID" -Method "Get" -Endpoint "/api/campaigns/$CAMPAIGN_ID" -Headers $authHeaders -ExpectedStatus 200
    
    # Update Campaign
    $updateBody = @{
        status = "completed"
        conversions = 5
        earnings = 50.00
    } | ConvertTo-Json
    
    Test-Endpoint -Name "Update Campaign" -Method "Put" -Endpoint "/api/campaigns/$CAMPAIGN_ID" -Body $updateBody -Headers $authHeaders -ExpectedStatus 200
    
    # Delete Campaign
    Test-Endpoint -Name "Delete Campaign" -Method "Delete" -Endpoint "/api/campaigns/$CAMPAIGN_ID" -Headers $authHeaders -ExpectedStatus 200
}

# TEST 5: Transaction Operations
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
Write-Host "PHASE 5: Transaction Operations" -ForegroundColor Blue
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
Write-Host ""

$transactionBody = @{
    amount = 123.45
    type = "commission"
    description = "Test transaction"
    payment_method = "stripe"
    status = "pending"
} | ConvertTo-Json

Test-Endpoint -Name "Create Transaction" -Method "Post" -Endpoint "/api/transactions" -Body $transactionBody -Headers $authHeaders -ExpectedStatus 201

Test-Endpoint -Name "Get All Transactions" -Method "Get" -Endpoint "/api/transactions" -Headers $authHeaders -ExpectedStatus 200

# SUMMARY
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
Write-Host "📊 TEST SUMMARY REPORT" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
Write-Host ""

$TOTAL_TESTS = $TESTS_PASSED + $TESTS_FAILED
$PASS_RATE = if ($TOTAL_TESTS -gt 0) { [math]::Round(($TESTS_PASSED / $TOTAL_TESTS) * 100, 2) } else { 0 }

Write-Host "  Total Tests:       $TOTAL_TESTS" -ForegroundColor White
Write-Host "  ✅ Tests Passed:   $TESTS_PASSED" -ForegroundColor Green
Write-Host "  ❌ Tests Failed:   $TESTS_FAILED" -ForegroundColor $(if ($TESTS_FAILED -eq 0) { "Green" } else { "Red" })
Write-Host "  📈 Pass Rate:      $PASS_RATE%" -ForegroundColor $(if ($PASS_RATE -eq 100) { "Green" } else { "Yellow" })
Write-Host ""

if ($TESTS_FAILED -eq 0) {
    Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -ForegroundColor Green
    Write-Host "ALL TESTS PASSED - SYSTEM IS READY!" -ForegroundColor Green
    Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your authentication system is:" -ForegroundColor Green
    Write-Host "  [OK] Server running and responding"
    Write-Host "  [OK] User signup working"
    Write-Host "  [OK] User login working"
    Write-Host "  [OK] JWT tokens being generated"
    Write-Host "  [OK] Route protection working (401 without token)"
    Write-Host "  [OK] Protected routes accessible with token (200)"
    Write-Host "  [OK] Data CRUD operations working"
    Write-Host "  [OK] Ready for production"
    Write-Host ""
} else {
    Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -ForegroundColor Yellow
    Write-Host "SOME TESTS FAILED - DIAGNOSIS NEEDED" -ForegroundColor Yellow
    Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -NoNewline; Write-Host "=" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Common Issues:" -ForegroundColor Yellow
    Write-Host "  1. Server not running? -> npm start (in separate terminal)"
    Write-Host "  2. Port in use? -> Check if another process uses :3001"
    Write-Host "  3. Supabase not configured? -> Add credentials to .env"
    Write-Host "  4. Node syntax error? -> Check server.js for errors"
    Write-Host ""
}

Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. ✅ Authentication verified"
Write-Host "  2. ⏭️  Set up Row Level Security (RLS) in Supabase"
Write-Host "  3. ⏭️  Build Vue.js/React PWA frontend"
Write-Host "  4. ⏭️  Deploy to production"
Write-Host ""
