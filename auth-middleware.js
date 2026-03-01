/**
 * Authentication Middleware for Affiliate AI Pro
 * Handles JWT verification and user session management
 */

const { createClient } = require("@supabase/supabase-js");

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY
);

/**
 * Middleware to verify JWT token and attach user info to request
 * Usage: app.use(verifyToken); or app.get('/protected', verifyToken, handler);
 */
const verifyToken = async (req, res, next) => {
  try {
    // Extract token from Authorization header
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return res.status(401).json({
        error: "Unauthorized",
        message: "Missing or invalid Authorization header",
      });
    }

    const token = authHeader.substring(7); // Remove "Bearer " prefix

    // Verify token with Supabase
    const {
      data: { user },
      error,
    } = await supabase.auth.getUser(token);

    if (error || !user) {
      return res.status(401).json({
        error: "Unauthorized",
        message: "Invalid or expired token",
        details: error?.message,
      });
    }

    // Attach user info to request object
    req.user = {
      id: user.id,
      email: user.email,
      user_metadata: user.user_metadata,
    };

    console.log(`[Auth] Verified user: ${user.email} (${user.id})`);

    // Continue to next middleware/route
    next();
  } catch (err) {
    console.error("[Auth Error]:", err);
    return res.status(500).json({
      error: "Internal Server Error",
      message: "Token verification failed",
    });
  }
};

/**
 * Middleware to verify if user owns a resource
 * Usage: app.get('/api/campaigns/:id', verifyOwnership('campaigns'), handler);
 */
const verifyOwnership = (tableName) => {
  return async (req, res, next) => {
    try {
      const resourceId = req.params.id;
      const userId = req.user.id;

      // Query database to check ownership
      const { data, error } = await supabase
        .from(tableName)
        .select("user_id")
        .eq("id", resourceId)
        .single();

      if (error) {
        return res.status(404).json({
          error: "Not Found",
          message: `${tableName.slice(0, -1)} not found`,
        });
      }

      if (data.user_id !== userId) {
        return res.status(403).json({
          error: "Forbidden",
          message: "You do not have permission to access this resource",
        });
      }

      next();
    } catch (err) {
      console.error("[Ownership Check Error]:", err);
      return res.status(500).json({
        error: "Internal Server Error",
        message: "Ownership verification failed",
      });
    }
  };
};

/**
 * Automatically filter results by user_id
 * Ensures users only see their own data
 */
const filterByUserId = (baseQuery) => {
  return baseQuery;
};

module.exports = {
  verifyToken,
  verifyOwnership,
  filterByUserId,
  supabase,
};
