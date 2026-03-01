# Phase 1 Checklist - Supabase Setup

## Getting Started Checklist

### Account & Project Setup
- [ ] Create Supabase account at https://supabase.com
- [ ] Create new project named "affiliate-ai-pro"
- [ ] Wait for project initialization (2-3 minutes)
- [ ] Project is now active and ready

### API Keys & Environment
- [ ] Copy Project URL from Settings > API
- [ ] Copy anon key from Settings > API
- [ ] Copy service_role key from Settings > API
- [ ] Update `.env` file with all three values
- [ ] Test: `echo $env:SUPABASE_URL` in PowerShell

### Database Schema
- [ ] Open Supabase SQL Editor
- [ ] Copy all SQL from `SUPABASE_SCHEMA.sql`
- [ ] Paste into SQL Editor
- [ ] Click Run (no errors should appear)
- [ ] Verify in Table Editor: See 7 tables listed

### Authentication Setup
- [ ] Go to Authentication > Providers
- [ ] Enable Email provider
- [ ] Customize email templates (optional)
- [ ] Confirm auth is ready

### Connection Testing
- [ ] Install `@supabase/supabase-js` for Node: `npm install @supabase/supabase-js`
- [ ] Install `supabase-py` for Python: `pip install supabase`
- [ ] Test Node.js connection with test script
- [ ] Test Python connection with test script
- [ ] Both show "✅ Connection successful"

### Manual Testing
- [ ] Create test user in Authentication > Users
- [ ] Navigate to Table Editor > campaigns
- [ ] Insert a test row manually
- [ ] Verify RLS prevents unauthorized access
- [ ] Data persists after page refresh

### Documentation Review
- [ ] Read through `PHASE1_SUPABASE_SETUP.md`
- [ ] Understand RLS security policies
- [ ] Know how to access SQL Editor
- [ ] Understand table relationships

### Final Verification
- [ ] `.env` file contains SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY
- [ ] No errors in Supabase dashboard
- [ ] All 7 tables appear in Table Editor
- [ ] Test user exists in Authentication
- [ ] Both Node.js and Python can connect

---

## Files Created in This Phase

1. **supabase-client.js** - Node.js Supabase client wrapper
2. **supabase_manager.py** - Python Supabase manager class
3. **SUPABASE_SCHEMA.sql** - Complete database schema (7 tables, RLS policies, functions)
4. **PHASE1_SUPABASE_SETUP.md** - Detailed setup instructions
5. **.env.example** - Environment variables template

---

## Estimated Time

- Account setup: 5 minutes
- API keys: 2 minutes
- Database schema: 5 minutes
- Authentication: 3 minutes
- Testing: 10 minutes
- **Total: ~25 minutes**

---

## Troubleshooting Quick Links

| Issue | Solution |
|-------|----------|
| Tables not created | Check SQL Editor for errors, run schema again |
| Connection failed | Verify API keys in .env, reload page |
| Permission denied | Use anon key in frontend, service_role in backend |
| Can't create test user | Make sure email is unique |
| RLS preventing access | Normal - it's working! Only own data accessible |

---

## Next Phase

Once all checklist items are ✅, you're ready for:

**Phase 2: Backend Updates**
- Update `server.js` to use Supabase
- Add authentication middleware
- Remove in-memory storage
- Add user isolation to all endpoints

Estimated time: 3-4 hours

---

**Status:** ⏳ Waiting for your confirmation that Phase 1 is complete!
