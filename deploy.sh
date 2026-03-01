#!/bin/bash

# Affiliate AI Pro - Deployment Script
# This script helps deploy your app to various cloud platforms

echo "🚀 Affiliate AI Pro - Cloud Deployment Script"
echo "=============================================="

# Check if required files exist
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Run this from the project root."
    exit 1
fi

if [ ! -f ".env.production" ]; then
    echo "❌ Error: .env.production not found. Please create it first."
    exit 1
fi

# Function to deploy to Vercel
deploy_to_vercel() {
    echo "📦 Deploying to Vercel..."
    
    # Check if Vercel CLI is installed
    if ! command -v vercel &> /dev/null; then
        echo "📥 Installing Vercel CLI..."
        npm install -g vercel
    fi
    
    # Deploy
    vercel --prod
    
    echo "✅ Vercel deployment complete!"
}

# Function to deploy to Render (manual setup)
deploy_to_render() {
    echo "📦 Preparing for Render deployment..."
    
    echo "📋 Steps to deploy to Render:"
    echo "1. Go to https://render.com"
    echo "2. Connect your GitHub repository"
    echo "3. Create a new Web Service"
    echo "4. Use these settings:"
    echo "   - Build Command: npm install"
    echo "   - Start Command: npm start"
    echo "   - Node Version: 18.x"
    echo "5. Add environment variables from .env.production"
    echo "6. Deploy! 🎉"
}

# Function to deploy to AWS EC2
deploy_to_aws() {
    echo "📦 Preparing for AWS EC2 deployment..."
    
    echo "📋 Steps to deploy to AWS EC2:"
    echo "1. Launch an EC2 instance (Ubuntu 20.04 recommended)"
    echo "2. SSH into your instance:"
    echo "   ssh -i your-key.pem ubuntu@your-ec2-ip"
    echo "3. Run these commands on the server:"
    echo "   sudo apt update && sudo apt upgrade -y"
    echo "   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -"
    echo "   sudo apt-get install -y nodejs git"
    echo "   git clone https://github.com/yourusername/affiliate-ai-backend.git"
    echo "   cd affiliate-ai-backend"
    echo "   npm install"
    echo "   npm install -g pm2"
    echo "   pm2 start server.js --name affiliate-ai-backend"
    echo "4. Set up environment variables on the server"
    echo "5. Configure security groups (ports 80, 443, 3001)"
    echo "6. Set up domain and SSL (optional)"
}

# Function to install production dependencies
install_production_deps() {
    echo "📦 Installing production dependencies..."
    
    # Install additional security and performance packages
    npm install helmet express-rate-limit compression morgan
    
    echo "✅ Production dependencies installed!"
}

# Function to create production startup script
create_startup_script() {
    echo "📝 Creating production startup script..."
    
    cat > start-production.sh << 'EOF'
#!/bin/bash

# Production startup script for Affiliate AI Pro
echo "🚀 Starting Affiliate AI Pro in Production Mode..."

# Load environment variables
if [ -f .env.production ]; then
    export $(cat .env.production | grep -v '^#' | xargs)
else
    echo "❌ Error: .env.production file not found!"
    exit 1
fi

# Check required environment variables
required_vars=("GOOGLE_API_KEY" "SUPABASE_URL" "SUPABASE_ANON_KEY")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Error: $var is not set!"
        exit 1
    fi
done

# Start the server
echo "✅ Environment variables validated!"
echo "🌐 Server starting on port ${PORT:-3001}"
NODE_ENV=production node server.js
EOF

    chmod +x start-production.sh
    echo "✅ Production startup script created!"
}

# Function to validate environment
validate_environment() {
    echo "🔍 Validating environment..."
    
    # Check if Node.js is installed
    if ! command -v node &> /dev/null; then
        echo "❌ Error: Node.js is not installed!"
        exit 1
    fi
    
    # Check Node.js version
    NODE_VERSION=$(node -v | cut -d'v' -f2)
    REQUIRED_VERSION="18.0.0"
    
    if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$NODE_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
        echo "❌ Error: Node.js version $NODE_VERSION is too old. Required: >= $REQUIRED_VERSION"
        exit 1
    fi
    
    echo "✅ Node.js version: $NODE_VERSION"
    
    # Check if npm is installed
    if ! command -v npm &> /dev/null; then
        echo "❌ Error: npm is not installed!"
        exit 1
    fi
    
    echo "✅ Environment validation complete!"
}

# Main menu
echo "Please choose your deployment option:"
echo "1) Vercel (Easiest - Free tier available)"
echo "2) Render (Recommended - Good balance)"
echo "3) AWS EC2 (Advanced - Full control)"
echo "4) Install production dependencies"
echo "5) Create production startup script"
echo "6) Validate environment"
echo "7) Exit"

read -p "Enter your choice (1-7): " choice

case $choice in
    1)
        deploy_to_vercel
        ;;
    2)
        deploy_to_render
        ;;
    3)
        deploy_to_aws
        ;;
    4)
        install_production_deps
        ;;
    5)
        create_startup_script
        ;;
    6)
        validate_environment
        ;;
    7)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice!"
        exit 1
        ;;
esac

echo "🎉 Deployment script completed!"
