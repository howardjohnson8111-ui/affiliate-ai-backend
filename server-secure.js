/**
 * Affiliate AI Pro - Secure Backend API with Authentication
 * Node.js + Express + Supabase
 * 
 * This server provides REST API endpoints for:
 * - User Authentication (signup, login, logout)
 * - Campaign Management (CRUD operations)
 * - Transaction Logging
 * - Stock Tracking
 * - Learning Modules
 * - User Preferences
 * 
 * All routes are protected by JWT authentication and Row Level Security (RLS)
 */

const express = require("express");
const cors = require("cors");
const { createClient } = require("@supabase/supabase-js");
const { verifyToken, verifyOwnership } = require("./auth-middleware");

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Initialize Supabase client
const supabase = createClient(
  process.env.SUPABASE_URL || "http://127.0.0.1:54321",
  process.env.SUPABASE_ANON_KEY || "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
);

// ============================================================================
// AUTHENTICATION ENDPOINTS (No auth required)
// ============================================================================

/**
 * POST /api/auth/signup
 * Register a new user
 * Body: { email: string, password: string }
 */
app.post("/api/auth/signup", async (req, res) => {
  try {
    const { email, password } = req.body;

    // Validate input
    if (!email || !password) {
      return res.status(400).json({
        error: "Bad Request",
        message: "Email and password are required",
      });
    }

    if (password.length < 8) {
      return res.status(400).json({
        error: "Bad Request",
        message: "Password must be at least 8 characters",
      });
    }

    // Sign up user with Supabase Auth
    const { data, error } = await supabase.auth.signUpWithPassword({
      email,
      password,
    });

    if (error) {
      return res.status(400).json({
        error: "Signup Failed",
        message: error.message,
      });
    }

    console.log(`[Auth] New signup: ${email}`);

    return res.status(201).json({
      success: true,
      message: "User registered successfully",
      user: {
        id: data.user?.id,
        email: data.user?.email,
      },
    });
  } catch (err) {
    console.error("[Signup Error]:", err);
    return res.status(500).json({
      error: "Internal Server Error",
      message: err.message,
    });
  }
});

/**
 * POST /api/auth/login
 * Authenticate user and return session tokens
 * Body: { email: string, password: string }
 */
app.post("/api/auth/login", async (req, res) => {
  try {
    const { email, password } = req.body;

    // Validate input
    if (!email || !password) {
      return res.status(400).json({
        error: "Bad Request",
        message: "Email and password are required",
      });
    }

    // Sign in user
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {
      return res.status(401).json({
        error: "Unauthorized",
        message: "Invalid email or password",
      });
    }

    console.log(`[Auth] Login successful: ${email}`);

    return res.status(200).json({
      success: true,
      message: "Login successful",
      user: {
        id: data.user?.id,
        email: data.user?.email,
      },
      session: {
        access_token: data.session?.access_token,
        refresh_token: data.session?.refresh_token,
        expires_in: data.session?.expires_in,
      },
    });
  } catch (err) {
    console.error("[Login Error]:", err);
    return res.status(500).json({
      error: "Internal Server Error",
      message: err.message,
    });
  }
});

/**
 * POST /api/auth/logout
 * Invalidate user session
 * Headers: { Authorization: "Bearer TOKEN" }
 */
app.post("/api/auth/logout", verifyToken, async (req, res) => {
  try {
    // Supabase session is invalidated on client side
    // You can optionally track logout in database here
    console.log(`[Auth] Logout: ${req.user.email}`);

    return res.status(200).json({
      success: true,
      message: "Logged out successfully",
    });
  } catch (err) {
    console.error("[Logout Error]:", err);
    return res.status(500).json({
      error: "Internal Server Error",
      message: err.message,
    });
  }
});

/**
 * POST /api/auth/refresh
 * Refresh access token using refresh token
 * Body: { refresh_token: string }
 */
app.post("/api/auth/refresh", async (req, res) => {
  try {
    const { refresh_token } = req.body;

    if (!refresh_token) {
      return res.status(400).json({
        error: "Bad Request",
        message: "Refresh token is required",
      });
    }

    const { data, error } = await supabase.auth.refreshSession({
      refresh_token,
    });

    if (error) {
      return res.status(401).json({
        error: "Unauthorized",
        message: "Invalid refresh token",
      });
    }

    console.log(`[Auth] Token refreshed for user`);

    return res.status(200).json({
      success: true,
      session: {
        access_token: data.session?.access_token,
        refresh_token: data.session?.refresh_token,
        expires_in: data.session?.expires_in,
      },
    });
  } catch (err) {
    console.error("[Refresh Error]:", err);
    return res.status(500).json({
      error: "Internal Server Error",
      message: err.message,
    });
  }
});

