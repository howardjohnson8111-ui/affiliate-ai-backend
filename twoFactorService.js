const speakeasy = require('speakeasy');
const QRCode = require('qrcode');
const logger = require('./logger');
const { log } = require('./auditLog');

// In-memory store for demo; in production use Supabase
const user2FA = {};

function generateSecret(userId) {
  const secret = speakeasy.generateSecret({
    name: `Affiliate AI Pro (${userId})`,
    issuer: 'Affiliate AI Pro'
  });
  user2FA[userId] = { secret: secret.base32, enabled: false };
  return secret;
}

async function generateQRCode(secret) {
  return await QRCode.toDataURL(secret.otpauth_url);
}

function verifyToken(userId, token) {
  const record = user2FA[userId];
  if (!record || !record.secret) return false;
  const verified = speakeasy.totp.verify({
    secret: record.secret,
    encoding: 'base32',
    token,
    window: 2
  });
  if (verified) {
    log('2FA_SUCCESS', userId, { method: 'TOTP' });
  } else {
    log('2FA_FAILED', userId, { method: 'TOTP' });
  }
  return verified;
}

function enable2FA(userId) {
  if (user2FA[userId]) user2FA[userId].enabled = true;
}

function is2FAEnabled(userId) {
  return user2FA[userId]?.enabled || false;
}

module.exports = {
  generateSecret,
  generateQRCode,
  verifyToken,
  enable2FA,
  is2FAEnabled
};
