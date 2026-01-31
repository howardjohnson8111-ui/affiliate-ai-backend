# Supabase Authentication & Security Setup Guide

This guide walks you through setting up Supabase authentication and Row Level Security (RLS) for Affiliate AI Pro.

## Prerequisites

- Supabase project created
- Node.js backend running
- Supabase client libraries installed

---

## Step 1: Enable Email/Password Authentication in Supabase Dashboard

### 1.1 Navigate to Authentication Providers

1. Go to your Supabase project dashboard: https://app.supabase.com
2. Click on **Authentication** in the left sidebar
3. Click on **Providers**
4. Ensure **Email** provider is **enabled**
   - Allow sign ups: ✅ ON
   - Confirm email: You can choose (OFF for testing, ON for production)
   - Double confirm changes: Choose preference

### 1.2 (Optional) Enable Social Providers

You can also enable:
- Google OAuth
- GitHub OAuth
- Discord OAuth
- Apple OAuth
- Microsoft OAuth

For now, we'll focus on email/password.

---

## Step 2: Add `user_id` Column to Database Tables

For each user-specific table (campaigns, transactions, stocks, learning_modules, user_preferences), you need to:

### 2.1 Access Table Editor

1. Click **Database** in left sidebar
2. Click **Table Editor**
3. Select the table (start with `campaigns`)

### 2.2 Add `user_id` Column

For each table, add a new column:

| Property | Value |
|----------|-------|
| Name | `user_id` |
| Type | `uuid` |
| Default value | `auth.uid()` |
| Is nullable | ❌ No |
| Is unique | No |
| Is primary key | No |

**Repeat for tables:**
- campaigns
- transactions
- stocks
- learning_modules
- user_preferences

---

## Step 3: Enable Row Level Security (RLS)

### 3.1 Enable RLS on Tables

1. Go to **Database > Table Editor**
2. Select the first table (e.g., `campaigns`)
3. Click **RLS** button in top right
4. Toggle **Enable RLS** to ON
5. Click **Create policy**

### 3.2 Create RLS Policies

For each table, create policies that restrict access:

#### Policy 1: SELECT (Users can only read their own data)

```sql
CREATE POLICY "Users can read own campaigns"
ON campaigns
FOR SELECT
USING (auth.uid() = user_id);
```

#### Policy 2: INSERT (Users can only insert their own records)

```sql
CREATE POLICY "Users can create own campaigns"
ON campaigns
FOR INSERT
WITH CHECK (auth.uid() = user_id);
```

#### Policy 3: UPDATE (Users can only modify their own data)

```sql
CREATE POLICY "Users can update own campaigns"
ON campaigns
FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);
```

#### Policy 4: DELETE (Users can only delete their own data)

```sql
CREATE POLICY "Users can delete own campaigns"
ON campaigns
FOR DELETE
USING (auth.uid() = user_id);
```

**Repeat for all user-specific tables:**
- transactions
- stocks
- learning_modules
- user_preferences

### 3.3 SQL Script (Easy Way)

Alternatively, go to **SQL Editor** and paste this script:

```sql
-- Enable RLS on all user-specific tables
ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE stocks ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_modules ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

-- Campaigns policies
CREATE POLICY "Users can read own campaigns" ON campaigns FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can create own campaigns" ON campaigns FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own campaigns" ON campaigns FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own campaigns" ON campaigns FOR DELETE USING (auth.uid() = user_id);

-- Transactions policies
CREATE POLICY "Users can read own transactions" ON transactions FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can create own transactions" ON transactions FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own transactions" ON transactions FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own transactions" ON transactions FOR DELETE USING (auth.uid() = user_id);

-- Stocks policies
CREATE POLICY "Users can read own stocks" ON stocks FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can create own stocks" ON stocks FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own stocks" ON stocks FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own stocks" ON stocks FOR DELETE USING (auth.uid() = user_id);

-- Learning modules policies
CREATE POLICY "Users can read own learning modules" ON learning_modules FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can create own learning modules" ON learning_modules FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own learning modules" ON learning_modules FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own learning modules" ON learning_modules FOR DELETE USING (auth.uid() = user_id);

-- User preferences policies
CREATE POLICY "Users can read own preferences" ON user_preferences FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update own preferences" ON user_preferences FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
```

---

## Step 4: Verify Table Structure

After adding `user_id` columns, your tables should look like:

### campaigns
- id (uuid, primary key)
- **user_id (uuid, not null, default: auth.uid())**
- name (text)
- platform (text)
- content (text)
- status (text)
- created_at (timestamp)
- ... other fields

### transactions
- id (uuid, primary key)
- **user_id (uuid, not null, default: auth.uid())**
- amount (numeric)
- type (text)
- payment_method (text)
- status (text)
- created_at (timestamp)
- ... other fields

---

## Step 5: Get Your Supabase Credentials

You'll need these for your backend:

1. Go to **Project Settings > API**
2. Copy:
   - **Project URL**: `https://your-project.supabase.co`
   - **Anon Key**: `eyJ...` (public key for client-side)
   - **Service Role Key**: `eyJ...` (secret key for server-side, keep safe!)

3. Update your `.env` file:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

---

## Next Steps

1. ✅ Enable email/password authentication
2. ✅ Add user_id columns to tables
3. ✅ Enable RLS and create policies
4. 👉 **Update server.js with auth endpoints** (see auth-middleware.js)
5. Update ai_service.py for authenticated requests
6. Test with auth test scripts
7. Build React frontend with login

---

## Security Best Practices

✅ **DO:**
- Use HTTPS in production
- Keep `SUPABASE_SERVICE_ROLE_KEY` secret (server-side only)
- Always verify JWT tokens on the backend
- Enable RLS on all user-specific tables
- Use `auth.uid()` in RLS policies
- Validate and sanitize user input

❌ **DON'T:**
- Expose `SUPABASE_SERVICE_ROLE_KEY` in client code
- Disable RLS on user-specific tables
- Trust client-side validation alone
- Store sensitive data in JWT tokens
- Skip email verification in production

---

## Troubleshooting

### "User not found" error
- Ensure user is created via signup endpoint
- Check if email is verified (if required)

### "RLS violation" error
- Verify `user_id` column exists on table
- Ensure RLS policies are correctly created
- Check that `auth.uid()` is working (SQL Editor test)

### "Permission denied" error
- Verify JWT token is being sent in Authorization header
- Check that Supabase client is initialized with correct credentials
- Ensure RLS policies allow the operation

---

## Testing Authentication

See `test_auth.py` and `test_auth.js` for complete test scripts.

Quick test:
```bash
# Signup
curl -X POST http://localhost:3001/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Login
curl -X POST http://localhost:3001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Use token in subsequent requests
curl -X GET http://localhost:3001/api/campaigns \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

**Congratulations!** Your Affiliate AI Pro now has enterprise-grade authentication and authorization! 🔐