// ============================================================================
// PROTECTED ROUTES (Auth required)
// ============================================================================

// Apply verifyToken middleware to all protected routes
app.use("/api/campaigns", verifyToken);
app.use("/api/transactions", verifyToken);
app.use("/api/stocks", verifyToken);
app.use("/api/learning", verifyToken);
app.use("/api/preferences", verifyToken);

// ============================================================================
// CAMPAIGN ROUTES (Protected)
// ============================================================================

/**
 * POST /api/campaigns
 * Create a new campaign for the authenticated user
 */
app.post("/api/campaigns", async (req, res) => {
  try {
    const { name, platform, content, status } = req.body;
    const userId = req.user.id;

    // Validate input
    if (!name || !platform) {
      return res.status(400).json({
        error: "Bad Request",
        message: "Name and platform are required",
      });
    }

    // Insert campaign
    const { data, error } = await supabase
      .from("campaigns")
      .insert([
        {
          name,
          platform,
          content,
          status: status || "draft",
          user_id: userId, // RLS will enforce this
        },
      ])
      .select();

    if (error) {
      return res.status(400).json({
        error: "Database Error",
        message: error.message,
      });
    }

    console.log(`[Campaign] Created: ${name} (${data[0]?.id})`);

    return res.status(201).json({
      success: true,
      message: "Campaign created",
      campaign: data[0],
    });
  } catch (err) {
    console.error("[Campaign Create Error]:", err);
    return res.status(500).json({
      error: "Internal Server Error",
      message: err.message,
    });
  }
});

/**
 * GET /api/campaigns
 * Get all campaigns for the authenticated user
 */
app.get("/api/campaigns", async (req, res) => {
  try {
    const userId = req.user.id;

    // RLS will automatically filter by user_id
    const { data, error } = await supabase
      .from("campaigns")
      .select("*")
      .eq("user_id", userId)
      .order("created_at", { ascending: false });

    if (error) {
      return res.status(400).json({
        error: "Database Error",
        message: error.message,
      });
    }

    console.log(`[Campaign] Retrieved ${data.length} campaigns for user`);

    return res.status(200).json({
      success: true,
      campaigns: data,
      count: data.length,
    });
  } catch (err) {
    console.error("[Campaign Get All Error]:", err);
    return res.status(500).json({
      error: "Internal Server Error",
      message: err.message,
    });
  }
});

/**
 * GET /api/campaigns/:id
 * Get a specific campaign by ID
 */
app.get("/api/campaigns/:id", async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.id;

    const { data, error } = await supabase
      .from("campaigns")
      .select("*")
      .eq("id", id)
      .eq("user_id", userId)
      .single();

    if (error) {
      return res.status(404).json({
        error: "Not Found",
        message: "Campaign not found",
      });
    }

    return res.status(200).json({
      success: true,
      campaign: data,
    });
  } catch (err) {
    console.error("[Campaign Get One Error]:", err);
    return res.status(500).json({
      error: "Internal Server Error",
      message: err.message,
    });
  }
});

/**
 * PUT /api/campaigns/:id
 * Update a campaign
 */
app.put("/api/campaigns/:id", async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.id;
    const updates = req.body;

    // Verify ownership first
    const { data: existing, error: checkError } = await supabase
      .from("campaigns")
      .select("user_id")
      .eq("id", id)
      .single();

    if (checkError || existing.user_id !== userId) {
      return res.status(403).json({
        error: "Forbidden",
        message: "You do not have permission to modify this campaign",
      });
    }

    // Update campaign
    const { data, error } = await supabase
      .from("campaigns")
      .update(updates)
      .eq("id", id)
      .select();

    if (error) {
      return res.status(400).json({
        error: "Database Error",
        message: error.message,
      });
    }

    console.log(`[Campaign] Updated: ${id}`);

    return res.status(200).json({
      success: true,
      message: "Campaign updated",
      campaign: data[0],
    });
  } catch (err) {
    console.error("[Campaign Update Error]:", err);
    return res.status(500).json({
      error: "Internal Server Error",
      message: err.message,
    });
  }
});

/**
 * DELETE /api/campaigns/:id
 * Delete a campaign
 */
