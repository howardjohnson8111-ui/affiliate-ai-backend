const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const axios = require('axios');
const app = express();
const PORT = 3001;

// Security middleware
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
      fontSrc: ["'self'", "https://fonts.gstatic.com"],
      imgSrc: ["'self'", "data:", "https:"],
      scriptSrc: ["'self'"],
      connectSrc: ["'self'", "https://mxhvdwyuyxcmcrgljblc.supabase.co", "https://affiliate-ai-backend.onrender.com"],
      frameSrc: ["'none'"],
      objectSrc: ["'none'"],
    },
  },
}));

// CORS: allow only your frontend and Supabase
app.use(cors({
  origin: [
    'http://localhost:3000',
    'https://affiliate-ai-backend.onrender.com',
    'https://mxhvdwyuyxcmcrgljblc.supabase.co'
  ],
  credentials: true,
}));

app.use(express.json());

// ============ SUPABASE AUTHENTICATION SETUP ============
const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY;

let supabase = null;

// Initialize Supabase client if credentials are available
if (SUPABASE_URL && SUPABASE_ANON_KEY) {
  const { createClient } = require('@supabase/supabase-js');
  supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
  console.log('✅ [Supabase]: Initialized');
} else {
  console.log('⚠️  [Supabase]: Not configured. Set SUPABASE_URL and SUPABASE_ANON_KEY environment variables.');
}

// ============ AUTHENTICATION MIDDLEWARE ============
// Middleware to protect routes and get user ID from JWT
async function protect(req, res, next) {
  try {
    // Extract token from Authorization header
    let token;
    if (req.headers.authorization && req.headers.authorization.startsWith('Bearer ')) {
      token = req.headers.authorization.split(' ')[1];
    }

    if (!token) {
      return res.status(401).json({ error: '❌ Not authorized - no token provided' });
    }

    // If Supabase is not configured, skip authentication
    if (!supabase) {
      req.user = { id: 'demo-user', email: 'demo@example.com' }; // Demo mode
      return next();
    }

    // Verify token with Supabase
    const { data: { user }, error } = await supabase.auth.getUser(token);

    if (error || !user) {
      console.error('❌ [Auth Error]:', error ? error.message : 'User not found with token');
      return res.status(401).json({ error: '❌ Not authorized - invalid token' });
    }

    req.user = user; // Attach the user object to the request
    next(); // Continue to the next middleware/route handler
  } catch (err) {
    console.error('❌ [Auth Middleware Error]:', err.message);
    res.status(401).json({ error: '❌ Not authorized - token verification failed' });
  }
}

// ============ INPUT VALIDATION MIDDLEWARE ============
function validateCampaign(req, res, next) {
  const { name, platform } = req.body;
  
  if (!name || typeof name !== 'string' || name.trim().length === 0) {
    return res.status(400).json({ error: 'Name is required and must be a non-empty string' });
  }
  
  if (!platform || typeof platform !== 'string' || platform.trim().length === 0) {
    return res.status(400).json({ error: 'Platform is required and must be a non-empty string' });
  }
  
  // Validate platform enum
  const validPlatforms = ['instagram', 'facebook', 'tiktok', 'twitter', 'youtube', 'linkedin', 'pinterest'];
  if (!validPlatforms.includes(platform.toLowerCase())) {
    return res.status(400).json({ error: `Platform must be one of: ${validPlatforms.join(', ')}` });
  }
  
  // Validate optional fields
  if (req.body.affiliate_link && typeof req.body.affiliate_link !== 'string') {
    return res.status(400).json({ error: 'Affiliate link must be a string' });
  }
  
  if (req.body.clicks !== undefined && (typeof req.body.clicks !== 'number' || req.body.clicks < 0)) {
    return res.status(400).json({ error: 'Clicks must be a non-negative number' });
  }
  
  if (req.body.conversions !== undefined && (typeof req.body.conversions !== 'number' || req.body.conversions < 0)) {
    return res.status(400).json({ error: 'Conversions must be a non-negative number' });
  }
  
  if (req.body.earnings !== undefined && (typeof req.body.earnings !== 'number')) {
    return res.status(400).json({ error: 'Earnings must be a number' });
  }
  
  next();
}

