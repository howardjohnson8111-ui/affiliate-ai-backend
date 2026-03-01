/**
 * Supabase Client Configuration for Node.js Backend
 * This file initializes the Supabase client and provides helper methods
 */

const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

// Initialize Supabase client
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
    console.warn('[WARNING] Supabase credentials not found in environment variables');
    console.warn('Please set SUPABASE_URL and SUPABASE_ANON_KEY in your .env file');
}

const supabase = createClient(supabaseUrl, supabaseKey);

/**
 * Helper function to get user from auth token
 */
async function getUserFromToken(token) {
    try {
        const { data: { user }, error } = await supabase.auth.getUser(token);
        if (error) throw error;
        return user;
    } catch (error) {
        console.error('[Supabase Auth Error]:', error.message);
        return null;
    }
}

/**
 * Helper function to fetch user data with their preferences
 */
async function getUserWithPreferences(userId) {
    try {
        // Fetch user preferences
        const { data, error } = await supabase
            .from('user_preferences')
            .select('*')
            .eq('user_id', userId)
            .single();

        if (error && error.code !== 'PGRST116') throw error;
        
        return data || {
            user_id: userId,
            theme: 'dark',
            default_view: 'dashboard',
            notifications_enabled: true,
            currency: 'USD',
            language: 'en'
        };
    } catch (error) {
        console.error('[Supabase Preferences Error]:', error.message);
        return null;
    }
}

/**
 * Helper function to insert or update user preferences
 */
async function saveUserPreferences(userId, preferences) {
    try {
        const { data, error } = await supabase
            .from('user_preferences')
            .upsert({
                user_id: userId,
                ...preferences,
                updated_at: new Date().toISOString()
            }, { onConflict: 'user_id' })
            .select();

        if (error) throw error;
        return data[0];
    } catch (error) {
        console.error('[Supabase Save Preferences Error]:', error.message);
        return null;
    }
}

/**
 * Middleware to authenticate requests using Supabase
 */
function authMiddleware(req, res, next) {
    const token = req.headers.authorization?.replace('Bearer ', '');
    
    if (!token) {
        return res.status(401).json({ error: 'Missing authorization token' });
    }

    // Store token in request for later use
    req.supabaseToken = token;
    
    next();
}

/**
 * Middleware to get user from token and attach to request
 */
async function userMiddleware(req, res, next) {
    const token = req.supabaseToken;
    
    if (!token) {
        return res.status(401).json({ error: 'Missing authorization token' });
    }

    const user = await getUserFromToken(token);
    
    if (!user) {
        return res.status(401).json({ error: 'Invalid or expired token' });
    }

    req.user = user;
    next();
}

module.exports = {
    supabase,
    getUserFromToken,
    getUserWithPreferences,
    saveUserPreferences,
    authMiddleware,
    userMiddleware
};
