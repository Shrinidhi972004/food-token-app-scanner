# 🐳 Docker Deployment Guide - Food Token Scanner

## 🚀 One-Command Cloud Deployment

### **Quick Start (Recommended)**
```bash
# 1. Clone or upload your project to the cloud server
git clone <your-repo-url>
cd food-token-app-scanner

# 2. Configure your email credentials
cp .env.example .env
nano .env  # Edit with your email settings

# 3. Deploy with Docker Compose
docker-compose up -d

# That's it! Your app is running at http://localhost:3000
```

## 📋 Prerequisites

### **What you need on your cloud server:**
- **Docker** (20.x or higher)
- **Docker Compose** (2.x or higher)
- **2GB RAM minimum** (recommended for 500+ students)
- **10GB storage** (for QR codes and database)

### **Quick Docker Installation:**
```bash
# For Ubuntu/Debian
curl -fsSL https://get.docker.com | bash
sudo usermod -aG docker $USER
sudo systemctl enable docker
sudo systemctl start docker

# For CentOS/RHEL
sudo yum install -y docker docker-compose
sudo systemctl enable docker
sudo systemctl start docker

# Verify installation
docker --version
docker-compose --version
```

## 🔧 Configuration

### **1. Environment Variables (.env file)**
```bash
# Email Configuration (Required)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-16-char-app-password
EMAIL_FROM_NAME=College Food Token System
EMAIL_SUBJECT=Your Food Token QR Code

# Application Settings
NODE_ENV=production
PORT=3000

# Optional: Custom domain
# DOMAIN=your-domain.com
```

### **2. Docker Compose Override (Optional)**
Create `docker-compose.override.yml` for custom settings:
```yaml
version: '3.8'
services:
  food-token-scanner:
    ports:
      - "80:3000"  # Run on port 80
    environment:
      - DOMAIN=your-domain.com
```

## 🌐 Cloud Platform Specific Deployments

### **🔵 DigitalOcean Droplet**
```bash
# 1. Create Droplet (1GB RAM, Ubuntu 22.04)
# 2. SSH into droplet
ssh root@your-droplet-ip

# 3. Install Docker
curl -fsSL https://get.docker.com | bash

# 4. Clone and deploy
git clone <your-repo>
cd food-token-app-scanner
cp .env.example .env
nano .env  # Add your email credentials
docker-compose up -d

# 5. Configure firewall
ufw allow 22    # SSH
ufw allow 80    # HTTP
ufw allow 443   # HTTPS
ufw enable

# Your app is now live at: http://your-droplet-ip
```

### **🟠 AWS EC2**
```bash
# 1. Launch EC2 instance (t3.micro, Ubuntu 22.04)
# 2. Configure Security Groups:
#    - SSH (22) from your IP
#    - HTTP (80) from anywhere
#    - Custom TCP (3000) from anywhere

# 3. SSH and deploy
ssh -i your-key.pem ubuntu@your-ec2-ip
sudo apt update
curl -fsSL https://get.docker.com | bash
sudo usermod -aG docker ubuntu
newgrp docker

git clone <your-repo>
cd food-token-app-scanner
cp .env.example .env
nano .env
docker-compose up -d

# Access at: http://your-ec2-public-ip
```

### **🔴 Google Cloud Platform**
```bash
# 1. Create Compute Engine VM (e2-micro, Ubuntu 22.04)
# 2. Enable HTTP/HTTPS traffic in firewall rules

# 3. SSH and deploy
gcloud compute ssh your-vm-name
sudo apt update
curl -fsSL https://get.docker.com | bash
sudo usermod -aG docker $USER
newgrp docker

git clone <your-repo>
cd food-token-app-scanner
cp .env.example .env
nano .env
docker-compose up -d

# Access at: http://your-vm-external-ip
```

### **🟢 Linode**
```bash
# 1. Create Linode (Nanode 1GB, Ubuntu 22.04)
# 2. SSH and deploy
ssh root@your-linode-ip
apt update && apt upgrade -y
curl -fsSL https://get.docker.com | bash

git clone <your-repo>
cd food-token-app-scanner
cp .env.example .env
nano .env
docker-compose up -d

# Access at: http://your-linode-ip
```