function validateTransaction(req, res, next) {
  const { amount, type } = req.body;
  
  if (amount === undefined || typeof amount !== 'number' || amount <= 0) {
    return res.status(400).json({ error: 'Amount is required and must be a positive number' });
  }
  
  if (!type || typeof type !== 'string') {
    return res.status(400).json({ error: 'Type is required and must be a string' });
  }
  
  // Validate transaction type enum
  const validTypes = ['deposit', 'withdrawal', 'dividend', 'affiliate_payout', 'stock_purchase', 'stock_sale'];
  if (!validTypes.includes(type)) {
    return res.status(400).json({ error: `Type must be one of: ${validTypes.join(', ')}` });
  }
  
  // Validate optional payment method
  if (req.body.payment_method) {
    const validMethods = ['paypal', 'apple_pay', 'cash_app', 'chime', 'bank_transfer', 'crypto'];
    if (!validMethods.includes(req.body.payment_method)) {
      return res.status(400).json({ error: `Payment method must be one of: ${validMethods.join(', ')}` });
    }
  }
  
  // Validate optional status
  if (req.body.status) {
    const validStatuses = ['pending', 'completed', 'failed'];
    if (!validStatuses.includes(req.body.status)) {
      return res.status(400).json({ error: `Status must be one of: ${validStatuses.join(', ')}` });
    }
  }
  
  next();
}

function validatePayment(req, res, next) {
  const { amount, description } = req.body;
  
  if (amount === undefined || typeof amount !== 'number' || amount <= 0) {
    return res.status(400).json({ error: 'Amount is required and must be a positive number' });
  }
  
  if (!description || typeof description !== 'string' || description.trim().length === 0) {
    return res.status(400).json({ error: 'Description is required and must be a non-empty string' });
  }
  
  next();
}

// In-memory database (for testing)
let campaigns = {};
let transactions = {};

// ============ AUTHENTICATION ROUTES ============

// Sign up endpoint
app.post('/api/auth/signup', async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password are required' });
    }

    if (!supabase) {
      return res.status(503).json({ error: '❌ Supabase not configured' });
    }

    const { data, error } = await supabase.auth.signUp({
      email,
      password,
    });

    if (error) {
      console.error('❌ [Auth Error]:', error.message);
      return res.status(400).json({ error: error.message });
    }

    console.log('🚪 [Auth]: User signed up -', email);
    res.status(201).json({
      message: 'User registered successfully',
      user: { id: data.user?.id, email: data.user?.email },
    });
  } catch (err) {
    console.error('❌ [Auth Error]:', err.message);
    res.status(500).json({ error: '❌ Signup failed' });
  }
});

// Login endpoint
app.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password are required' });
    }

    if (!supabase) {
      return res.status(503).json({ error: '❌ Supabase not configured' });
    }

    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {
      console.error('❌ [Auth Error]:', error.message);
      return res.status(401).json({ error: error.message });
    }

    console.log('🚪 [Auth]: User logged in -', email);
    res.status(200).json({
      message: 'Login successful',
      user: { id: data.user?.id, email: data.user?.email },
      token: data.session?.access_token,
    });
  } catch (err) {
    console.error('❌ [Auth Error]:', err.message);
    res.status(500).json({ error: '❌ Login failed' });
  }
});

// Logout endpoint (protected)
app.post('/api/auth/logout', protect, async (req, res) => {
  try {
    if (!supabase) {
      return res.status(200).json({ message: 'Logged out (demo mode)' });
    }

    const { error } = await supabase.auth.signOut();

    if (error) {
      console.error('❌ [Auth Error]:', error.message);
      return res.status(400).json({ error: error.message });
    }

    console.log('🚪 [Auth]: User logged out -', req.user.email);
    res.status(200).json({ message: 'Logged out successfully' });
  } catch (err) {
    console.error('❌ [Auth Error]:', err.message);
    res.status(500).json({ error: '❌ Logout failed' });
  }
});

// ============ CAMPAIGN ENDPOINTS ============

