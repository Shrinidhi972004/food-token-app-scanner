# 🚀 EC2 Quick Deployment Guide

## Step 1: Launch EC2 Instance
1. Launch Ubuntu 22.04 LTS instance
2. Security group: Allow ports 22 (SSH), 80 (HTTP), 3000 (Node.js)
3. Connect via SSH

## Step 2: Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Git
sudo apt install git -y
```

## Step 3: Clone and Deploy
```bash
# Clone the repository
git clone https://github.com/Shrinidhi972004/food-token-app-scanner.git
cd food-token-app-scanner

# Create environment file
nano .env
# Add your email credentials:
# EMAIL_USER=your-email@gmail.com
# EMAIL_PASS=your-app-password

# Make scripts executable
chmod +x *.sh

# Run complete automated deployment
bash complete_docker_deploy.sh
```

## Step 4: Generate QR Codes and Database
```bash
# The automation script will:
# 1. Build Docker containers
# 2. Start services
# 3. Generate QR codes from CSV
# 4. Create database with all students
# 5. Start the web server

# Access your app at: http://your-ec2-ip:3000
```

## Step 5: Send Emails (Optional)
```bash
# After QR codes are generated, send emails:
docker-compose exec python python deploy_email_distribution.py
```

## 📊 What Will Be Generated
- **399 QR Codes** (JPEG format)
- **SQLite Database** with all student records
- **Web Scanner Interface** on port 3000
- **Admin Dashboard** for statistics

## 🔧 Manual Alternative
If Docker automation fails, use:
```bash
bash install.sh  # Manual setup
```

## 🌐 Access Points
- **Scanner**: `http://your-ec2-ip:3000`
- **Admin**: `http://your-ec2-ip:3000/admin`
- **QR Codes**: Available in `/qr_codes_jpeg/` directory

---
**Note**: Make sure to update your `.env` file with real email credentials before deployment!
