const twilio = require('twilio');
const logger = require('./logger');

const accountSid = process.env.TWILIO_ACCOUNT_SID;
const authToken = process.env.TWILIO_AUTH_TOKEN;
const fromNumber = process.env.TWILIO_PHONE_NUMBER;

const client = accountSid && authToken ? twilio(accountSid, authToken) : null;

async function sendSMS(to, body) {
  if (!client) {
    logger.log('[SMS] Twilio not configured - skipping send');
    return false;
  }
  try {
    await client.messages.create({ body, from: fromNumber, to });
    logger.log(`[SMS] Sent to ${to}: ${body}`);
    return true;
  } catch (err) {
    logger.error('[SMS] Failed:', err.message);
    return false;
  }
}

module.exports = { sendSMS };