// POST /api/campaigns - Create a new campaign
app.post('/api/campaigns', protect, validateCampaign, (req, res) => {
  try {
    const { name, platform, affiliate_link, clicks, content, conversions, earnings, image_url, scheduled_date, status, tags } = req.body;
    
    // Validate required fields
    if (!name || !platform) {
      return res.status(400).json({ error: 'Name and platform are required' });
    }

    // Generate a simple ID
    const id = Date.now().toString();
    
    const campaign = {
      id,
      name,
      platform,
      affiliate_link: affiliate_link || null,
      clicks: clicks || 0,
      content: content || null,
      conversions: conversions || 0,
      earnings: earnings || 0,
      image_url: image_url || null,
      scheduled_date: scheduled_date || null,
      status: status || 'draft',
      tags: tags || [],
      created_at: new Date().toISOString()
    };

    campaigns[id] = campaign;
    console.log(`[Server]: Campaign created with ID: ${id}`);
    res.status(201).json(campaign);
  } catch (error) {
    console.error('[Server]: Error creating campaign:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/campaigns/:id - Read a campaign by ID
app.get('/api/campaigns/:id', protect, (req, res) => {
  try {
    const { id } = req.params;
    const campaign = campaigns[id];

    if (!campaign) {
      return res.status(404).json({ error: 'Campaign not found' });
    }

    console.log(`[Server]: Campaign retrieved with ID: ${id}`);
    res.status(200).json(campaign);
  } catch (error) {
    console.error('[Server]: Error reading campaign:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// PUT /api/campaigns/:id - Update a campaign by ID
app.put('/api/campaigns/:id', protect, (req, res) => {
  try {
    const { id } = req.params;
    const campaign = campaigns[id];

    if (!campaign) {
      return res.status(404).json({ error: 'Campaign not found' });
    }

    // Update fields
    Object.assign(campaign, req.body);
    campaign.updated_at = new Date().toISOString();

    console.log(`[Server]: Campaign updated with ID: ${id}`);
    res.status(200).json(campaign);
  } catch (error) {
    console.error('[Server]: Error updating campaign:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// DELETE /api/campaigns/:id - Delete a campaign by ID
app.delete('/api/campaigns/:id', protect, (req, res) => {
  try {
    const { id } = req.params;
    const campaign = campaigns[id];

    if (!campaign) {
      return res.status(404).json({ error: 'Campaign not found' });
    }

    delete campaigns[id];
    console.log(`[Server]: Campaign deleted with ID: ${id}`);
    res.status(200).json({ message: 'Campaign deleted successfully', id });
  } catch (error) {
    console.error('[Server]: Error deleting campaign:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/campaigns - Get all campaigns
app.get('/api/campaigns', protect, (req, res) => {
  try {
    console.log('[Server]: All campaigns retrieved');
    res.status(200).json(Object.values(campaigns));
  } catch (error) {
    console.error('[Server]: Error retrieving campaigns:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============ TRANSACTION ENDPOINTS ============

// POST /api/transactions - Create a new transaction
app.post('/api/transactions', protect, validateTransaction, async (req, res) => {
  try {
    console.log('💰 [POST] /api/transactions - Adding new record:', req.body);
    const { amount, type, description, payment_method, status } = req.body;
    
    // Validate required fields
    if (!amount || !type) {
      return res.status(400).json({ error: 'Amount and type are required' });
    }

    // Generate a simple ID
    const id = Date.now().toString();
    
    const transaction = {
      id,
      amount,
      type,
      description: description || null,
      payment_method: payment_method || null,
      status: status || 'pending',
      created_at: new Date().toISOString()
    };

    transactions[id] = transaction;
    console.log(`[Server]: Transaction created with ID: ${id}`);
    res.status(201).json(transaction);
  } catch (error) {
    console.error('[Server]: Error creating transaction:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/transactions - Get all transactions
app.get('/api/transactions', protect, async (req, res) => {
  try {
    const allTransactions = Object.values(transactions).sort((a, b) => 
      new Date(b.created_at) - new Date(a.created_at)
    );
    console.log('[Server]: All transactions retrieved');
    res.status(200).json(allTransactions);
  } catch (error) {
    console.error('[Server]: Error retrieving transactions:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============ PAYPAL PAYMENT ENDPOINTS ============
const PAYPAL_EMAIL = process.env.PAYPAL_EMAIL;
const PAYPAL_CLIENT_ID = process.env.PAYPAL_CLIENT_ID;
const PAYPAL_SECRET = process.env.PAYPAL_SECRET;

// Store payment records
const payments = {};

// POST /api/payments - Create a payment record
app.post('/api/payments', protect, validatePayment, async (req, res) => {
  try {
    const { amount, description, orderId } = req.body;

    if (!amount || !description) {
      return res.status(400).json({ error: 'Amount and description required' });
    }

    const paymentId = `PAY_${Date.now()}`;
    const payment = {
      id: paymentId,
      userId: req.user.id,
      amount: parseFloat(amount),
      description: description,
      orderId: orderId || null,
      status: 'pending',
      paypalEmail: PAYPAL_EMAIL,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };

    payments[paymentId] = payment;
    
    console.log(`[PayPal]: Payment created - ${paymentId}`);
    res.status(201).json(payment);
  } catch (error) {
    console.error('[PayPal]: Error creating payment:', error);
    res.status(500).json({ error: 'Failed to create payment' });
  }
});

// GET /api/payments - Get all payments for user
app.get('/api/payments', protect, async (req, res) => {
  try {
    const userPayments = Object.values(payments)
      .filter(p => p.userId === req.user.id)
      .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    
    console.log(`[PayPal]: Retrieved ${userPayments.length} payments for user ${req.user.id}`);
    res.status(200).json(userPayments);
  } catch (error) {
    console.error('[PayPal]: Error retrieving payments:', error);
    res.status(500).json({ error: 'Failed to retrieve payments' });
  }
});

// GET /api/payments/:id - Get payment details
app.get('/api/payments/:id', protect, async (req, res) => {
  try {
    const payment = payments[req.params.id];

    if (!payment) {
      return res.status(404).json({ error: 'Payment not found' });
    }

    if (payment.userId !== req.user.id) {
      return res.status(403).json({ error: 'Not authorized to view this payment' });
    }

    console.log(`[PayPal]: Payment retrieved - ${req.params.id}`);
    res.status(200).json(payment);
  } catch (error) {
    console.error('[PayPal]: Error retrieving payment:', error);
    res.status(500).json({ error: 'Failed to retrieve payment' });
  }
});

// PUT /api/payments/:id - Update payment status
app.put('/api/payments/:id', protect, async (req, res) => {
  try {
    const { status } = req.body;
    const payment = payments[req.params.id];

    if (!payment) {
      return res.status(404).json({ error: 'Payment not found' });
    }

    if (payment.userId !== req.user.id) {
      return res.status(403).json({ error: 'Not authorized to update this payment' });
    }

    payment.status = status || payment.status;
    payment.updated_at = new Date().toISOString();

    console.log(`[PayPal]: Payment updated - ${req.params.id} (status: ${payment.status})`);
    res.status(200).json(payment);
  } catch (error) {
    console.error('[PayPal]: Error updating payment:', error);
    res.status(500).json({ error: 'Failed to update payment' });
  }
});

// POST /api/payments/:id/verify - Verify PayPal payment
app.post('/api/payments/:id/verify', protect, async (req, res) => {
  try {
    const { transactionId } = req.body;
    const payment = payments[req.params.id];

    if (!payment) {
      return res.status(404).json({ error: 'Payment not found' });
    }

    if (payment.userId !== req.user.id) {
      return res.status(403).json({ error: 'Not authorized to verify this payment' });
    }

    // In production: Verify with PayPal API
    // For now: Mark as verified
    payment.status = 'completed';
    payment.transactionId = transactionId;
    payment.verified_at = new Date().toISOString();
    payment.updated_at = new Date().toISOString();

    console.log(`[PayPal]: Payment verified - ${req.params.id}`);
    res.status(200).json(payment);
  } catch (error) {
    console.error('[PayPal]: Error verifying payment:', error);
    res.status(500).json({ error: 'Failed to verify payment' });
  }
});

// ============ EXTERNAL STOCK DATA INTEGRATION ============


// DELETE /api/payments/:id - Cancel payment
app.delete('/api/payments/:id', protect, async (req, res) => {
  try {
    const payment = payments[req.params.id];

    if (!payment) {
      return res.status(404).json({ error: 'Payment not found' });
    }

    if (payment.userId !== req.user.id) {
      return res.status(403).json({ error: 'Not authorized to delete this payment' });
    }

    payment.status = 'cancelled';
    payment.updated_at = new Date().toISOString();

    console.log(`[PayPal]: Payment cancelled - ${req.params.id}`);
    res.status(200).json({ message: 'Payment cancelled', payment });
  } catch (error) {
    console.error('[PayPal]: Error cancelling payment:', error);
    res.status(500).json({ error: 'Failed to cancel payment' });
  }
});

// POST /api/paypal-config - Get PayPal email for frontend
app.get('/api/paypal-config', (req, res) => {
  res.status(200).json({
    paypalEmail: PAYPAL_EMAIL,
    clientId: PAYPAL_CLIENT_ID ? 'configured' : 'not-configured'
  });
});

// ============ ROOT ROUTE ============
app.get('/', (req, res) => {
  res.status(200).json({ 
    message: 'Affiliate AI Pro Backend API',
    status: 'running',
    version: '1.0.0',
    endpoints: {
      health: '/api/health',
      campaigns: '/api/campaigns',
      transactions: '/api/transactions',
      payments: '/api/payments',
      auth: '/api/auth'
    }
  });
});

// ============ HEALTH CHECK ============
app.get('/api/health', (req, res) => {
  res.status(200).json({ message: 'Backend is running!' });
});

// ============ EXTERNAL STOCK DATA ENDPOINTS ============
const STOCK_API_KEY = process.env.STOCK_API_KEY;
const STOCK_API_BASE_URL = process.env.STOCK_API_BASE_URL;
const STOCK_API_PROVIDER = process.env.STOCK_API_PROVIDER || 'alphavantage';

// In-memory subscriptions for notifications/calendar integration (demo)
const stockSubscriptions = {};

// Middleware to check for STOCK_API_KEY
function checkStockApiKey(req, res, next) {
  if (!STOCK_API_KEY || !STOCK_API_BASE_URL) {
    console.error('❌ Stock API Key or Base URL not set in .env');
    return res.status(500).json({ error: 'External Stock API credentials not configured.' });
  }
  next();
}

// Get live stock quote for a symbol
app.get('/api/external-stocks/quote/:symbol', protect, checkStockApiKey, async (req, res) => {
  const { symbol } = req.params;
  console.log(`📈 [GET] /api/external-stocks/quote/${symbol} - Fetching live quote.`);
  try {
    if (STOCK_API_PROVIDER === 'alphavantage') {
      const response = await axios.get(STOCK_API_BASE_URL, {
        params: {
          function: 'GLOBAL_QUOTE',
          symbol: symbol,
          apikey: STOCK_API_KEY
        }
      });
      if (response.data && response.data['Error Message']) {
        return res.status(400).json({ error: response.data['Error Message'] });
      }
      if (response.data && !response.data['Global Quote']) {
        return res.status(404).json({ error: `No quote found for symbol ${symbol}.` });
      }
      res.json(response.data['Global Quote']);
    } else if (STOCK_API_PROVIDER === 'finnhub') {
      const response = await axios.get(`${STOCK_API_BASE_URL}/quote`, {
        params: { symbol: symbol, token: STOCK_API_KEY }
      });
      res.json(response.data);
    } else {
      res.status(400).json({ error: `Unknown provider: ${STOCK_API_PROVIDER}` });
    }
  } catch (error) {
    console.error('❌ Error fetching stock quote:', error.message);
    res.status(500).json({ error: `Failed to fetch quote: ${error.message}` });
  }
});

// Get recent dividend history for a symbol
app.get('/api/external-stocks/dividends/:symbol', protect, checkStockApiKey, async (req, res) => {
  const { symbol } = req.params;
  console.log(`📅 [GET] /api/external-stocks/dividends/${symbol} - Fetching dividend history.`);
  try {
    const response = await axios.get(STOCK_API_BASE_URL, {
      params: {
        function: 'TIME_SERIES_DAILY_ADJUSTED',
        symbol: symbol,
        apikey: STOCK_API_KEY
      }
    });

    const data = response.data || {};
    const series = data['Time Series (Daily)'] || {};

    // Extract recent dividend events
    const dividends = [];
    for (const [date, dayData] of Object.entries(series)) {
      const div = parseFloat(dayData['7. dividend amount'] || 0);
      if (div > 0) {
        dividends.push({ date, dividend: div });
      }
      if (dividends.length >= 30) break; // limit
    }

    return res.status(200).json({ symbol, dividends });
  } catch (error) {
    console.error('[External Stock]: Error fetching dividends:', error.message);
    return res.status(500).json({ error: 'Failed to fetch dividend history', details: error.message });
  }
});

// Return a curated list of penny stocks (demo/static)
app.get('/api/external-stocks/penny-list', protect, async (req, res) => {
  console.log('📃 [GET] /api/external-stocks/penny-list - Returning demo penny stock list.');
  const demoPennyStocks = [
    { symbol: 'ABCD', name: 'ACME BioTech', price: 0.42, exchange: 'OTC' },
    { symbol: 'WXYZ', name: 'WinZoom Inc', price: 0.85, exchange: 'OTC' },
    { symbol: 'PENN', name: 'PennyPlay Ltd', price: 0.33, exchange: 'OTC' }
  ];
  res.status(200).json({ source: 'demo', data: demoPennyStocks });
});

// Get penny stocks (mock data)
app.get('/api/external-stocks/penny-stocks', protect, async (req, res) => {
  console.log('🪙 [GET] /api/external-stocks/penny-stocks');
  res.json({
    penny_stocks: [
      { symbol: 'SNDL', name: 'Sundial Growers Inc.', price: 1.42, change: -2.8 },
      { symbol: 'PROG', name: 'Progenity, Inc.', price: 0.68, change: 5.2 },
      { symbol: 'BBIG', name: 'Vinco Ventures, Inc.', price: 0.12, change: -8.1 }
    ]
  });
});

// Subscribe to price/dividend notifications or calendar updates (demo)
app.post('/api/external-stocks/subscribe', protect, (req, res) => {
  try {
    const userId = req.user.id || 'demo-user';
    const { symbol, frequency = 'daily', callbackUrl, calendar = null } = req.body;
    if (!symbol) return res.status(400).json({ error: 'symbol is required' });

    const id = `${userId}::${symbol}::${Date.now()}`;
    const sub = { id, userId, symbol, frequency, callbackUrl: callbackUrl || null, calendar: calendar || null, created_at: new Date().toISOString() };
    stockSubscriptions[id] = sub;

    console.log(`[Subscriptions]: New subscription ${id} for ${symbol}`);
    return res.status(201).json(sub);
  } catch (error) {
    console.error('[Subscriptions]: Error creating subscription:', error.message);
    return res.status(500).json({ error: 'Failed to create subscription', details: error.message });
  }
});

// List user's subscriptions
app.get('/api/external-stocks/subscriptions', protect, (req, res) => {
  const userId = req.user.id || 'demo-user';
  const subs = Object.values(stockSubscriptions).filter(s => s.userId === userId);
  res.status(200).json(subs);
});

// Trigger a test notification for a subscription (demo)
app.post('/api/external-stocks/subscriptions/:id/notify', protect, (req, res) => {
  const sub = stockSubscriptions[req.params.id];
  if (!sub) return res.status(404).json({ error: 'Subscription not found' });

  // In production: call callbackUrl, create calendar event, or send push notification
  console.log(`[Notifications]: Trigger test notification for ${sub.id} (symbol: ${sub.symbol})`);
  return res.status(200).json({ message: 'Notification triggered (demo)', subscription: sub });
});

// Start the server
app.listen(PORT, () => {
  console.log(`\n✅ [Server]: Affiliate AI Backend is running on http://localhost:${PORT}`);
  console.log(`📡 API Base URL: http://localhost:${PORT}/api`);
  console.log('\nAvailable endpoints:');
  console.log('  POST   /api/campaigns       - Create a campaign');
  console.log('  GET    /api/campaigns       - Get all campaigns');
  console.log('  GET    /api/campaigns/:id   - Get a campaign by ID');
  console.log('  PUT    /api/campaigns/:id   - Update a campaign');
  console.log('  DELETE /api/campaigns/:id   - Delete a campaign');
  console.log('  POST   /api/transactions    - Create a transaction');
  console.log('  GET    /api/transactions    - Get all transactions');
  console.log('  POST   /api/payments        - Create a payment');
  console.log('  GET    /api/payments        - Get all payments');
  console.log('  GET    /api/payments/:id    - Get payment details');
  console.log('  PUT    /api/payments/:id    - Update payment status');
  console.log('  POST   /api/payments/:id/verify - Verify PayPal payment');
  console.log('  DELETE /api/payments/:id    - Cancel payment');
  console.log('  GET    /api/paypal-config   - Get PayPal config');
  console.log('  GET    /api/health          - Health check\n');
});
