# 💳 PayPal Integration Guide

Your backend now has complete PayPal payment functionality!

---

## 🔧 Configuration

### 1. Add Your PayPal Credentials to `.env`

Open `.env` file and update:

```env
PAYPAL_EMAIL=phanor0811@outlook.com
PAYPAL_CLIENT_ID=your_paypal_client_id_here
PAYPAL_SECRET=your_paypal_secret_here
```

### 2. Get PayPal Credentials

Visit: [developer.paypal.com](https://developer.paypal.com)
1. Create Business Account
2. Go to Dashboard → Apps & Credentials
3. Copy your Client ID and Secret
4. Paste in `.env` file

### 3. Restart Backend

```powershell
npm start
```

---

## 📡 Available Payment Endpoints

All payment endpoints require JWT authentication (Bearer token)

### Create Payment
```http
POST /api/payments
Content-Type: application/json
Authorization: Bearer YOUR_JWT_TOKEN

{
  "amount": 99.99,
  "description": "Premium Package",
  "orderId": "ORDER_123"
}
```

**Response:**
```json
{
  "id": "PAY_1704067200000",
  "userId": "user_123",
  "amount": 99.99,
  "description": "Premium Package",
  "status": "pending",
  "paypalEmail": "phanor0811@outlook.com",
  "created_at": "2026-01-27T12:00:00.000Z"
}
```

---

### Get All Payments
```http
GET /api/payments
Authorization: Bearer YOUR_JWT_TOKEN
```

**Response:**
```json
[
  {
    "id": "PAY_1704067200000",
    "amount": 99.99,
    "status": "pending",
    "created_at": "2026-01-27T12:00:00.000Z"
  }
]
```

---

### Get Payment Details
```http
GET /api/payments/PAY_1704067200000
Authorization: Bearer YOUR_JWT_TOKEN
```

**Response:** Complete payment object

---

### Update Payment Status
```http
PUT /api/payments/PAY_1704067200000
Content-Type: application/json
Authorization: Bearer YOUR_JWT_TOKEN

{
  "status": "completed"
}
```

**Valid Statuses:**
- `pending` - Payment created, waiting for user action
- `processing` - Payment being processed
- `completed` - Payment successful
- `failed` - Payment failed
- `cancelled` - Payment cancelled

---

### Verify PayPal Payment
```http
POST /api/payments/PAY_1704067200000/verify
Content-Type: application/json
Authorization: Bearer YOUR_JWT_TOKEN

{
  "transactionId": "PAYPAL_TRANSACTION_ID"
}
```

**Response:**
```json
{
  "id": "PAY_1704067200000",
  "status": "completed",
  "transactionId": "PAYPAL_TRANSACTION_ID",
  "verified_at": "2026-01-27T12:05:00.000Z"
}
```

---

### Cancel Payment
```http
DELETE /api/payments/PAY_1704067200000
Authorization: Bearer YOUR_JWT_TOKEN
```

**Response:**
```json
{
  "message": "Payment cancelled",
  "payment": {
    "id": "PAY_1704067200000",
    "status": "cancelled"
  }
}
```

---

### Get PayPal Configuration
```http
GET /api/paypal-config
```

**Response:**
```json
{
  "paypalEmail": "phanor0811@outlook.com",
  "clientId": "configured"
}
```

---

## 💻 Frontend Integration Example

### In Vue.js Component:

```javascript
// 1. Create payment
async createPayment(amount, description) {
  const token = localStorage.getItem('authToken');
  
  const response = await fetch('http://localhost:3001/api/payments', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      amount: amount,
      description: description
    })
  });

  return response.json();
}

// 2. Get all payments
async getPayments() {
  const token = localStorage.getItem('authToken');
  
  const response = await fetch('http://localhost:3001/api/payments', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  return response.json();
}

// 3. Verify payment after PayPal redirect
async verifyPayment(paymentId, transactionId) {
  const token = localStorage.getItem('authToken');
  
  const response = await fetch(
    `http://localhost:3001/api/payments/${paymentId}/verify`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        transactionId: transactionId
      })
    }
  );

  return response.json();
}
```

---

## 🔄 Payment Flow

### Normal Flow:
```
1. User clicks "Pay with PayPal"
   ↓
2. Frontend calls POST /api/payments
   ↓
3. Backend creates payment record with status: "pending"
   ↓
4. Frontend redirects to PayPal
   ↓
