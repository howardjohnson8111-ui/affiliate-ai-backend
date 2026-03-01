const logger = require('./logger');
const { log } = require('./auditLog');
const { evaluateRules } = require('./rulesEngine');
const { simulateAutopilot } = require('./patternLearner');
const { check: checkDeadMans } = require('./deadMansSwitch');

async function runScheduler() {
  logger.log('[Scheduler] Starting scheduled run');
  const results = {
    rules: [],
    autopilot: null,
    deadMans: null
  };

  // Evaluate all users' rules (placeholder: iterate all users)
  // In production, fetch all user IDs from Supabase
  const demoUserId = 'demo-user'; // Replace with actual user list
  try {
    const ruleResults = await evaluateRules(demoUserId);
    results.rules = ruleResults;
  } catch (err) {
    logger.error('[Scheduler] Rules evaluation failed:', err.message);
  }

  // Run autopilot simulation
  try {
    const autopilotDecisions = simulateAutopilot(demoUserId);
    if (autopilotDecisions) {
      results.autopilot = autopilotDecisions;
      await log('SCHEDULED_AUTOPILOT', demoUserId, autopilotDecisions);
    }
  } catch (err) {
    logger.error('[Scheduler] Autopilot failed:', err.message);
  }

  // Check dead man’s switch
  try {
    const deadMansDecisions = await checkDeadMans(demoUserId);
    if (deadMansDecisions) {
      results.deadMans = deadMansDecisions;
    }
  } catch (err) {
    logger.error('[Scheduler] Dead Man’s Switch check failed:', err.message);
  }

  logger.log('[Scheduler] Run completed');
  return results;
}

module.exports = { runScheduler };
