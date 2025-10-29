#!/bin/bash
# 🚀 Complete AWS EC2 Docker Deployment Script
# Food Token Scanner - Production Ready

set -e  # Exit on any error

echo "🚀 AWS EC2 Docker Deployment - Food Token Scanner"
echo "================================================="
echo "This script will deploy your complete food token system"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Step 1: System Setup
print_info "Step 1: Setting up system and installing Docker..."
sudo apt update && sudo apt upgrade -y
curl -fsSL https://get.docker.com | bash
sudo usermod -aG docker $USER
print_step "Docker installed successfully"

# Step 2: Project Setup
print_info "Step 2: Setting up project..."
if [ ! -d "food-token-app-scanner" ]; then
    print_warning "Please upload your project files to this directory first"
    print_info "You can use: git clone <your-repo> or scp/sftp to upload files"
    exit 1
fi

cd food-token-app-scanner
print_step "Project directory found"

# Step 3: Environment Configuration
print_info "Step 3: Configuring environment..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_warning "Please edit .env file with your email credentials before continuing"
        print_info "Run: nano .env"
        read -p "Press Enter after configuring .env file..."
    else
        print_warning "Creating .env file template..."
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
        print_warning "Please edit .env file with your actual email credentials"
        print_info "Run: nano .env"
        exit 1
    fi
fi
print_step "Environment configured"

# Step 4: CSV Data Check
print_info "Step 4: Checking for CSV data..."
if [ ! -f "food_pref.csv" ] && [ ! -f "food_pref_cleaned.csv" ]; then
    print_warning "No CSV file found!"
    print_info "Please upload your Google Forms CSV file as 'food_pref.csv'"
    print_info "Expected columns: Enter Your Name, Enter Your College Mail ID, Enter Your USN, Class, What kind of food do you prefer"
    exit 1
fi
print_step "CSV data file found"

# Step 5: Deploy with Docker
print_info "Step 5: Deploying application with Docker..."
newgrp docker << 'DOCKER_COMMANDS'
docker-compose up -d
DOCKER_COMMANDS

# Wait for container to be ready
sleep 10
print_step "Application deployed successfully"

# Step 6: Data Processing Pipeline
print_info "Step 6: Processing student data..."

# Clean CSV and remove duplicates
print_info "6.1: Cleaning CSV and removing duplicates..."
docker-compose exec food-token-scanner python3 clean_csv.py
print_step "CSV cleaned and duplicates removed"

# Generate QR codes with cleaned data
print_info "6.2: Generating QR codes from cleaned data..."
docker-compose exec food-token-scanner python3 generate_qr_with_db.py
print_step "QR codes generated successfully"

# Test email configuration
print_info "6.3: Testing email configuration..."
docker-compose exec food-token-scanner python3 test_email_config.py
print_step "Email system tested"

# Step 7: Final Setup
print_info "Step 7: Final setup and verification..."

# Check application status
APP_STATUS=$(docker-compose ps --filter "name=food-token-scanner" --format "table {{.Status}}")
if [[ $APP_STATUS == *"Up"* ]]; then
    print_step "Application is running successfully"
else
    print_warning "Application may have issues. Check logs with: docker-compose logs"
fi

# Get public IP
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com/)
print_step "Deployment completed!"

echo ""
echo "🎉 DEPLOYMENT SUCCESSFUL!"
echo "========================"
print_info "Application URL: http://$PUBLIC_IP:3000"
print_info "Scanner Interface: http://$PUBLIC_IP:3000/scanner"
print_info "Admin Dashboard: http://$PUBLIC_IP:3000/admin"

echo ""
echo "📋 NEXT STEPS:"
echo "=============="
print_info "1. Test the scanner interface in your browser"
print_info "2. Send emails to all students:"
echo "   docker-compose exec food-token-scanner python3 deploy_email_distribution.py"
print_info "3. Monitor application:"
echo "   docker-compose logs -f"
print_info "4. Check container status:"
echo "   docker-compose ps"

echo ""
echo "🔧 MANAGEMENT COMMANDS:"
echo "======================"
echo "View logs:           docker-compose logs -f"
echo "Restart app:         docker-compose restart"
echo "Stop app:           docker-compose down"
echo "Generate QR codes:   docker-compose exec food-token-scanner python3 generate_qr_with_db.py"
echo "Send emails:         docker-compose exec food-token-scanner python3 deploy_email_distribution.py"
echo "Clean CSV:           docker-compose exec food-token-scanner python3 clean_csv.py"

echo ""
print_step "AWS EC2 deployment completed successfully! 🚀"