## 📊 Management Commands

### **Start/Stop Application:**
```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart

# View logs
docker-compose logs -f
```

### **Generate QR Codes:**
```bash
# Option 1: Generate QR codes inside container
docker-compose exec food-token-scanner python3 generate_qr_with_db.py

# Option 2: Generate with email sending
docker-compose exec food-token-scanner python3 generate_qr_with_emails.py

# Option 3: Send emails to existing users
docker-compose exec food-token-scanner python3 deploy_email_distribution.py
```

### **Database Management:**
```bash
# Access database
docker-compose exec food-token-scanner sqlite3 database/food_tokens.db

# Backup database
docker cp food-token-scanner:/app/database/food_tokens.db ./backup_$(date +%Y%m%d).db

# View QR codes
docker-compose exec food-token-scanner ls -la qr_codes_jpeg/
```

### **Monitor Application:**
```bash
# Check container status
docker-compose ps

# View resource usage
docker stats food-token-scanner

# Check health
docker-compose exec food-token-scanner curl -f http://localhost:3000/
```

## 🔒 SSL/HTTPS Setup with Nginx

### **1. Create nginx.conf:**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### **2. Docker Compose with Nginx:**
```yaml
version: '3.8'
services:
  food-token-scanner:
    # ... existing config
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./ssl-certs:/etc/ssl/certs
    depends_on:
      - food-token-scanner
```

### **3. Get SSL Certificate:**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📈 Scaling for High Traffic

### **For 1000+ Students:**
```yaml
version: '3.8'
services:
  food-token-scanner:
    build: .
    deploy:
      replicas: 3
    environment:
      - NODE_ENV=production
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf
```

### **Load Balancer Config (nginx-lb.conf):**
```nginx
upstream food_scanner {
    server food-token-scanner_1:3000;
    server food-token-scanner_2:3000;
    server food-token-scanner_3:3000;
}

server {
    listen 80;
    location / {
        proxy_pass http://food_scanner;
    }
}
```

## 🔧 Troubleshooting

### **Common Issues:**

1. **Container won't start:**
   ```bash
   docker-compose logs food-token-scanner
   ```

2. **Email not working:**
   ```bash
   docker-compose exec food-token-scanner python3 test_email_config.py
   ```

3. **Database issues:**
   ```bash
   docker-compose exec food-token-scanner python3 test_database.py
   ```

4. **QR codes not generating:**
   ```bash
   docker-compose exec food-token-scanner ls -la qr_codes_jpeg/
   ```

5. **Port already in use:**
   ```bash
   # Change port in docker-compose.yml
   ports:
     - "8080:3000"  # Use port 8080 instead
   ```

## 🚀 Production Deployment Checklist

- [ ] Docker and Docker Compose installed
- [ ] `.env` file configured with email credentials
- [ ] CSV data file uploaded
- [ ] Firewall configured (ports 80, 443, 22)
- [ ] Domain name pointed to server (optional)
- [ ] SSL certificate configured (optional)
- [ ] Application started: `docker-compose up -d`
- [ ] QR codes generated
- [ ] Email system tested
- [ ] Scanner functionality verified
- [ ] Backup strategy configured

## 🎯 Quick Commands Reference

```bash
# Deploy everything
docker-compose up -d

# Generate QR codes
docker-compose exec food-token-scanner python3 generate_qr_with_db.py

# Send emails to all students
docker-compose exec food-token-scanner python3 deploy_email_distribution.py

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop application
docker-compose down

# Update application
git pull
docker-compose up -d --build
```

## 💡 Benefits of Docker Deployment

✅ **One-command deployment**  
✅ **Consistent environment across all cloud platforms**  
✅ **Easy scaling and load balancing**  
✅ **Automatic restarts on failure**  
✅ **Built-in health checks**  
✅ **Volume persistence for data**  
✅ **Easy backup and migration**  
✅ **No manual dependency installation**  

Your Food Token Scanner is now ready for production deployment with Docker! 🎉
