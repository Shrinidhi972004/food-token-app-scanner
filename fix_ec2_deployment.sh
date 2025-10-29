#!/bin/bash
# Quick fix for EC2 deployment issue

echo "🔧 EC2 DEPLOYMENT FIX"
echo "==================="
echo "Fixing deployment issues..."

# Stop containers first
echo "🛑 Stopping Docker containers..."
docker-compose down

# Force remove any problematic directories (use privileged mode if needed)
echo "🗑️ Cleaning up conflicting files..."
sudo rm -rf food_pref_cleaned.csv 2>/dev/null || true
rm -f food_pref_cleaned_*.csv 2>/dev/null || true

# Clean QR codes and database
echo "🧹 Cleaning QR codes and database..."
rm -rf qr_codes_jpeg/* 2>/dev/null || true
rm -f database/food_tokens.db 2>/dev/null || true

# Make sure directories exist
mkdir -p qr_codes_jpeg
mkdir -p database

echo "✅ Cleanup complete!"
echo ""
echo "🚀 Now run the deployment again:"
echo "bash complete_docker_deploy.sh"
