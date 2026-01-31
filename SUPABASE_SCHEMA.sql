-- Affiliate AI Pro - Supabase Database Schema
-- Run this SQL in your Supabase SQL Editor to set up the complete database
-- ============================================================================

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- 1. USERS TABLE (Handled by Supabase Auth - this is for additional user info)
-- ============================================================================

CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE,
    display_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_user_profiles_email ON user_profiles(email);
CREATE INDEX IF NOT EXISTS idx_user_profiles_username ON user_profiles(username);

-- ============================================================================
-- 2. CAMPAIGNS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS campaigns (
    id TEXT PRIMARY KEY DEFAULT (gen_random_uuid()::text),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    platform TEXT NOT NULL,
    affiliate_link TEXT,
    clicks INTEGER DEFAULT 0,
    content TEXT,
    conversions INTEGER DEFAULT 0,
    earnings DECIMAL(10, 2) DEFAULT 0,
    image_url TEXT,
    scheduled_date TEXT,
    status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'paused', 'completed')),
    tags TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for campaigns
CREATE INDEX IF NOT EXISTS idx_campaigns_user_id ON campaigns(user_id);
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status);
CREATE INDEX IF NOT EXISTS idx_campaigns_created_at ON campaigns(created_at DESC);

-- ============================================================================
-- 3. TRANSACTIONS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS transactions (
    id TEXT PRIMARY KEY DEFAULT (gen_random_uuid()::text),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    amount DECIMAL(10, 2) NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('deposit', 'withdrawal', 'dividend', 'affiliate_payout', 'stock_purchase', 'stock_sale')),
    description TEXT,
    payment_method TEXT CHECK (payment_method IN ('paypal', 'apple_pay', 'cash_app', 'chime', 'bank_transfer', 'crypto', NULL)),
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'failed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for transactions
CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(type);
CREATE INDEX IF NOT EXISTS idx_transactions_status ON transactions(status);
CREATE INDEX IF NOT EXISTS idx_transactions_created_at ON transactions(created_at DESC);

