# Phase 1: Supabase Setup - Complete Guide

This guide will walk you through setting up Supabase and creating the database schema for Affiliate AI Pro.

## Step 1: Create a Supabase Account & Project

### 1.1 Sign Up / Log In
1. Go to https://supabase.com
2. Click "Sign Up" (or login if you have an account)
3. Sign up with GitHub, Google, or email

### 1.2 Create a New Project
1. Click "New Project" or go to your dashboard
2. Fill in the project details:
   - **Name:** `affiliate-ai-pro` (or your preferred name)
   - **Database Password:** Create a strong password (save this!)
   - **Region:** Choose closest to you (e.g., us-east-1 for US)
3. Click "Create new project"
4. Wait for project to initialize (~2-3 minutes)

---

## Step 2: Get Your API Keys

Once your project is ready:

### 2.1 Find Your API Keys
1. Go to **Settings** (gear icon, bottom left)
2. Click **API** in the left sidebar
3. You'll see:
   - **Project URL** - Copy this
   - **anon (public) key** - Copy this
   - **service_role (secret) key** - Copy this (keep secret!)

### 2.2 Update Your .env File
Open your `.env` file and add:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
```

---

## Step 3: Create the Database Schema

### 3.1 Access the SQL Editor
1. In Supabase dashboard, go to **SQL Editor** (left sidebar)
2. Click **New Query** button
3. You now have a blank SQL editor

### 3.2 Copy & Paste the Schema
1. Open the file `SUPABASE_SCHEMA.sql` in this directory
2. Copy **ALL** the SQL code
3. Paste it into the Supabase SQL Editor
4. Click **Run** (or press Ctrl+Enter)

You should see:
```
Success. No rows returned
```

This means all tables, indexes, RLS policies, and functions have been created!

### 3.3 Verify Tables Were Created
1. Go to **Table Editor** (left sidebar)
2. You should see these tables:
   - `user_profiles`
   - `campaigns`
   - `transactions`
   - `stocks`
   - `learning_modules`
   - `user_preferences`
   - `conversation_history`

---

## Step 4: Configure Authentication

### 4.1 Enable Email Authentication
1. Go to **Authentication** (left sidebar)
2. Click **Providers** tab
3. Find "Email" and toggle it **ON**
4. Keep default settings
5. Save

### 4.2 Set Email Templates (Optional)
1. Under **Authentication**, click **Email Templates**
2. You can customize email templates for:
   - Confirmation email
   - Password recovery
   - Email change
   - Magic link
3. For now, the defaults are fine

### 4.3 Get Auth Keys
1. Go to **Settings** > **API**
2. Under "anon key", copy the value
3. Under "service_role key", copy the value
4. Save these in your `.env` file (already done in Step 2.2)

---

## Step 5: Test the Connection

### 5.1 Install Required Packages (if not already installed)

**For Node.js:**
```bash
npm install @supabase/supabase-js dotenv
```

**For Python:**
```bash
pip install supabase python-dotenv
```

### 5.2 Test Node.js Connection
Create a test file `test-supabase-node.js`:
```javascript
const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

const supabase = createClient(
    process.env.SUPABASE_URL,
    process.env.SUPABASE_ANON_KEY
);

async function test() {
    try {
        // Try to fetch campaigns table
        const { data, error } = await supabase
            .from('campaigns')
            .select('*')
            .limit(1);
        
        if (error) throw error;
        console.log('✅ Supabase Node.js connection successful!');
        console.log('Sample data:', data);
    } catch (error) {
        console.error('❌ Connection failed:', error.message);
    }
}

test();
```

Run it:
```bash
node test-supabase-node.js
```

### 5.3 Test Python Connection
Create a test file `test_supabase_python.py`:
```python
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_ANON_KEY")
)

try:
    response = supabase.table('campaigns').select('*').limit(1).execute()
    print('✅ Supabase Python connection successful!')
    print('Sample data:', response.data)
except Exception as e:
    print('❌ Connection failed:', str(e))
```

Run it:
```bash
python test_supabase_python.py
```

---

## Step 6: Security Configuration

### 6.1 Row Level Security (RLS)
All tables have RLS policies already created in the schema. This means:
- Users can only see their own data
- Users cannot access other users' campaigns, transactions, etc.
- Enforced at the database level (more secure)

### 6.2 API Key Security
- **anon key**: Safe to expose (used in frontend) - only allows RLS-restricted access
- **service_role key**: Keep secret! (used in backend only) - has full database access

### 6.3 Best Practices
1. Never commit `.env` file to git
2. Use `.gitignore` to exclude it:
   ```
   .env
   .env.local
   .env.*.local
   ```
3. Use environment variables in production
4. Rotate keys regularly

---

## Step 7: Test End-to-End Flow

### 7.1 Create a Test User (Manual)
1. In Supabase dashboard, go to **Authentication** > **Users**
2. Click **Add user**
3. Enter:
   - Email: `test@example.com`
   - Password: `TestPassword123!`
4. Click **Create user**

### 7.2 Test Creating Data
1. Go to **Table Editor**
2. Click on `campaigns` table
3. Click **Insert row**
4. Fill in:
   - `user_id`: Copy the ID of the test user you created
   - `name`: "Test Campaign"
   - `platform`: "Instagram"
   - `status`: "draft"
5. Click **Save**

You should see the row inserted!

### 7.3 Verify RLS Works
1. Try to manually change the `user_id` to something else
2. Try to save - it should fail (because RLS prevents this)

---

## Troubleshooting

### Issue: "Cannot insert row"
**Solution:** Make sure you're setting a valid `user_id` (must match an existing user in `auth.users`)

### Issue: "Access denied" in Python/Node.js
**Solution:** 
- Check your API keys are correct
- Check your `.env` file is in the right directory
- Run `python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('SUPABASE_URL'))"`

### Issue: Tables not appearing
**Solution:**
- Refresh the page
- Check the SQL Editor for errors when you ran the schema
- Try running the schema again, one section at a time

### Issue: "Permission denied for schema public"
**Solution:** This usually means your service_role key has limited permissions. Use it only in the backend.

---

## Next Steps

Once you've completed this setup:

1. ✅ Supabase project created
2. ✅ Database schema deployed
3. ✅ Authentication configured
4. ✅ API keys saved in `.env`
5. ✅ Connection tested

**You're ready for Phase 2!** 

Next, we'll:
- Update `server.js` to use Supabase instead of in-memory storage
- Add authentication middleware to protect routes
- Update `ai_service.py` to store conversations in Supabase

---

## Quick Reference Commands

### Get your project status:
```bash
# Python - check connection
python -c "from supabase import create_client; import os; from dotenv import load_dotenv; load_dotenv(); print(create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_ANON_KEY')).table('user_profiles').select('*').limit(1).execute())"

# Node.js - check connection
node -e "require('dotenv').config(); const {createClient} = require('@supabase/supabase-js'); const s = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY); s.from('user_profiles').select('*').limit(1).then(r => console.log('✅ OK')).catch(e => console.log('❌', e.message))"
```

### View your API keys:
```bash
# From terminal
cat .env | grep SUPABASE
```

---

## Support & Resources

- **Supabase Docs:** https://supabase.com/docs
- **Database Queries:** https://supabase.com/docs/guides/database/overview
- **Authentication:** https://supabase.com/docs/guides/auth/overview
- **RLS Policies:** https://supabase.com/docs/guides/auth/row-level-security

---

**Ready?** Once you've completed all steps, let me know and we'll move to Phase 2!
