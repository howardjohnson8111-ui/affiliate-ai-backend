const logger = require('./logger');
const { log } = require('./auditLog');
const { simulateAutopilot } = require('./patternLearner');

// In-memory store; in production use Supabase
const switches = {};

function configure(userId, options = {}) {
  const { enabled = false, inactiveDays = 7 } = options;
  switches[userId] = { enabled, inactiveDays, lastSeen: new Date() };
  logger.log(`[DeadMansSwitch] Configured for user ${userId}: enabled=${enabled}, inactiveDays=${inactiveDays}`);
}

function ping(userId) {
  if (switches[userId]) {
    switches[userId].lastSeen = new Date();
  }
}

async function check(userId) {
  const sw = switches[userId];
  if (!sw || !sw.enabled) return null;

  const now = new Date();
  const daysSinceLastSeen = (now - sw.lastSeen) / (1000 * 60 * 60 * 24);
  if (daysSinceLastSeen >= sw.inactiveDays) {
    await log('DEAD_MANS_TRIGGERED', userId, { daysSinceLastSeen });
    const decisions = simulateAutopilot(userId);
    logger.log(`[DeadMansSwitch] Triggered for user ${userId} after ${daysSinceLastSeen.toFixed(1)} days`);
    return decisions;
  }
  return null;
}

module.exports = { configure, ping, check };
