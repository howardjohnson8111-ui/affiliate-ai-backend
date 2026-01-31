# 🚀 Render Deployment Instructions

## **Step 1: Push to GitHub**

First, let's get your code on GitHub:

```bash
# If you haven't already, create a GitHub repository
# Go to https://github.com and create a new repository called "affiliate-ai-backend"

# Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/affiliate-ai-backend.git
git branch -M main
git push -u origin main
```

## **Step 2: Deploy to Render**

### **Option A: Quick Deploy (Recommended)**

1. **Go to [render.com](https://render.com)**
2. **Sign up** for a free account
3. **Click "New" → "Web Service"**
4. **Connect GitHub** and authorize access
5. **Select your repository**: `affiliate-ai-backend`
6. **Configure your service**:

```
Name: affiliate-ai-backend
Environment: Node
Region: Choose nearest to you
Branch: main
Runtime: Node
Build Command: npm install
Start Command: npm start
Instance Type: Free
```

7. **Add Environment Variables** (from `.env.production`):

```
NODE_ENV=production
PORT=3001
GOOGLE_API_KEY=your_actual_gemini_api_key
SUPABASE_URL=your_actual_supabase_url
SUPABASE_ANON_KEY=your_actual_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_actual_supabase_service_role_key
```

8. **Click "Create Web Service"**

### **Option B: Using Render CLI**

```bash
# Install Render CLI
npm install -g render

# Login
render login

# Deploy
render deploy
```

## **Step 3: Configure Environment Variables**

In your Render dashboard, go to your service → **Environment** and add these variables:

### **Required Variables:**
```
NODE_ENV=production
PORT=3001
GOOGLE_API_KEY=your_gemini_api_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
```

### **Optional Variables:**
```
PAYPAL_EMAIL=your-paypal-email@example.com
STOCK_API_KEY=your_stock_api_key
```

## **Step 4: Wait for Deployment**

Render will automatically:
- Build your application
- Install dependencies
- Start your server
- Provide a public URL

## **Step 5: Test Your Deployment**

Once deployed, you'll get a URL like:
`https://affiliate-ai-backend.onrender.com`

Test these endpoints:
- Health check: `https://your-app.onrender.com/api/health`
- Campaigns: `https://your-app.onrender.com/api/campaigns`

## **Step 6: Update Frontend**

Update your frontend to use the new backend URL:

```javascript
// In your frontend .env file
REACT_APP_API_URL=https://your-app.onrender.com
```

## **🎉 Success!**

Your app is now:
- ✅ Live on the internet
- ✅ Accessible from any device
- ✅ Secure with HTTPS
- ✅ Auto-deploying on git push

## **📱 Mobile Access**

Open your phone's browser and go to your Render URL. Your app will work perfectly on mobile devices!

## **💰 Cost**

- **Free tier**: Available (limited to 750 hours/month)
- **Paid tier**: $7/month for unlimited uptime

## **🔧 Troubleshooting**

If deployment fails:
1. Check the build logs in Render dashboard
2. Verify all environment variables are set
3. Make sure your `package.json` has the correct start script
4. Check that your server listens on the correct port (3001)

## **📞 Need Help?**

- Render docs: https://render.com/docs
- Support: support@render.com

---

**Ready to start?** Go to https://render.com and deploy your app! 🚀
