#!/bin/bash
# 🚀 Food Token Scanner - Cloud Installation Script
# Usage: bash install.sh

set -e  # Exit on any error

echo "🚀 Food Token Scanner System - Cloud Installation"
echo "================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if [ -f /etc/debian_version ]; then
        OS="debian"
        print_info "Detected Debian/Ubuntu system"
    elif [ -f /etc/redhat-release ]; then
        OS="redhat"
        print_info "Detected RedHat/CentOS system"
    else
        print_error "Unsupported Linux distribution"
        exit 1
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    print_info "Detected macOS system"
else
    print_error "Unsupported operating system: $OSTYPE"
    exit 1
fi

# Update system packages
print_info "Updating system packages..."
if [[ "$OS" == "debian" ]]; then
    sudo apt update && sudo apt upgrade -y
    print_status "System packages updated"
elif [[ "$OS" == "redhat" ]]; then
    sudo yum update -y
    print_status "System packages updated"
elif [[ "$OS" == "macos" ]]; then
    print_info "Please ensure Homebrew is installed and up to date"
fi

# Install Node.js
print_info "Installing Node.js 18.x..."
if [[ "$OS" == "debian" ]]; then
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
elif [[ "$OS" == "redhat" ]]; then
    curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
    sudo yum install -y nodejs
elif [[ "$OS" == "macos" ]]; then
    if command -v brew &> /dev/null; then
        brew install node@18
    else
        print_error "Homebrew not found. Please install Node.js manually"
        exit 1
    fi
fi

# Verify Node.js installation
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_status "Node.js installed: $NODE_VERSION"
else
    print_error "Node.js installation failed"
    exit 1
fi

# Install Python 3.11
print_info "Installing Python 3.11..."
if [[ "$OS" == "debian" ]]; then
    sudo apt install -y python3.11 python3.11-venv python3-pip python3.11-dev
elif [[ "$OS" == "redhat" ]]; then
    sudo yum install -y python3.11 python3.11-venv python3-pip python3.11-devel
elif [[ "$OS" == "macos" ]]; then
    if command -v brew &> /dev/null; then
        brew install python@3.11
    else
        print_error "Homebrew not found. Please install Python manually"
        exit 1
    fi
fi

# Verify Python installation
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_status "Python installed: $PYTHON_VERSION"
else
    print_error "Python installation failed"
    exit 1
fi

# Install system dependencies for Pillow (image processing)
print_info "Installing system dependencies for image processing..."
if [[ "$OS" == "debian" ]]; then
    sudo apt install -y libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk
elif [[ "$OS" == "redhat" ]]; then
    sudo yum install -y libjpeg-devel zlib-devel freetype-devel lcms2-devel libwebp-devel tcl-devel tk-devel
elif [[ "$OS" == "macos" ]]; then
    if command -v brew &> /dev/null; then
        brew install libjpeg zlib freetype libpng
    fi
fi
print_status "System dependencies installed"

# Install PM2 for process management (optional but recommended)
print_info "Installing PM2 process manager..."
sudo npm install -g pm2
print_status "PM2 installed globally"

# Create project directory
PROJECT_DIR="food-token-app-scanner"
if [ -d "$PROJECT_DIR" ]; then
    print_warning "Project directory already exists"
    read -p "Do you want to remove it and start fresh? (y/N): " -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$PROJECT_DIR"
        print_info "Removed existing project directory"
    else
        print_info "Using existing project directory"
    fi
fi

# If project doesn't exist, create it
if [ ! -d "$PROJECT_DIR" ]; then
    mkdir -p "$PROJECT_DIR"
    print_status "Created project directory: $PROJECT_DIR"
fi

cd "$PROJECT_DIR"

# Create necessary directories
print_info "Creating project structure..."
mkdir -p database qr_codes_jpeg uploads logs public
print_status "Project directories created"

# Install Node.js dependencies
if [ -f "package.json" ]; then
    print_info "Installing Node.js dependencies..."
    npm install
    print_status "Node.js dependencies installed"
else
    print_warning "package.json not found. Please add your project files."
fi

# Create Python virtual environment
print_info "Creating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate
print_status "Python virtual environment created"

# Install Python dependencies
if [ -f "requirements.txt" ]; then
    print_info "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    print_status "Python dependencies installed"
else
    print_warning "requirements.txt not found. Installing basic dependencies..."
    pip install qrcode[pil] pillow pandas python-dotenv numpy
    print_status "Basic Python dependencies installed"
fi

# Create environment file template
if [ ! -f ".env" ]; then
    print_info "Creating environment configuration template..."
    cat > .env << EOF
# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_FROM_NAME=College Food Token System
EMAIL_SUBJECT=Your Food Token QR Code - College Cafeteria

# Application Settings
NODE_ENV=production
PORT=3000
EOF
    print_status "Environment template created (.env)"
    print_warning "Please edit .env file with your actual email credentials"
fi

# Set proper permissions
print_info "Setting file permissions..."
chmod 755 database qr_codes_jpeg uploads logs
if [ -f "server.js" ]; then
    chmod 644 *.js *.json *.md 2>/dev/null || true
fi
print_status "File permissions set"

# Create startup script
print_info "Creating startup script..."
cat > start.sh << 'EOF'
#!/bin/bash
# Food Token Scanner Startup Script

# Activate Python virtual environment
source .venv/bin/activate

# Start the application with PM2
pm2 start server.js --name "food-token-scanner" --watch --ignore-watch="database qr_codes_jpeg uploads logs"

echo "🚀 Food Token Scanner started!"
echo "📱 Access at: http://localhost:3000"
echo "📊 PM2 status: pm2 status"
echo "📋 View logs: pm2 logs food-token-scanner"
EOF

chmod +x start.sh
print_status "Startup script created (start.sh)"

# Create stop script
cat > stop.sh << 'EOF'
#!/bin/bash
# Food Token Scanner Stop Script

pm2 stop food-token-scanner
pm2 delete food-token-scanner

echo "🛑 Food Token Scanner stopped!"
EOF

chmod +x stop.sh
print_status "Stop script created (stop.sh)"

# Final instructions
echo ""
echo "🎉 Installation completed successfully!"
echo "======================================"
print_status "Node.js $(node --version) installed"
print_status "Python $(python3 --version | cut -d' ' -f2) installed"
print_status "PM2 process manager installed"
print_status "Project structure created"
print_status "Dependencies installed"

echo ""
echo "📋 Next Steps:"
echo "=============="
print_info "1. Add your project files to: $(pwd)"
print_info "2. Edit .env file with your email credentials"
print_info "3. Add your CSV data file"
print_info "4. Start the application: ./start.sh"
print_info "5. Access the scanner: http://localhost:3000"

echo ""
echo "🔧 Common Commands:"
echo "=================="
echo "  Start app:     ./start.sh"
echo "  Stop app:      ./stop.sh"
echo "  View logs:     pm2 logs food-token-scanner"
echo "  Check status:  pm2 status"
echo "  Restart:       pm2 restart food-token-scanner"

echo ""
print_info "Installation log saved to: install.log"
echo "📖 For detailed deployment guide, see: CLOUD_DEPLOYMENT_GUIDE.md"