-- ============================================================================
-- 4. STOCKS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS stocks (
    id TEXT PRIMARY KEY DEFAULT (gen_random_uuid()::text),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    ticker TEXT NOT NULL,
    shares DECIMAL(10, 4) NOT NULL,
    purchase_price DECIMAL(10, 2) NOT NULL,
    current_price DECIMAL(10, 2),
    purchase_date TEXT,
    broker TEXT,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for stocks
CREATE INDEX IF NOT EXISTS idx_stocks_user_id ON stocks(user_id);
CREATE INDEX IF NOT EXISTS idx_stocks_ticker ON stocks(ticker);
CREATE INDEX IF NOT EXISTS idx_stocks_created_at ON stocks(created_at DESC);

-- ============================================================================
-- 5. LEARNING MODULES TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS learning_modules (
    id TEXT PRIMARY KEY DEFAULT (gen_random_uuid()::text),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    platform TEXT,
    description TEXT,
    progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    target_completion TEXT,
    status TEXT DEFAULT 'in_progress' CHECK (status IN ('not_started', 'in_progress', 'completed', 'paused')),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for learning modules
CREATE INDEX IF NOT EXISTS idx_learning_modules_user_id ON learning_modules(user_id);
CREATE INDEX IF NOT EXISTS idx_learning_modules_status ON learning_modules(status);
CREATE INDEX IF NOT EXISTS idx_learning_modules_created_at ON learning_modules(created_at DESC);

-- ============================================================================
-- 6. USER PREFERENCES TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS user_preferences (
    id TEXT PRIMARY KEY DEFAULT (gen_random_uuid()::text),
    user_id UUID NOT NULL UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,
    theme TEXT DEFAULT 'dark' CHECK (theme IN ('light', 'dark', 'auto')),
    default_view TEXT DEFAULT 'dashboard' CHECK (default_view IN ('dashboard', 'campaigns', 'transactions', 'stocks', 'learning', 'chat')),
    notifications_enabled BOOLEAN DEFAULT true,
    currency TEXT DEFAULT 'USD',
    language TEXT DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for user preferences
CREATE INDEX IF NOT EXISTS idx_user_preferences_user_id ON user_preferences(user_id);

-- ============================================================================
-- 7. CONVERSATION HISTORY TABLE (For AI chat history)
-- ============================================================================

CREATE TABLE IF NOT EXISTS conversation_history (
    id TEXT PRIMARY KEY DEFAULT (gen_random_uuid()::text),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    persona TEXT NOT NULL,
    user_message TEXT NOT NULL,
    ai_response TEXT,
    tools_used TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for conversation history
CREATE INDEX IF NOT EXISTS idx_conversation_history_user_id ON conversation_history(user_id);
CREATE INDEX IF NOT EXISTS idx_conversation_history_persona ON conversation_history(persona);
CREATE INDEX IF NOT EXISTS idx_conversation_history_created_at ON conversation_history(created_at DESC);

-- ============================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ============================================================================

-- Enable RLS on all tables
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE stocks ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_modules ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversation_history ENABLE ROW LEVEL SECURITY;

-- User Profiles Policies
CREATE POLICY "Users can view their own profile"
    ON user_profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile"
    ON user_profiles FOR UPDATE
    USING (auth.uid() = id);

CREATE POLICY "Users can insert their own profile"
    ON user_profiles FOR INSERT
    WITH CHECK (auth.uid() = id);

-- Campaigns Policies
CREATE POLICY "Users can view their own campaigns"
    ON campaigns FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create campaigns"
    ON campaigns FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own campaigns"
    ON campaigns FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own campaigns"
    ON campaigns FOR DELETE
    USING (auth.uid() = user_id);

-- Transactions Policies
CREATE POLICY "Users can view their own transactions"
    ON transactions FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create transactions"
    ON transactions FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own transactions"
    ON transactions FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own transactions"
    ON transactions FOR DELETE
    USING (auth.uid() = user_id);

-- Stocks Policies
CREATE POLICY "Users can view their own stocks"
    ON stocks FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create stocks"
    ON stocks FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own stocks"
    ON stocks FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own stocks"
    ON stocks FOR DELETE
    USING (auth.uid() = user_id);

-- Learning Modules Policies
CREATE POLICY "Users can view their own learning modules"
    ON learning_modules FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create learning modules"
    ON learning_modules FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own learning modules"
    ON learning_modules FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own learning modules"
    ON learning_modules FOR DELETE
    USING (auth.uid() = user_id);

-- User Preferences Policies
CREATE POLICY "Users can view their own preferences"
    ON user_preferences FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can update their own preferences"
    ON user_preferences FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own preferences"
    ON user_preferences FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Conversation History Policies
CREATE POLICY "Users can view their own conversation history"
    ON conversation_history FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create conversation entries"
    ON conversation_history FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- ============================================================================
-- VIEWS (Optional - useful for analytics)
-- ============================================================================

-- View for user campaign statistics
CREATE OR REPLACE VIEW campaign_stats AS
SELECT 
    user_id,
    COUNT(*) as total_campaigns,
    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_campaigns,
    SUM(clicks) as total_clicks,
    SUM(conversions) as total_conversions,
    SUM(earnings) as total_earnings
FROM campaigns
GROUP BY user_id;

-- View for user transaction summary
CREATE OR REPLACE VIEW transaction_summary AS
SELECT 
    user_id,
    SUM(CASE WHEN type = 'deposit' THEN amount ELSE 0 END) as total_deposits,
    SUM(CASE WHEN type = 'withdrawal' THEN amount ELSE 0 END) as total_withdrawals,
    SUM(CASE WHEN type = 'affiliate_payout' THEN amount ELSE 0 END) as total_affiliate_payouts,
    SUM(CASE WHEN type = 'dividend' THEN amount ELSE 0 END) as total_dividends,
    COUNT(*) as total_transactions
FROM transactions
WHERE status = 'completed'
GROUP BY user_id;

-- ============================================================================
-- FUNCTIONS
-- ============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for updating updated_at
CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_campaigns_updated_at BEFORE UPDATE ON campaigns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_transactions_updated_at BEFORE UPDATE ON transactions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_stocks_updated_at BEFORE UPDATE ON stocks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_learning_modules_updated_at BEFORE UPDATE ON learning_modules
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_preferences_updated_at BEFORE UPDATE ON user_preferences
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Check all tables are created
-- SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;

-- Check all policies are in place
-- SELECT schemaname, tablename, policyname, qual, with_check FROM pg_policies;

-- ============================================================================
-- NOTE: After running this script:
-- 1. Go to Supabase Dashboard > Authentication > Users to manage users
-- 2. Enable Email authentication in Authentication > Providers
-- 3. Get your anon key and service_role_key from Settings > API
-- 4. Update your .env file with SUPABASE_URL and keys
-- ============================================================================
