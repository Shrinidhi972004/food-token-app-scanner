# 🚀 Cloud Deployment Guide for Food Token Scanner System

## 📋 System Requirements

### **Python Requirements (requirements.txt)**
```bash
pip install -r requirements.txt
```

**Core Dependencies:**
- `qrcode[pil]==7.4.2` - QR code generation
- `Pillow==10.0.1` - Image processing for QR codes
- `pandas==2.1.4` - CSV data processing
- `numpy==1.24.4` - Data manipulation
- `python-dotenv==1.0.0` - Environment variable management

### **Node.js Requirements (package.json)**
```bash
npm install
```

**Core Dependencies:**
- `express==^4.18.2` - Web server framework
- `sqlite3==^5.1.6` - Database management
- `multer==^1.4.5-lts.1` - File upload handling
- `csv-parser==^3.0.0` - CSV data parsing
- `qrcode==^1.5.3` - QR code utilities
- `uuid==^9.0.1` - Unique ID generation
- `cors==^2.8.5` - Cross-origin resource sharing

## 🌐 Cloud Platform Deployment

### **1. AWS EC2 Deployment**

#### **Instance Requirements:**
- **Instance Type**: t3.micro or t3.small (1-2 vCPU, 1-2GB RAM)
- **Storage**: 10-20GB SSD
- **OS**: Ubuntu 22.04 LTS or Amazon Linux 2023
- **Security Group**: Allow ports 22 (SSH), 80 (HTTP), 443 (HTTPS), 3000 (App)

#### **Installation Commands:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Python 3.11 and pip
sudo apt install -y python3.11 python3.11-venv python3-pip

# Install system dependencies for Pillow
sudo apt install -y libjpeg-dev zlib1g-dev libfreetype6-dev

# Clone your project
git clone <your-repo-url>
cd food-token-app-scanner

# Install Node.js dependencies
npm install

# Create Python virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your email credentials

# Start application
npm start
```

### **2. Google Cloud Platform (GCP) Deployment**

#### **Compute Engine Instance:**
- **Machine Type**: e2-micro or e2-small
- **Boot Disk**: Ubuntu 22.04 LTS, 20GB SSD
- **Firewall**: Allow HTTP/HTTPS traffic

#### **App Engine Deployment (app.yaml):**
```yaml
runtime: nodejs18

env_variables:
  NODE_ENV: production
  EMAIL_HOST: smtp.gmail.com
  EMAIL_PORT: 587
  EMAIL_USER: your-email@gmail.com
  EMAIL_PASSWORD: your-app-password

automatic_scaling:
  min_instances: 1
  max_instances: 3
  target_cpu_utilization: 0.8

resources:
  cpu: 1
  memory_gb: 1
  disk_size_gb: 10
```

### **3. Microsoft Azure Deployment**

#### **Azure App Service:**
- **Runtime Stack**: Node.js 18 LTS
- **Operating System**: Linux
- **Pricing Tier**: Basic B1 or Standard S1

#### **Configuration:**
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login and deploy
az login
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name food-token-scanner --runtime "NODE|18-lts"
az webapp config appsettings set --resource-group myResourceGroup --name food-token-scanner --settings EMAIL_HOST=smtp.gmail.com EMAIL_PORT=587
```

### **4. DigitalOcean Droplet**

#### **Droplet Specs:**
- **Size**: Basic 1GB RAM, 1 vCPU, 25GB SSD
- **Image**: Ubuntu 22.04 x64
- **Features**: Enable monitoring and backups

#### **Setup Script:**
```bash
#!/bin/bash
# DigitalOcean deployment script

# Update system
apt update && apt upgrade -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

# Install Python and dependencies
apt install -y python3.11 python3.11-venv python3-pip
apt install -y libjpeg-dev zlib1g-dev libfreetype6-dev

# Install PM2 for process management
npm install -g pm2

# Clone and setup project
git clone <your-repo-url>
cd food-token-app-scanner
npm install
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure PM2
pm2 start server.js --name "food-token-scanner"
pm2 startup
pm2 save
```

### **5. Heroku Deployment**

