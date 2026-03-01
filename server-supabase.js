/**
 * Affiliate AI Pro - Node.js Backend Server (Updated with Supabase)
 * Features: Campaign management, Transaction logging, User authentication
 */

const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const { authMiddleware } = require('./lib/auth');
const {
  CampaignService,
  TransactionService,
  StockService,
  LearningService,
  PreferencesService,
} = require('./lib/supabase-db');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// ============================================================================
// HEALTH CHECK ENDPOINT
// ============================================================================
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    message: 'Affiliate AI Backend is running',
    timestamp: new Date(),
  });
});

// ============================================================================
// CAMPAIGN ENDPOINTS (Authenticated)
// ============================================================================

// Create campaign
app.post('/api/campaigns', authMiddleware, async (req, res) => {
  try {
    const campaign = await CampaignService.createCampaign(req.userId, req.body);
    res.status(201).json({
      success: true,
      campaign,
      message: 'Campaign created successfully'
    });
  } catch (error) {
    console.error('Error creating campaign:', error);
    res.status(500).json({
      error: error.message,
      success: false
    });
  }
});

// Get all campaigns for user
app.get('/api/campaigns', authMiddleware, async (req, res) => {
  try {
    const campaigns = await CampaignService.getAllCampaigns(req.userId);
    res.json({
      success: true,
      campaigns,
      count: campaigns.length
    });
  } catch (error) {
    console.error('Error fetching campaigns:', error);
    res.status(500).json({
      error: error.message,
      success: false
    });
  }
});

// Get specific campaign
app.get('/api/campaigns/:id', authMiddleware, async (req, res) => {
  try {
    const campaign = await CampaignService.getCampaign(req.userId, req.params.id);
    if (!campaign) {
      return res.status(404).json({
        error: 'Campaign not found',
        success: false
      });
    }
    res.json({
      success: true,
      campaign
    });
  } catch (error) {
    console.error('Error fetching campaign:', error);
    res.status(500).json({
      error: error.message,
      success: false
    });
  }
});

// Update campaign
app.put('/api/campaigns/:id', authMiddleware, async (req, res) => {
  try {
    const campaign = await CampaignService.updateCampaign(req.userId, req.params.id, req.body);
    res.json({
      success: true,
      campaign,
      message: 'Campaign updated successfully'
    });
  } catch (error) {
    console.error('Error updating campaign:', error);
    res.status(500).json({
      error: error.message,
      success: false
    });
  }
});

// Delete campaign
app.delete('/api/campaigns/:id', authMiddleware, async (req, res) => {
  try {
    await CampaignService.deleteCampaign(req.userId, req.params.id);
    res.json({
      success: true,
      message: 'Campaign deleted successfully'
    });
  } catch (error) {
    console.error('Error deleting campaign:', error);
    res.status(500).json({
      error: error.message,
      success: false
    });
  }
});

// ============================================================================
// TRANSACTION ENDPOINTS (Authenticated)
// ============================================================================

// Create transaction
app.post('/api/transactions', authMiddleware, async (req, res) => {
  try {
    const transaction = await TransactionService.createTransaction(req.userId, req.body);
    res.status(201).json({
      success: true,
      transaction,
      message: 'Transaction logged successfully'
    });
  } catch (error) {
    console.error('Error creating transaction:', error);
    res.status(500).json({
      error: error.message,
      success: false
    });
  }
});

// Get all transactions
app.get('/api/transactions', authMiddleware, async (req, res) => {
  try {
    const transactions = await TransactionService.getAllTransactions(req.userId);
    res.json({
      success: true,
      transactions,
      count: transactions.length
    });
  } catch (error) {
    console.error('Error fetching transactions:', error);
    res.status(500).json({
      error: error.message,
      success: false
    });
  }
});

// Get transaction summary
app.get('/api/transactions/summary', authMiddleware, async (req, res) => {
  try {
    const summary = await TransactionService.getTransactionsSummary(req.userId);
    res.json({
      success: true,
      summary
    });
  } catch (error) {
    console.error('Error fetching summary:', error);
    res.status(500).json({
      error: error.message,
      success: false
    });
  }
});

// ============================================================================
// STOCK ENDPOINTS (Authenticated)
// ============================================================================

// Create stock
app.post('/api/stocks', authMiddleware, async (req, res) => {
  try {
    const stock = await StockService.createStock(req.userId, req.body);
    res.status(201).json({
      success: true,
      stock,
      message: 'Stock record created'
    });
  } catch (error) {
    console.error('Error creating stock:', error);
    res.status(500).json({
      error: error.message,
      success: false
    });
  }
});

