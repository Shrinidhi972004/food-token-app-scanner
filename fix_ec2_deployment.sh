#!/bin/bash
# Quick fix for EC2 deployment issue

echo "🔧 EC2 DEPLOYMENT FIX"
echo "==================="
echo "Fixing the food_pref_cleaned.csv directory issue..."

# Remove the problematic directory if it exists
if [ -d "food_pref_cleaned.csv" ]; then
    echo "🗑️ Removing food_pref_cleaned.csv directory..."
    rm -rf food_pref_cleaned.csv
    echo "✅ Directory removed"
fi

# Also clean up any other potential issues
if [ -d "qr_codes_jpeg" ]; then
    echo "🧹 Cleaning QR codes directory..."
    rm -rf qr_codes_jpeg/*
    echo "✅ QR codes cleaned"
fi

if [ -f "database/food_tokens.db" ]; then
    echo "🗄️ Removing old database..."
    rm -f database/food_tokens.db
    echo "✅ Database removed"
fi

echo ""
echo "🚀 Now retry the deployment:"
echo "bash complete_docker_deploy.sh"