5. User completes payment on PayPal
   ↓
6. PayPal redirects back to your app
   ↓
7. Frontend calls POST /api/payments/:id/verify
   ↓
8. Backend verifies and updates status: "completed"
   ↓
9. Frontend shows success message
```

---

## 📊 Payment Data Structure

```javascript
{
  "id": "PAY_1704067200000",           // Unique payment ID
  "userId": "user_123",                 // Who made payment
  "amount": 99.99,                      // Payment amount
  "description": "Premium Package",     // What they're paying for
  "orderId": "ORDER_123",               // Optional order reference
  "status": "pending",                  // Current status
  "paypalEmail": "phanor0811@outlook.com",  // Your PayPal email
  "transactionId": "PAYPAL_TXN_ID",    // PayPal transaction ID (after verify)
  "created_at": "2026-01-27...",       // When created
  "updated_at": "2026-01-27...",       // Last update
  "verified_at": "2026-01-27..."       // When verified
}
```

---

## 🧪 Test Locally (Without Real PayPal)

### Create test payment:
```powershell
# 1. Login to get token
$body = @{
  email = "test@example.com"
  password = "password123"
} | ConvertTo-Json

$login = Invoke-RestMethod -Uri "http://localhost:3001/login" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body

$token = $login.token

# 2. Create payment
$paymentBody = @{
  amount = 99.99
  description = "Test Payment"
} | ConvertTo-Json

$payment = Invoke-RestMethod -Uri "http://localhost:3001/api/payments" `
  -Method POST `
  -ContentType "application/json" `
  -Headers @{ "Authorization" = "Bearer $token" } `
  -Body $paymentBody

$paymentId = $payment.id
Write-Host "Created payment: $paymentId"

# 3. Get payments
Invoke-RestMethod -Uri "http://localhost:3001/api/payments" `
  -Headers @{ "Authorization" = "Bearer $token" }

# 4. Verify payment
$verifyBody = @{
  transactionId = "TEST_TXN_123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:3001/api/payments/$paymentId/verify" `
  -Method POST `
  -ContentType "application/json" `
  -Headers @{ "Authorization" = "Bearer $token" } `
  -Body $verifyBody
```

---

## ✅ What's Included

- ✅ Create payments
- ✅ List user payments
- ✅ Get payment details
- ✅ Update payment status
- ✅ Verify payments
- ✅ Cancel payments
- ✅ Get PayPal config

---

## 🔒 Security Features

- ✅ JWT authentication required (no anonymous payments)
- ✅ Users can only see their own payments
- ✅ Sensitive credentials in `.env` file (not in code)
- ✅ Status validation
- ✅ Error handling

---

## 📝 Next Steps

1. **Get PayPal Credentials**
   - Visit developer.paypal.com
   - Create app
   - Get Client ID and Secret

2. **Update .env File**
   - Add your credentials
   - Restart backend

3. **Build Payment UI**
   - Create payment button in Vue.js
   - Integrate PayPal SDK
   - Handle redirects

4. **Test Payment Flow**
   - Use test credentials
   - Test payment creation
   - Test verification

5. **Deploy to Production**
   - Switch to live PayPal credentials
   - Test full flow
   - Monitor payments

---

## 🚀 Production Setup

### Before deploying:
1. Update `.env` with LIVE PayPal credentials
2. Test with real PayPal sandbox account
3. Set up proper error logging
4. Configure PayPal IPN (Instant Payment Notifications)
5. Add payment webhooks to process async events

### Environment Variables Needed:
```
PAYPAL_EMAIL=your-business-email@paypal.com
PAYPAL_CLIENT_ID=your_live_client_id
PAYPAL_SECRET=your_live_secret
```

---

## 📚 PayPal Resources

- **Developer Dashboard:** https://developer.paypal.com
- **API Documentation:** https://developer.paypal.com/docs/
- **REST API Reference:** https://developer.paypal.com/api/rest/
- **SDK Integration:** https://developer.paypal.com/sdk/js/

---

## 💡 Tips

- **Test Mode:** Use sandbox credentials for testing
- **Live Mode:** Switch credentials when going live
- **Webhooks:** Set up PayPal webhooks for async payments
- **Error Handling:** Always validate payment status
- **Logging:** Monitor payment logs for issues

---

**Your PayPal integration is ready!** 🎉

Start by adding your PayPal credentials to `.env` and testing with the examples above.
