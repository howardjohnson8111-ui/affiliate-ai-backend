const logger = require('./logger');
const { log } = require('./auditLog');

// List of allowed IP ranges (your VPN/network)
const ALLOWED_IPS = [
  '127.0.0.1',           // Localhost
  '::1',                 // IPv6 localhost
  // Add your VPN IP ranges here
  // '10.0.0.0/8',        // Private network
  // '172.16.0.0/12',     // Private network
  // '192.168.0.0/16',    // Private network
];

function requireVPN(req, res, next) {
  const clientIP = req.ip || req.connection.remoteAddress || req.socket.remoteAddress;
  
  // For now, allow all (remove this in production)
  if (process.env.NODE_ENV === 'production') {
    const isAllowed = ALLOWED_IPS.some(allowed => {
      if (allowed.includes('/')) {
        // CIDR range check (simplified)
        return clientIP.startsWith(allowed.split('/')[0]);
      }
      return clientIP === allowed;
    });

    if (!isAllowed) {
      logger.log(`[Security] Blocked non-VPN IP: ${clientIP}`);
      log('VPN_BLOCKED', null, { ip: clientIP });
      return res.status(403).json({ error: 'Access denied. VPN required.' });
    }
  }

  next();
}

module.exports = { requireVPN };
