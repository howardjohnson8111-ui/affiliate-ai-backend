# Affiliate AI Pro - Cloud Deployment Guide

## 🚀 Cloud Hosting Options

### **Recommended Options (Easiest to Hardest):**

#### 1. **Vercel** (Recommended for Beginners)
- **Pros**: Free tier, automatic SSL, easy deployment, Git integration
- **Cons**: Limited to Node.js/Python, less control
- **Cost**: Free for hobby projects
- **Best for**: Quick deployment, prototypes

#### 2. **Render** (Recommended Balance)
- **Pros**: Free tier, supports databases, easy deployment
- **Cons**: Limited free tier resources
- **Cost**: Free tier + $7/month for web services
- **Best for**: Production apps with database

#### 3. **AWS EC2** (Most Flexible)
- **Pros**: Full control, scalable, reliable
- **Cons**: Complex setup, requires server management
- **Cost**: ~$10-50/month depending on instance
- **Best for**: Production, scalable apps

#### 4. **DigitalOcean** (Good Balance)
- **Pros**: Simple, affordable, good documentation
- **Cons**: Manual setup required
- **Cost**: ~$5-20/month
- **Best for**: Small to medium apps

---

## 📋 Deployment Steps

### **Step 1: Choose Your Hosting Provider**

#### Option A: Vercel (Easiest)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod

# Follow prompts to connect your Git repository
```

#### Option B: Render (Recommended)
1. Go to [render.com](https://render.com)
2. Connect your GitHub repository
3. Create a "Web Service"
4. Set build command: `npm install`
5. Set start command: `npm start`
6. Add environment variables from `.env.production`

#### Option C: AWS EC2 (Advanced)
```bash
# Connect to your EC2 instance
ssh -i your-key.pem ec2-user@your-ec2-ip

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Clone your repository
git clone https://github.com/yourusername/affiliate-ai-backend.git
cd affiliate-ai-backend

# Install dependencies
npm install

# Set up PM2 for process management
npm install -g pm2
pm2 start server.js --name "affiliate-ai-backend"
pm2 startup
pm2 save
```

---

### **Step 2: Configure Environment Variables**

Copy the production environment variables to your hosting provider:

**Required Variables:**
- `GOOGLE_API_KEY`
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `NODE_ENV=production`
- `PORT=3001`

**For Production:**
- `PAYPAL_EMAIL`
- `PAYPAL_CLIENT_ID`
- `PAYPAL_SECRET`
- `STOCK_API_KEY`

---

### **Step 3: Set Up Supabase for Production**

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Get your production URL and keys
4. Update your environment variables
5. Run the database schema from `SUPABASE_SCHEMA.sql`

---

### **Step 4: Update Frontend Configuration**

Update your frontend to point to the new backend URL:

```javascript
// In your frontend .env file
REACT_APP_API_URL=https://your-backend-domain.com
```

---

### **Step 5: SSL/HTTPS Setup**

Most cloud providers handle this automatically:
- **Vercel/Render**: Automatic SSL
- **AWS EC2**: Use Let's Encrypt with Certbot
- **DigitalOcean**: Use Let's Encrypt

---

## 🔧 Production Server Configuration

### **Enhanced server.js for Production:**

```javascript
// Add these security middlewares in production
if (process.env.NODE_ENV === 'production') {
  app.use(helmet()); // Security headers
  app.use(compression()); // Compress responses
  app.use(morgan('combined')); // Request logging
  
  // Rate limiting
  const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100 // limit each IP to 100 requests per windowMs
  });
  app.use('/api/', limiter);
}
```

---

## 📱 Mobile Access

Once deployed, your app will be accessible from any device:

1. **Phone/Tablet**: Open browser and go to your domain
2. **Desktop**: Same URL works on any computer
3. **PWA**: Can be installed as a mobile app

**Example URLs:**
- Backend: `https://your-backend-domain.com`
- Frontend: `https://your-frontend-domain.com`
- API: `https://your-backend-domain.com/api`

---

## 🛠️ Troubleshooting

### **Common Issues:**

1. **CORS Errors**: Update `ALLOWED_ORIGINS` in environment
2. **Database Connection**: Check Supabase URL and keys
3. **API Keys**: Ensure all required keys are set
4. **Port Issues**: Use port 3001 or provider's default

### **Monitoring:**

```bash
# Check logs (PM2)
pm2 logs affiliate-ai-backend

# Check status
pm2 status

# Restart if needed
pm2 restart affiliate-ai-backend
```

---

## 💰 Cost Estimates

| Provider | Free Tier | Paid Tier | Monthly Cost |
|----------|-----------|-----------|--------------|
| Vercel | Yes | Pro | $0-20 |
| Render | Yes | Standard | $0-7 |
| AWS EC2 | No | t2.micro | $10-15 |
| DigitalOcean | No | Basic | $5-10 |

---

## 🚀 Quick Start Recommendation

**For immediate deployment**: Use **Render** - it's the best balance of ease and features.

**For learning**: Use **AWS EC2** - you'll learn valuable cloud skills.

**For speed**: Use **Vercel** - fastest deployment time.

---

## 📞 Next Steps

1. Choose your hosting provider
2. Set up your account
3. Deploy using the steps above
4. Test your app from mobile devices
5. Set up domain name (optional)

Need help with any specific provider? Let me know which one you choose!
