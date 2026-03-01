const fs = require('fs').promises;
const path = require('path');
const logger = require('./logger');

const LOG_FILE = path.join(__dirname, 'audit.log');

async function log(event, userId, details = {}) {
  const entry = {
    timestamp: new Date().toISOString(),
    event,
    userId,
    ip: details.ip,
    userAgent: details.userAgent,
    ...details
  };
  const line = JSON.stringify(entry) + '\n';
  try {
    await fs.appendFile(LOG_FILE, line);
    logger.log(`[Audit] ${event}: ${entry.userId}`);
  } catch (err) {
    logger.error('[Audit] Failed to write log:', err.message);
  }
}

module.exports = { log };
