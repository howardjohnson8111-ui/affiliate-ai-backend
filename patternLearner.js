const logger = require('./logger');
const { log } = require('./auditLog');

// In-memory store for demo; in production use Supabase
const userPatterns = {};

function recordAction(userId, action, details = {}) {
  if (!userPatterns[userId]) {
    userPatterns[userId] = {
      loginTimes: [],
      campaignFrequency: {},
      payoutMethods: [],
      preferredPlatforms: [],
      lastActions: []
    };
  }
  const p = userPatterns[userId];
  const now = new Date();
  p.lastActions.push({ action, details, timestamp: now });
  if (p.lastActions.length > 100) p.lastActions.shift(); // keep recent 100

  // Learn login patterns
  if (action === 'login') {
    p.loginTimes.push(now);
    if (p.loginTimes.length > 30) p.loginTimes.shift(); // keep 30 logins
  }

  // Learn campaign frequency
  if (action === 'create_campaign') {
    const platform = details.platform;
    p.campaignFrequency[platform] = (p.campaignFrequency[platform] || 0) + 1;
    if (!p.preferredPlatforms.includes(platform)) {
      p.preferredPlatforms.push(platform);
    }
  }

  // Learn payout methods
  if (action === 'payout') {
    const method = details.method;
    if (!p.payoutMethods.includes(method)) {
      p.payoutMethods.push(method);
    }
  }

  logger.log(`[PatternLearner] Recorded ${action} for user ${userId}`);
}

function getPattern(userId) {
  return userPatterns[userId] || null;
}

function simulateAutopilot(userId) {
  const p = userPatterns[userId];
  if (!p || p.lastActions.length < 5) return null; // not enough data

  // Simulate decisions based on learned patterns
  const decisions = {
    launchCampaigns: false,
    requestPayout: false,
    preferredPlatform: p.preferredPlatforms[0] || 'instagram',
    payoutMethod: p.payoutMethods[0] || 'paypal',
    reason: ''
  };

  // If user usually creates campaigns every ~1 day, simulate launch
  const recentCampaigns = p.lastActions.filter(a => a.action === 'create_campaign' && (Date.now() - new Date(a.timestamp).getTime()) < 48 * 3600 * 1000);
  if (recentCampaigns.length > 0) {
    decisions.launchCampaigns = true;
    decisions.reason = 'User typically launches campaigns every 1–2 days';
  }

  // If user has earnings and usually payouts weekly, simulate payout
  const recentPayouts = p.lastActions.filter(a => a.action === 'payout' && (Date.now() - new Date(a.timestamp).getTime()) < 10 * 24 * 3600 * 1000);
  if (recentPayouts.length === 0 && p.payoutMethods.length > 0) {
    decisions.requestPayout = true;
    decisions.reason = 'User has not requested payout in >10 days; typical interval is weekly';
  }

  log('AUTOPILOT_SIMULATION', userId, decisions);
  return decisions;
}

module.exports = { recordAction, getPattern, simulateAutopilot };
