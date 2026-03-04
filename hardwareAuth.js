const logger = require('./logger');
const { log } = require('./auditLog');

// Simple hardware key validation (placeholder for real WebAuthn/YubiKey)
function validateHardwareKey(keyId, signature) {
  // In production, integrate with WebAuthn or YubiKey APIs
  // For now, accept a configured hardware key
  const validKeyId = process.env.HARDWARE_KEY_ID;
  const validSignature = process.env.HARDWARE_KEY_SIGNATURE;

  return keyId === validKeyId && signature === validSignature;
}

function requireHardwareKey(req, res, next) {
  const keyId = req.headers['x-hardware-key-id'];
  const signature = req.headers['x-hardware-signature'];

  if (!keyId || !signature) {
    logger.log('[Security] Missing hardware key headers');
    log('HARDWARE_KEY_MISSING', null);
    return res.status(401).json({ error: 'Hardware key required' });
  }

  if (!validateHardwareKey(keyId, signature)) {
    logger.log(`[Security] Invalid hardware key: ${keyId}`);
    log('HARDWARE_KEY_INVALID', null, { keyId });
    return res.status(401).json({ error: 'Invalid hardware key' });
  }

  next();
}

function generateHardwareChallenge() {
  // Generate a challenge for hardware key
  return {
    challenge: Buffer.from(Date.now().toString()).toString('base64'),
    timeout: 60000
  };
}

module.exports = { requireHardwareKey, generateHardwareChallenge };
