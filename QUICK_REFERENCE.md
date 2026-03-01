# 🚀 Affiliate AI Pro - Quick Reference Guide

## TL;DR - Get Started in 30 Seconds

```bash
# 1. Set API Key
$env:GOOGLE_API_KEY='your-api-key-here'

# 2. Start Node backend
node server.js

# 3. Start Python service
python ai_service.py

# 4. Start using it!
[You]: Create a new Instagram campaign called My Campaign
```

---

## The 6 Personas At a Glance

| Persona | Emoji | Best For | Example Command |
|---------|-------|----------|-----------------|
| Campaign Manager | 🎯 | Marketing campaigns | "Create an Instagram campaign" |
| Stock Analyst | 📈 | Stock/investments | "Log my Apple stock purchase" |
| Learning Manager | 🎓 | Education/skills | "Update my course progress" |
| Financial Assistant | 💰 | Transactions | "Log a $500 affiliate payout" |
| App Customizer | ⚙️ | Settings | "Set theme to dark mode" |
| Language Assistant | 🌍 | Translation | "Translate to Spanish" |

---

## How to Invoke

### Explicit (Recommended for complex requests)
```
"Campaign Manager, create a new Facebook ad campaign"
"Stock Analyst, show my portfolio value"
"Language Assistant, translate this to French"
```

### Implicit (Natural language)
```
"Create a new Instagram campaign"           → Campaign Manager
"Log a $500 affiliate payout"               → Financial Assistant
"What languages do you support?"            → Language Assistant
```

---

## Key Features

✅ **Intelligent Detection** - Automatically routes to best persona  
✅ **Tool Calling** - Executes real actions on your backend  
✅ **Multi-language** - Supports 65+ languages  
✅ **Context Aware** - Understands your business domain  
✅ **Conversational** - Natural back-and-forth dialogue  
✅ **Actionable** - Provides clear next steps  

---

## Commands by Persona

### 🎯 Campaign Manager
```
"Create a new Instagram campaign called Summer Sale"
"Show me details of campaign ID 12345"
"Update my Facebook campaign to active status"
"Delete my old Twitter campaign"
```

### 📈 Stock Analyst
```
"Log my purchase of 10 AAPL shares at $150 each"
"What's my current stock portfolio?"
"Update my MSFT holdings to 20 shares"
"Record a $25 dividend from Microsoft"
```

### 🎓 Learning Manager
```
"Create a learning module for Advanced Python"
"Update my AI Tools course to 75% progress"
"Mark my Web Development course as completed"
"Show my learning progress on all courses"
```

### 💰 Financial Assistant
```
"Log an affiliate payout of $500 via PayPal"
"Record a $1000 bank deposit"
"Log a $25 dividend from Microsoft"
"Record my stock purchase expense of $1500"
```

### ⚙️ App Customizer
```
"Set my theme to dark mode"
"Change my default view to Stock dashboard"
"Enable notifications for transactions"
"Set my preferred currency to EUR"
```

### 🌍 Language Assistant
```
"Translate 'Hello world' to Spanish"
"Set my app language to French"
"Generate a campaign description in German"
"What languages do you support?"
```

---

## System Architecture

```
Your Command (Natural Language)
        ↓
Persona Detection System
        ↓
Route to Appropriate Persona
        ↓
Get Persona-Specific Tools
        ↓
Send to Gemini with System Instruction
        ↓
Gemini Decides Which Tool(s) to Use
        ↓
Execute Tool(s) on Backend
        ↓
Return Results to Gemini
        ↓
Gemini Generates Response
        ↓
Display to User
```

---

## API Endpoints Available

### Campaign Routes
```
POST   /api/campaigns       - Create campaign
GET    /api/campaigns       - Get all campaigns
GET    /api/campaigns/:id   - Get specific campaign
PUT    /api/campaigns/:id   - Update campaign
DELETE /api/campaigns/:id   - Delete campaign
```

### Transaction Routes
```
POST   /api/transactions    - Create transaction
GET    /api/transactions    - Get all transactions
```

### Health Check
```
GET    /api/health          - Check if server is running
```

---

## Troubleshooting

### "GOOGLE_API_KEY environment variable is not set!"
```powershell
$env:GOOGLE_API_KEY='your-api-key-here'
```

### "Port 3001 already in use"
```powershell
Get-Process | Where-Object {$_.ProcessName -like "*node*"} | Stop-Process -Force
node server.js
```

### "Connection refused"
Make sure Node.js server is running on port 3001

### "Persona not detected correctly"
Try explicitly naming the persona: "Hey Campaign Manager, ..."

---

## Performance Tips

1. **Keep requests focused** - One action per request is better
2. **Use explicit personas** for complex multi-step tasks
3. **Provide context** - More details = better results
4. **Check responses** - The AI summarizes what it did

---

## Supported Languages

**European:** English, Spanish, French, German, Italian, Portuguese, Dutch, Polish, Russian, Swedish, Danish, Norwegian, Finnish, Greek, Czech, Hungarian, Romanian, Bulgarian, Croatian, Serbian, Ukrainian

**Asian:** Chinese (Mandarin), Japanese, Korean, Hindi, Thai, Vietnamese, Indonesian, Burmese, Filipino, Mongolian, Bengali, Tamil, Telugu, Kannada, Malayalam

**Middle East/Africa:** Arabic, Hebrew, Persian, Urdu, Afrikaans

**And 20+ more languages!**

---

## File Structure

```
Gemini_api_backend/
├── ai_service.py              # Main AI service (this is where the magic happens!)
├── server.js                  # Node.js backend API
├── package.json               # Node dependencies
├── demo_personas.py           # Persona detection demo
├── test_transaction.py        # Test script for transactions
├── SYSTEM_DOCUMENTATION.md    # Full documentation
└── QUICK_REFERENCE.md         # This file!
```

---

## What's Next?

### Phase 1: Complete ✅
- Multi-persona system
- Natural language understanding
- Tool calling
- Campaign management
- Transaction logging

### Phase 2: In Progress 🔄
- Stock market tracking
- Learning modules
- App customizer
- Full language support

### Phase 3: Coming Soon 🚀
- Progressive Web App (PWA) frontend
- Supabase database integration
- Mobile app versions
- Advanced analytics
- Cloud deployment

---

## Success Metrics

You'll know it's working when:

1. ✅ Can start ai_service.py without errors
2. ✅ Can create a campaign with natural language
3. ✅ Can log transactions automatically
4. ✅ Persona detection is accurate
5. ✅ Get helpful summaries of actions

---

## Remember

- **Be natural** - Type like you're talking to a person
- **Be specific** - More details = better results
- **Iterate** - You can follow up and refine
- **Explore** - Try different personas and requests
- **Have fun** - This is a powerful tool!

---

## Questions?

Check these files:
- `SYSTEM_DOCUMENTATION.md` - Comprehensive guide
- `demo_personas.py` - See how persona detection works
- `ai_service.py` - Source code and implementation
- Error messages in terminal - Usually clear and actionable

---

**You're ready to go! 🚀 Start with:**
```
python ai_service.py
```

Then try:
```
Create a new Instagram campaign called Test
```

Enjoy! 🎉
