# 🌐 Cloud Deployment - Replicate Local Development Workflow

## 🎯 **Your Plan: Run Same Commands on Cloud as Local**

This guide replicates **exactly** what you did locally, but on AWS EC2.

---

## **🖥️ What We Did Locally vs 🌐 What We'll Do on Cloud**

### **Local Workflow (What You Did):**
```bash
# Local machine commands:
cd food-token-app-scanner
source .venv/bin/activate
python clean_csv.py                    # Clean duplicates (406 → 399)
python generate_qr_with_db.py          # Generate QR codes (399 unique)
python test_shrinidhi_email.py         # Test email
python deploy_email_distribution.py    # Send to all (when ready)
npm start                              # Start server
```

### **Cloud Workflow (Same Commands):**
```bash
# AWS EC2 commands (identical process):
cd food-token-app-scanner
source .venv/bin/activate
python3 clean_csv.py                   # Clean duplicates (406 → 399)
python3 generate_qr_with_db.py         # Generate QR codes (399 unique)  
python3 test_shrinidhi_email.py        # Test email
python3 deploy_email_distribution.py   # Send to all (when ready)
npm start                              # Start server
```

**Only difference**: `python` → `python3` on cloud Linux

---

## **🚀 Step-by-Step AWS EC2 Setup (Manual Installation)**

### **Step 1: Launch EC2 Instance**
- **Instance Type**: t3.micro or t3.small
- **OS**: Ubuntu 22.04 LTS  
- **Storage**: 20GB SSD
- **Security Groups**: SSH (22), HTTP (80), Custom TCP (3000)

### **Step 2: Install Dependencies (Same as Local)**
```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js 18.x (same version as local)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Python 3.11 and pip (same as local)
sudo apt install -y python3.11 python3.11-venv python3-pip

# Install system dependencies for Pillow (image processing)
sudo apt install -y libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev

# Verify installations (same versions as local)
node --version
npm --version  
python3 --version
```

### **Step 3: Upload Your Project Files**
```bash
# Option A: Upload via SCP from your local machine
scp -i your-key.pem -r /path/to/food-token-app-scanner ubuntu@your-ec2-ip:~/

# Option B: Create directory and upload files manually
mkdir food-token-app-scanner
cd food-token-app-scanner
# Then upload files via SFTP or copy-paste
```

### **Step 4: Setup Environment (Identical to Local)**
```bash
cd food-token-app-scanner

# Install Node.js dependencies (same as local)
npm install

# Create Python virtual environment (same as local)
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies (same as local)
pip install qrcode[pil] pillow pandas python-dotenv numpy

# OR if you have requirements.txt:
pip install -r requirements.txt
```

### **Step 5: Configure Email (Same .env File)**
```bash
# Create .env file with same email credentials you used locally
nano .env

# Add same content as your local .env:
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=shrinidhiupadhyaya00@gmail.com
EMAIL_PASSWORD=fpvx lxkn isqu hrzq
EMAIL_FROM_NAME=Food Token System
EMAIL_SUBJECT=Your Food Token QR Code - College Food Counter
```

### **Step 6: Upload CSV Data**
```bash
# Upload your food_pref.csv file (same file you used locally)
# Via SCP: scp -i your-key.pem food_pref.csv ubuntu@your-ec2-ip:~/food-token-app-scanner/
```

---

## **🎯 Execute Same Workflow on Cloud**

### **Run Exact Same Commands as Local:**

```bash
# Activate Python environment (same as local)
cd food-token-app-scanner
source .venv/bin/activate

# Step 1: Clean CSV and remove duplicates (CRITICAL FIRST STEP)
python3 clean_csv.py
# Output: Creates food_pref_cleaned.csv (406 → 399 students)
# Removes: Timestamps, duplicates, cleans data format

# Step 2: Generate QR codes with cleaned database (same command)  
python3 generate_qr_with_db.py
# Output: Creates qr_codes_jpeg/ directory with 399 unique QR codes
# Uses: food_pref_cleaned.csv (not original food_pref.csv)

# Step 3: Test email with Shrinidhi (same command)
python3 test_shrinidhi_email.py
# Output: Sends test email to verify system works

# Step 4: Start the web server (same command)
npm start
# Output: Server running on http://your-ec2-ip:3000

# Step 5: Send emails to all students (when ready)
python3 deploy_email_distribution.py
# Output: Sends emails to all 399 students (no duplicates)
```

---

## **📱 Access Your Application**

### **Same URLs, Different IP:**
- **Local**: `http://localhost:3000`
- **Cloud**: `http://your-ec2-public-ip:3000`

### **Same Interfaces:**
- **Scanner**: `http://your-ec2-public-ip:3000/scanner`
- **Admin**: `http://your-ec2-public-ip:3000/admin`
- **Home**: `http://your-ec2-public-ip:3000`

---

## **🔧 Process Management on Cloud**

### **Keep Server Running (Unlike Local)**
```bash
# Option 1: Use screen to keep session alive
sudo apt install screen
screen -S food-scanner
npm start
# Press Ctrl+A, then D to detach
# Reconnect with: screen -r food-scanner

# Option 2: Use PM2 process manager
sudo npm install -g pm2
pm2 start server.js --name "food-token-scanner"
pm2 startup  # Set auto-start on reboot
pm2 save
```

### **Monitor and Manage:**
```bash
# Check server status
pm2 status

# View logs
pm2 logs food-token-scanner

# Restart server
pm2 restart food-token-scanner

# Stop server
pm2 stop food-token-scanner
```

---

## **📊 Comparison: Local vs Cloud**

| Aspect | Local Development | Cloud Production |
|--------|------------------|-----------------|
| **Commands** | `python` | `python3` |
| **Environment** | `.venv/bin/activate` | `.venv/bin/activate` |
| **Server** | `npm start` | `pm2 start server.js` |
| **Access** | `localhost:3000` | `ec2-ip:3000` |
| **Files** | Same directory | Same directory |
| **Database** | SQLite local | SQLite on EC2 |
| **Email** | Same config | Same config |

---

## **🎉 Result: Identical System on Cloud**

After following this guide, you'll have:

✅ **Same QR codes** generated on cloud (399 unique, no duplicates)  
✅ **Same database** with 399 students (duplicates removed)  
✅ **Same email system** working  
✅ **Same scanner interface**  
✅ **Same admin dashboard**  
✅ **24/7 availability** (unlike local)
✅ **Clean data** (406 → 399 students, timestamps removed)

**It's literally your local setup, just running on AWS EC2 instead!** 🚀

---

## **💡 Quick Setup Script**

Want to automate the setup? Here's a one-script solution:

```bash
#!/bin/bash
# Replicate local environment on EC2

# Install dependencies
sudo apt update && sudo apt upgrade -y
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs python3.11 python3.11-venv python3-pip
sudo apt install -y libjpeg-dev zlib1g-dev libfreetype6-dev

# Setup project (upload files first)
cd food-token-app-scanner
npm install
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run same workflow as local
python3 clean_csv.py                    # CRITICAL: Remove duplicates first
python3 generate_qr_with_db.py          # Generate from cleaned data
python3 test_shrinidhi_email.py         # Test email system

# Start server with PM2
sudo npm install -g pm2
pm2 start server.js --name "food-token-scanner"
pm2 startup
pm2 save

echo "🎉 Cloud deployment complete! Same as local setup."
echo "✅ Duplicates removed: 406 → 399 students"
echo "✅ QR codes generated: 399 unique codes"
echo "Access at: http://$(curl -s http://checkip.amazonaws.com/):3000"
```

Your plan is perfect - replicate the exact local workflow on cloud! 🎯
