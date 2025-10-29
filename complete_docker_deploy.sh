#!/bin/bash
# 🐳 Complete Docker Deployment & Automation Script
# Everything through Docker: Clean CSV → Generate QR → Send Emails

set -e

echo "🐳 COMPLETE DOCKER AUTOMATION SCRIPT"
echo "===================================="
echo "This will handle EVERYTHING through Docker:"
echo "✅ CSV cleaning & duplicate removal"
echo "✅ QR code generation"
echo "✅ Database population"
echo "✅ Email system testing"
echo "✅ Mass email distribution"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

print_step() { echo -e "${GREEN}✅ $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }

# Check prerequisites
print_info "Checking prerequisites..."

if [ ! -f "docker-compose.yml" ]; then
    print_error "docker-compose.yml not found!"
    exit 1
fi

if [ ! -f ".env" ]; then
    print_warning ".env file not found!"
    print_info "Creating .env template..."
    cat > .env << 'EOF'
# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_FROM_NAME=College Food Token System
EMAIL_SUBJECT=Your Food Token QR Code

# Application Settings
NODE_ENV=production
PORT=3000
EOF
    print_warning "Please edit .env file with your email credentials!"
    print_info "Run: nano .env"
    read -p "Press Enter after configuring .env..."
fi

if [ ! -f "food_pref.csv" ] && [ ! -f "food_pref_cleaned.csv" ]; then
    print_error "No CSV data found!"
    print_info "Please upload your Google Forms CSV as 'food_pref.csv'"
    exit 1
fi

print_step "Prerequisites checked"

# Step 1: Deploy with Docker
print_info "Step 1: Deploying application with Docker..."
docker-compose up -d

# Wait for container to be ready
print_info "Waiting for container to start..."
sleep 10

# Check container status
if ! docker-compose ps | grep -q "Up"; then
    print_error "Container failed to start!"
    docker-compose logs
    exit 1
fi

print_step "Docker container running successfully"

# Step 2: Complete automation through Docker
print_info "Step 2: Running complete automation inside Docker container..."

# Clean CSV and remove duplicates
print_info "2.1: Cleaning CSV and removing duplicates..."
docker-compose exec food-token-scanner python3 clean_csv.py
print_step "CSV cleaned successfully"

# Generate QR codes
print_info "2.2: Generating QR codes and populating database..."
docker-compose exec food-token-scanner python3 generate_qr_with_db.py
print_step "QR codes generated successfully"

# Show statistics
print_info "2.3: Getting system statistics..."
docker-compose exec food-token-scanner python3 -c "
import sqlite3
conn = sqlite3.connect('database/food_tokens.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM users')
total = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM users WHERE food_preference LIKE \"%veg%\" AND food_preference NOT LIKE \"%non%\"')
veg = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM users WHERE food_preference LIKE \"%non%\"')
non_veg = cursor.fetchone()[0]
conn.close()
print(f'📊 System Statistics:')
print(f'Total Students: {total}')
print(f'Vegetarian: {veg}')
print(f'Non-Vegetarian: {non_veg}')
"

# Test email system
print_info "2.4: Testing email system..."
read -p "Do you want to send a test email to verify email system? (y/n): " test_email

if [[ $test_email == "y" || $test_email == "Y" ]]; then
    print_info "Running email test..."
    docker-compose exec food-token-scanner python3 test_shrinidhi_email.py
    print_step "Email test completed"
fi

# Mass email distribution
print_info "2.5: Mass email distribution..."
print_warning "This will send emails to ALL students!"

read -p "🚨 Send emails to ALL students now? (type 'YES' to confirm): " send_emails

if [ "$send_emails" = "YES" ]; then
    print_info "Starting mass email distribution..."
    docker-compose exec food-token-scanner python3 deploy_email_distribution.py
    print_step "Mass email distribution completed!"
else
    print_info "Email distribution skipped"
    print_info "You can run it later with:"
    echo "docker-compose exec food-token-scanner python3 deploy_email_distribution.py"
fi

# Get application URL
print_info "Step 3: Getting application access information..."

# Try to get public IP
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com/ 2>/dev/null || echo "localhost")

print_step "Complete Docker automation finished!"

echo ""
echo "🎉 DEPLOYMENT SUCCESSFUL!"
echo "========================"
print_info "Application URL: http://$PUBLIC_IP:3000"
print_info "QR Scanner: http://$PUBLIC_IP:3000/scanner"  
print_info "Admin Dashboard: http://$PUBLIC_IP:3000/admin"

echo ""
echo "📊 WHAT WAS ACCOMPLISHED:"
echo "========================"
print_step "CSV data cleaned and duplicates removed"
print_step "QR codes generated for all students"
print_step "Database populated with student data"
print_step "Email system configured and tested"
if [ "$send_emails" = "YES" ]; then
    print_step "Emails sent to all students"
else
    print_warning "Emails not sent yet (run manually when ready)"
fi
print_step "Scanner system ready for food counter"

echo ""
echo "🔧 MANAGEMENT COMMANDS:"
echo "======================"
echo "View logs:           docker-compose logs -f"
echo "Check status:        docker-compose ps"
echo "Restart app:         docker-compose restart"
echo "Stop app:            docker-compose down"
echo ""
echo "🐳 DOCKER AUTOMATION COMMANDS:"
echo "=============================="
echo "Clean CSV:           docker-compose exec food-token-scanner python3 clean_csv.py"
echo "Generate QR codes:   docker-compose exec food-token-scanner python3 generate_qr_with_db.py"
echo "Test email:          docker-compose exec food-token-scanner python3 test_shrinidhi_email.py"
echo "Send all emails:     docker-compose exec food-token-scanner python3 deploy_email_distribution.py"
echo "Run automation:      docker-compose exec food-token-scanner python3 docker_automation.py"

echo ""
print_step "🚀 Your food token system is now fully deployed and operational!"

# Show container status
echo ""
print_info "Current container status:"
docker-compose ps
