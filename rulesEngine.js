const logger = require('./logger');
const { log } = require('./auditLog');
const { simulateAutopilot } = require('./patternLearner');

// In-memory store; in production use Supabase
const userRules = {};

function addRule(userId, rule) {
  if (!userRules[userId]) userRules[userId] = [];
  const ruleWithId = { ...rule, id: Date.now().toString(), createdAt: new Date() };
  userRules[userId].push(ruleWithId);
  logger.log(`[RulesEngine] Added rule for user ${userId}: ${rule.type}`);
  return ruleWithId;
}

function removeRule(userId, ruleId) {
  if (!userRules[userId]) return;
  userRules[userId] = userRules[userId].filter(r => r.id !== ruleId);
  logger.log(`[RulesEngine] Removed rule ${ruleId} for user ${userId}`);
}

function getRules(userId) {
  return userRules[userId] || [];
}

async function evaluateRules(userId) {
  const rules = getRules(userId);
  const results = [];
  for (const rule of rules) {
    if (await shouldTrigger(rule, userId)) {
      const action = await executeRule(rule, userId);
      results.push({ rule: rule.id, action });
      await log('RULE_TRIGGERED', userId, { ruleId: rule.id, type: rule.type, action });
    }
  }
  return results;
}

async function shouldTrigger(rule, userId) {
  const now = new Date();
  switch (rule.trigger.type) {
    case 'inactive_days':
      // Simplified: use dead man’s switch logic
      return false; // Let dead man’s switch handle this
    case 'schedule':
      const [hour, minute] = rule.trigger.time.split(':').map(Number);
      const scheduled = new Date();
      scheduled.setHours(hour, minute, 0, 0);
      return Math.abs(now - scheduled) < 60000; // Within 1 minute
    case 'event':
      // Placeholder: check if event occurred
      return false;
    default:
      return false;
  }
}

async function executeRule(rule, userId) {
  switch (rule.type) {
    case 'launch_campaign':
      return { type: 'campaign_launched', platform: rule.payload.platform, message: 'Campaign launched by rule' };
    case 'request_payout':
      return { type: 'payout_requested', method: rule.payload.method, amount: rule.payload.amount, message: 'Payout requested by rule' };
    case 'send_alert':
      const { sendSMS } = require('./smsService');
      await sendSMS(rule.payload.phone, rule.payload.message);
      return { type: 'alert_sent', message: 'SMS alert sent' };
    default:
      return { type: 'unknown', message: 'Unknown rule type' };
  }
}

module.exports = { addRule, removeRule, getRules, evaluateRules };