#### **Required Files:**

**Procfile:**
```
web: node server.js
```

**package.json engines:**
```json
{
  "engines": {
    "node": "18.x",
    "npm": "9.x"
  }
}
```

#### **Deployment Commands:**
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create food-token-scanner-app

# Set environment variables
heroku config:set EMAIL_HOST=smtp.gmail.com
heroku config:set EMAIL_PORT=587
heroku config:set EMAIL_USER=your-email@gmail.com
heroku config:set EMAIL_PASSWORD=your-app-password

# Deploy
git push heroku main
```

## 🔧 Environment Configuration

### **Required Environment Variables (.env)**
```bash
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

# Optional: Database URL (if using external database)
# DATABASE_URL=sqlite:///app/database/food_tokens.db
```

### **Production Environment Setup Script:**
```bash
#!/bin/bash
# production-setup.sh

echo "🚀 Setting up Food Token Scanner for Production"

# Create necessary directories
mkdir -p database qr_codes_jpeg uploads logs

# Set proper permissions
chmod 755 database qr_codes_jpeg uploads
chmod 644 *.js *.json *.md

# Install production dependencies only
npm ci --only=production

# Activate Python environment and install requirements
source .venv/bin/activate
pip install --no-cache-dir -r requirements.txt

# Generate initial QR codes if CSV exists
if [ -f "food_pref_cleaned.csv" ]; then
    echo "📊 Generating QR codes from CSV..."
    python generate_qr_with_db.py
fi

echo "✅ Production setup complete!"
echo "🔧 Configure your .env file with email credentials"
echo "🚀 Start with: npm start"
```

## 📊 Resource Requirements

### **Minimum Requirements:**
- **CPU**: 1 vCPU
- **RAM**: 1GB
- **Storage**: 10GB SSD
- **Bandwidth**: 1TB/month

### **Recommended for 500+ Students:**
- **CPU**: 2 vCPU
- **RAM**: 2GB
- **Storage**: 20GB SSD
- **Bandwidth**: 2TB/month

### **Storage Breakdown:**
- **Application Code**: ~50MB
- **Node.js Dependencies**: ~200MB
- **Python Dependencies**: ~150MB
- **Database**: ~5MB (for 500 students)
- **QR Code Images**: ~200MB (500 × 400KB each)
- **Logs and Temp Files**: ~100MB

## 🔒 Security Considerations

### **SSL/HTTPS Setup:**
```bash
# Install Certbot for Let's Encrypt
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### **Firewall Configuration:**
```bash
# UFW setup
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 3000/tcp  # Application (if needed)
sudo ufw enable
```

### **Nginx Reverse Proxy (Optional):**
```nginx
# /etc/nginx/sites-available/food-token-scanner
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📝 Deployment Checklist

- [ ] Install Node.js 18.x
- [ ] Install Python 3.11+
- [ ] Install system dependencies (libjpeg-dev, zlib1g-dev)
- [ ] Clone repository
- [ ] Install Node.js dependencies (`npm install`)
- [ ] Create Python virtual environment
- [ ] Install Python requirements (`pip install -r requirements.txt`)
- [ ] Configure environment variables (.env)
- [ ] Set up SSL certificates
- [ ] Configure firewall rules
- [ ] Test email functionality
- [ ] Generate QR codes
- [ ] Start application
- [ ] Set up monitoring and logging
- [ ] Configure backups
- [ ] Test scanner functionality

## 🎯 Post-Deployment Steps

1. **Test the complete flow:**
   - Upload CSV → Generate QR codes → Send emails → Scan QR codes

2. **Monitor logs:**
   ```bash
   # Application logs
   tail -f logs/app.log
   
   # PM2 logs (if using PM2)
   pm2 logs food-token-scanner
   ```

3. **Set up monitoring:**
   - Use tools like New Relic, DataDog, or built-in cloud monitoring
   - Monitor CPU, memory, disk usage, and response times

4. **Backup strategy:**
   - Database backups (daily)
   - QR code image backups
   - Configuration file backups

Your food token scanner system is now ready for cloud deployment! 🚀
