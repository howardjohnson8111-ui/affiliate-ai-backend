const fs = require('fs').promises;
const path = require('path');
const logger = require('./logger');
const { log } = require('./auditLog');

const ALERT_FILE = path.join(__dirname, 'SECURITY_ALERTS.log');

async function alert(event, details = {}) {
  const entry = {
    timestamp: new Date().toISOString(),
    severity: 'CRITICAL',
    event,
    ...details
  };
  await fs.appendFile(ALERT_FILE, JSON.stringify(entry) + '\n');
  logger.log(`[SECURITY ALERT] ${event}: ${JSON.stringify(details)}`);
  // Optionally send SMS if configured
  if (process.env.ADMIN_PHONE) {
    const { sendSMS } = require('./smsService');
    await sendSMS(process.env.ADMIN_PHONE, `SECURITY ALERT: ${event}`);
  }
}

// Detect suspicious patterns
function detectSuspicious(req, res, next) {
  const ip = req.ip;
  const ua = req.get('User-Agent') || '';
  const suspicious = (
    ua.includes('bot') ||
    ua.includes('curl') ||
    ua.includes('python') ||
    req.headers['x-forwarded-for']?.split(',').length > 3
  );
  if (suspicious) {
    alert('SUSPICIOUS_REQUEST', { ip, ua });
    return res.status(403).json({ error: 'Forbidden' });
  }
  next();
}

module.exports = { alert, detectSuspicious };
