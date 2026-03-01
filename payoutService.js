const logger = require('./logger');
const { log } = require('./auditLog');

const SUPPORTED_METHODS = ['paypal', 'cash_app', 'chime', 'bank_transfer', 'crypto'];

function validatePayoutMethod(method) {
  if (!SUPPORTED_METHODS.includes(method)) {
    throw new Error(`Unsupported payout method: ${method}. Supported: ${SUPPORTED_METHODS.join(', ')}`);
  }
}

async function requestPayout(userId, amount, method, recipient) {
  validatePayoutMethod(method);
  await log('PAYOUT_REQUEST', userId, { amount, method, recipient });

  // Placeholder: In production, integrate with each provider
  const instructions = {
    paypal: `Send $${amount} via PayPal to ${recipient}`,
    cash_app: `Send $${amount} via Cash App to $${recipient}`,
    chime: `Transfer $${amount} to Chime account ${recipient}`,
    bank_transfer: `Wire $${amount} to account ${recipient}`,
    crypto: `Send $${amount} equivalent in crypto to ${recipient}`
  };

  logger.log(`[Payout] ${method} requested for user ${userId}: ${instructions[method]}`);
  return {
    status: 'queued',
    message: `Payout queued via ${method}`,
    instructions: instructions[method],
    next_step: 'Admin will review and process within 24h'
  };
}

module.exports = { requestPayout, SUPPORTED_METHODS };
