const logger = require('./logger');
const { log } = require('./auditLog');

// WebAuthn biometric authentication (placeholder)
function verifyBiometric(credentialId, signature, challenge) {
  // In production, integrate with WebAuthn API
  // For now, accept a configured biometric credential
  const validCredentialId = process.env.BIOMETRIC_CREDENTIAL_ID;
  
  return credentialId === validCredentialId && challenge === process.env.BIOMETRIC_CHALLENGE;
}

function requireBiometric(req, res, next) {
  const credentialId = req.headers['x-biometric-credential'];
  const signature = req.headers['x-biometric-signature'];
  const challenge = req.headers['x-biometric-challenge'];

  if (!credentialId || !signature || !challenge) {
    logger.log('[Security] Missing biometric headers');
    log('BIOMETRIC_MISSING', null);
    return res.status(401).json({ error: 'Biometric authentication required' });
  }

  if (!verifyBiometric(credentialId, signature, challenge)) {
    logger.log(`[Security] Invalid biometric: ${credentialId}`);
    log('BIOMETRIC_INVALID', null, { credentialId });
    return res.status(401).json({ error: 'Invalid biometric data' });
  }

  next();
}

function generateBiometricChallenge() {
  return {
    challenge: Buffer.from(Date.now().toString() + Math.random()).toString('base64'),
    userVerification: 'required',
    timeout: 60000
  };
}

module.exports = { requireBiometric, generateBiometricChallenge };