// Get all stocks
app.get('/api/stocks', authMiddleware, async (req, res) => {
  try {
    const stocks = await StockService.getAllStocks(req.userId);
    res.json({
      success: true,
      stocks,
      count: stocks.length
    });
  } catch (error) {
    console.error('Error fetching stocks:', error);
    res.status(500).json({
      error: error.message,
      success: false
    });
  }
});

// Update stock
app.put('/api/stocks/:id', authMiddleware, async (req, res) => {
  try {
    const stock = await StockService.updateStock(req.userId, req.params.id, req.body);
    res.json({
      success: true,
      stock,
      message: 'Stock updated'
    });
  } catch (error) {
    console.error('Error updating stock:', error);
    res.status(500).json({
      error: error.message,
      success: false
    });
  }
});

// Delete stock
app.delete('/api/stocks/:id', authMiddleware, async (req, res) => {
  try {
    await StockService.deleteStock(req.userId, req.params.id);
    res.json({
      success: true,
      message: 'Stock deleted'
    });
  } catch (error) {
    console.error('Error deleting stock:', error);
    res.status(500).json({
      error: error.message,
      success: false
    });
  }
});

// ============================================================================
// LEARNING MODULE ENDPOINTS (Authenticated)
// ============================================================================

// Create learning module
app.post('/api/learning', authMiddleware, async (req, res) => {
  try {
    const module = await LearningService.createModule(req.userId, req.body);
    res.status(201).json({
      success: true,
      module,
      message: 'Learning module created'
    });
  } catch (error) {
    console.error('Error creating module:', error);
    res.status(500).json({
      error: error.message,
      success: false
    });
  }
});

// Get all learning modules
app.get('/api/learning', authMiddleware, async (req, res) => {
  try {
    const modules = await LearningService.getAllModules(req.userId);
    res.json({
      success: true,
      modules,
      count: modules.length
    });
  } catch (error) {
    console.error('Error fetching modules:', error);
    res.status(500).json({
      error: error.message,
      success: false
    });
  }
});

// Update learning module
app.put('/api/learning/:id', authMiddleware, async (req, res) => {
  try {
    const module = await LearningService.updateModule(req.userId, req.params.id, req.body);
    res.json({
      success: true,
      module,
      message: 'Module updated'
    });
  } catch (error) {
    console.error('Error updating module:', error);
    res.status(500).json({
      error: error.message,
      success: false
    });
  }
});

// Delete learning module
app.delete('/api/learning/:id', authMiddleware, async (req, res) => {
  try {
    await LearningService.deleteModule(req.userId, req.params.id);
    res.json({
      success: true,
      message: 'Module deleted'
    });
  } catch (error) {
    console.error('Error deleting module:', error);
    res.status(500).json({
      error: error.message,
      success: false
    });
  }
});

// ============================================================================
// USER PREFERENCES ENDPOINTS (Authenticated)
// ============================================================================

// Get preferences
app.get('/api/preferences', authMiddleware, async (req, res) => {
  try {
    const preferences = await PreferencesService.getPreferences(req.userId);
    res.json({
      success: true,
      preferences
    });
  } catch (error) {
    console.error('Error fetching preferences:', error);
    res.status(500).json({
      error: error.message,
      success: false
    });
  }
});

// Update preferences
app.put('/api/preferences', authMiddleware, async (req, res) => {
  try {
    const preferences = await PreferencesService.updatePreferences(req.userId, req.body);
    res.json({
      success: true,
      preferences,
      message: 'Preferences updated'
    });
  } catch (error) {
    console.error('Error updating preferences:', error);
    res.status(500).json({
      error: error.message,
      success: false
    });
  }
});

// ============================================================================
// ERROR HANDLING
// ============================================================================

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Endpoint not found',
    path: req.path,
    method: req.method
  });
});

// Error handler
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({
    error: 'Internal server error',
    message: err.message
  });
});

// ============================================================================
// SERVER STARTUP
// ============================================================================

app.listen(PORT, () => {
  console.log(`\n${'='.repeat(70)}`);
  console.log('✅ [Server]: Affiliate AI Backend is running');
  console.log(`📡 API Base URL: http://localhost:${PORT}/api`);
  console.log(`🔐 Authentication: Enabled (JWT)`);
  console.log(`💾 Database: Supabase`);
  console.log(`${'='.repeat(70)}\n`);
  
  console.log('Available endpoints:');
  console.log('  Campaigns:    POST/GET/PUT/DELETE /api/campaigns');
  console.log('  Transactions: POST/GET             /api/transactions');
  console.log('  Stocks:       POST/GET/PUT/DELETE /api/stocks');
  console.log('  Learning:     POST/GET/PUT/DELETE /api/learning');
  console.log('  Preferences:  GET/PUT              /api/preferences');
  console.log('  Health:       GET                  /api/health\n');
});

module.exports = app;
