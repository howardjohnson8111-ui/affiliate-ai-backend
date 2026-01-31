#!/bin/bash

# GitHub Setup Script for Affiliate AI Pro
echo "🔗 Setting up GitHub connection..."

# Get GitHub username
read -p "Enter your GitHub username: " USERNAME

# Add remote origin
echo "📡 Adding GitHub remote..."
git remote add origin https://github.com/$USERNAME/affiliate-ai-backend.git

# Push to GitHub
echo "📤 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo "✅ Code pushed to GitHub!"
echo "🌐 Your repository: https://github.com/$USERNAME/affiliate-ai-backend"