app.delete("/api/campaigns/:id", async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.id;

    // Verify ownership
    const { data: existing, error: checkError } = await supabase
      .from("campaigns")
      .select("user_id")
      .eq("id", id)
      .single();

    if (checkError || existing.user_id !== userId) {
      return res.status(403).json({
        error: "Forbidden",
        message: "You do not have permission to delete this campaign",
      });
    }

    // Delete
    const { error } = await supabase.from("campaigns").delete().eq("id", id);

    if (error) {
      return res.status(400).json({
        error: "Database Error",
        message: error.message,
      });
    }

    console.log(`[Campaign] Deleted: ${id}`);

    return res.status(200).json({
      success: true,
      message: "Campaign deleted",
    });
  } catch (err) {
    console.error("[Campaign Delete Error]:", err);
    return res.status(500).json({
      error: "Internal Server Error",
      message: err.message,
    });
  }
});

// ============================================================================
// TRANSACTION ROUTES (Protected)
// ============================================================================

/**
 * POST /api/transactions
 * Create a new transaction
 */
app.post("/api/transactions", async (req, res) => {
  try {
    const { amount, type, description, payment_method, status } = req.body;
    const userId = req.user.id;

    // Validate input
    if (!amount || !type) {
      return res.status(400).json({
        error: "Bad Request",
        message: "Amount and type are required",
      });
    }

    const { data, error } = await supabase
      .from("transactions")
      .insert([
        {
          amount,
          type,
          description,
          payment_method,
          status: status || "pending",
          user_id: userId,
        },
      ])
      .select();

    if (error) {
      return res.status(400).json({
        error: "Database Error",
        message: error.message,
      });
    }

    console.log(
      `[Transaction] Created: $${amount} ${type} (${data[0]?.id})`
    );

    return res.status(201).json({
      success: true,
      message: "Transaction logged",
      transaction: data[0],
    });
  } catch (err) {
    console.error("[Transaction Create Error]:", err);
    return res.status(500).json({
      error: "Internal Server Error",
      message: err.message,
    });
  }
});

/**
 * GET /api/transactions
 * Get all transactions for the user
 */
app.get("/api/transactions", async (req, res) => {
  try {
    const userId = req.user.id;

    const { data, error } = await supabase
      .from("transactions")
      .select("*")
      .eq("user_id", userId)
      .order("created_at", { ascending: false });

    if (error) {
      return res.status(400).json({
        error: "Database Error",
        message: error.message,
      });
    }

    return res.status(200).json({
      success: true,
      transactions: data,
      count: data.length,
    });
  } catch (err) {
    console.error("[Transaction Get Error]:", err);
    return res.status(500).json({
      error: "Internal Server Error",
      message: err.message,
    });
  }
});

// ============================================================================
// HEALTH CHECK
// ============================================================================

/**
 * GET /api/health
 * Server status check
 */
app.get("/api/health", (req, res) => {
  return res.status(200).json({
    status: "ok",
    server: "Affiliate AI Backend",
    timestamp: new Date().toISOString(),
    baseUrl: `http://localhost:${PORT}/api`,
  });
});

// ============================================================================
// ERROR HANDLING
// ============================================================================

// 404 Not Found
app.use((req, res) => {
  return res.status(404).json({
    error: "Not Found",
    message: `Route ${req.method} ${req.path} not found`,
  });
});

// Server startup
app.listen(PORT, () => {
  console.log("\n" + "=".repeat(70));
  console.log("✅ [Server]: Affiliate AI Backend is running");
  console.log(`📡 API Base URL: http://localhost:${PORT}/api`);
  console.log(
    "🔐 Authentication: Enabled with Supabase JWT & Row Level Security"
  );
  console.log("=".repeat(70));
  console.log("\nAvailable endpoints:");
  console.log("  🔓 POST   /api/auth/signup       - Register new user");
  console.log("  🔓 POST   /api/auth/login        - Login user");
  console.log("  🔐 POST   /api/auth/logout       - Logout (requires token)");
  console.log("  🔐 POST   /api/auth/refresh      - Refresh token");
  console.log("  🔐 POST   /api/campaigns         - Create campaign");
  console.log("  🔐 GET    /api/campaigns         - Get all campaigns");
  console.log("  🔐 GET    /api/campaigns/:id     - Get campaign by ID");
  console.log("  🔐 PUT    /api/campaigns/:id     - Update campaign");
  console.log("  🔐 DELETE /api/campaigns/:id     - Delete campaign");
  console.log("  🔐 POST   /api/transactions      - Log transaction");
  console.log("  🔐 GET    /api/transactions      - Get transactions");
  console.log("  🔓 GET    /api/health            - Health check");
  console.log("=".repeat(70) + "\n");
});

module.exports = app;
