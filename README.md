# 🍽️ Food Token Scanner System

A complete web-based QR code food token management system for college food distribution. This system allows you to generate unique QR codes for students from Google Forms data and scan them at the food counter with automatic validation.

## 📋 Features

- **📊 CSV Data Processing**: Import student data from Google Forms CSV
- **🎯 QR Code Generation**: Generate unique JPEG QR codes for each student
- **� Automatic Email Distribution**: Send QR codes directly to students' email addresses
- **�📱 Automatic QR Scanning**: Camera-based QR code detection with instant validation
- **🆔 USN Support**: Manual entry using University Seat Number (USN) as backup
- **🔒 One-Time Use**: Prevents duplicate token usage
- **🥗 Food Preference Tracking**: Supports vegetarian and non-vegetarian options
- **📈 Admin Dashboard**: Real-time statistics and user management
- **🎨 Responsive Design**: Works on desktop, tablet, and mobile devices
- **📧 Professional Email Templates**: HTML emails with student details and instructions
- **🐳 Docker Support**: Easy containerized deployment

## 🛠️ Requirements

- **Node.js** (v14 or higher)
- **Python** (v3.7 or higher)
- **npm** (comes with Node.js)
- **Camera-enabled device** for scanning

## 🚀 Quick Start

### 1. Setup Project

```bash
# Clone or download the project
cd food-token-app-scanner

# Install Node.js dependencies
npm install

# Create Python virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install Python dependencies
pip install qrcode[pil] pillow pandas python-dotenv
```

### 2. Configure Email System (Optional)

For automatic email distribution, configure your email settings:

```bash
# Copy and edit the email configuration
cp .env.example .env

# Edit .env file with your email credentials:
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_FROM_NAME=College Food Token System
```

**📧 Email Setup Guide**: See `EMAIL_SETUP_GUIDE.md` for detailed instructions.

### 3. Prepare Your Data

1. **Export Google Forms data** as CSV
2. **Clean your data** (remove duplicates and unwanted columns):
   ```bash
   # Activate Python environment first
   source .venv/bin/activate
   
   # Clean your CSV file
   python clean_csv.py
   ```
3. **Your cleaned CSV** will be saved as `food_pref_cleaned.csv`

**Expected CSV format:**
- `Enter Your Name`
- `Enter Your College Mail ID`
- `Enter Your USN`
- `Class`
- `What kind of food do you prefer`

### 4. Generate QR Codes

**Option A: Generate QR codes WITH automatic email sending**
```bash
# Make sure Python virtual environment is activated
source .venv/bin/activate

# Generate QR codes and send emails automatically
python generate_qr_with_emails.py
```

**Option B: Generate QR codes first, send emails later**
```bash
# Generate QR codes only
python generate_qr_with_db.py

# Send emails separately (optional)
python send_qr_emails.py
```

**Option C: Test email configuration first**
```bash
# Test your email setup before sending to all students
python test_email_config.py
```

This will:
- ✅ Create `qr_codes_jpeg/` directory with individual QR code images
- ✅ Set up SQLite database with student data
- ✅ Send professional HTML emails with QR codes (if email is configured)
- ✅ Provide real-time progress and email delivery status
- ✅ Generate `tokens_list.json` with all token information
- ✅ Prevent duplicate generation on subsequent runs

### 5. Start the Application

```bash
# Start the Node.js server
npm start
```

The server will start on `http://localhost:3000`

### 5. Access the Interfaces

- **🏠 Home Page**: `http://localhost:3000`
- **📱 QR Scanner**: `http://localhost:3000/scanner`
- **⚙️ Admin Dashboard**: `http://localhost:3000/admin`

## 📱 How to Use

### For Students:
1. **Receive your QR code** (JPEG file sent via email/messaging)
2. **Show QR code** to camera at food counter
3. **Automatic validation** - no button clicks needed!

### For Food Counter Staff:
1. **Open scanner page** on any device with camera
2. **Allow camera permissions** when prompted
3. **Point camera at student's QR code** for automatic detection
4. **Alternative: Manual USN Entry**
   - If camera doesn't work or QR code is damaged
   - Enter student's USN (e.g., `ABOOBAKKARDS22`) in the manual entry field
   - Click "Validate Entry" button
5. **View student details** instantly:
   - Name, USN, and class
   - Food preference (Veg/Non-Veg)
   - Validation status
6. **One-time use** - used tokens cannot be scanned again

### For Administrators:
1. **Access admin dashboard** for statistics
2. **View scan history** and student data
3. **Monitor real-time usage** statistics

## 📁 Project Structure

```
food-token-app-scanner/
├── 📄 server.js                 # Main Express.js server
├── 📄 database.js               # SQLite database management
├── 📄 package.json              # Node.js dependencies
├── 🐳 Dockerfile                # Docker container setup
├── 🐳 docker-compose.yml        # Docker Compose configuration
├── 🐍 generate_qr_with_db.py    # Basic QR code generation script
├── 🐍 generate_qr_with_emails.py # QR generation WITH email sending
├── 📧 send_qr_emails.py         # Standalone email sending script
├── � test_email_config.py      # Email configuration testing
├── �🧹 clean_csv.py              # CSV data cleaning utility
├── 🧹 cleanup_duplicates.py     # Cleanup utility
├── 🧪 test_database.py          # Database testing utility
├── � EMAIL_SETUP_GUIDE.md      # Detailed email setup instructions
├── 🔐 .env                      # Email configuration (create this)
├── �📂 public/                   # Frontend files
│   ├── 📄 index.html            # Home page
│   ├── 📄 admin.html            # Admin dashboard
│   └── 📄 scanner.html          # QR scanner interface
├── 📂 database/                 # SQLite database files
├── 📂 qr_codes_jpeg/            # Generated QR code images
└── 📂 uploads/                  # CSV upload directory
```

## � Email Distribution Features

### Professional Email Templates
- **HTML Design**: Clean, professional college-branded emails
- **Student Details**: Name, USN, Class, Food Preference displayed clearly
- **Visual Indicators**: Color-coded food preferences (Green=Veg, Red=Non-Veg)
- **Instructions**: Clear usage instructions for students
- **Backup Option**: USN manual entry instructions included

### Email System Features
- **QR Code Attachment**: High-quality JPEG QR codes attached to emails
- **Real-time Progress**: Live feedback during email sending process
- **Error Handling**: Graceful handling of failed email deliveries
- **Rate Limiting**: Built-in delays to prevent overwhelming email servers
- **Success Tracking**: Detailed statistics on email delivery success rates

### Supported Email Providers
- **Gmail**: Recommended (with App Passwords)
- **Yahoo Mail**: Supported
- **Outlook/Hotmail**: Supported
- **Custom SMTP**: Any SMTP server supported

### Email Automation Options
1. **During QR Generation**: Automatic email sending as QR codes are created
2. **Batch Sending**: Send all emails after QR generation is complete
3. **Selective Sending**: Send emails to specific students or classes
4. **Retry Failed**: Re-attempt failed email deliveries

## �🔧 Configuration

### Database Settings
- **Database Type**: SQLite
- **Location**: `database/food_tokens.db`
- **Auto-created**: Yes, on first run

### QR Code Settings
- **Format**: JPEG
- **Size**: 600x700 pixels
- **Quality**: 95%
- **Includes**: Student name, class, food preference, college branding

### Email Settings (Optional)
- **SMTP Support**: TLS/SSL encrypted connections
- **File Attachments**: QR codes attached as JPEG files
- **Template System**: Customizable HTML email templates
- **Delivery Tracking**: Success/failure monitoring

### Scanner Settings
- **Auto-detection**: Enabled
- **Scan cooldown**: 3 seconds
- **Camera selection**: Automatic (prefers back camera)
- **Scan area**: 300x300 pixels

## 🐳 Docker Deployment

### Option 1: Docker Compose (Recommended)
```bash
# Build and start containers
docker-compose up -d

# Access application at http://localhost:3000
```

### Option 2: Manual Docker Build
```bash
# Build Docker image
docker build -t food-token-scanner .

# Run container
docker run -p 3000:3000 -v $(pwd)/database:/app/database food-token-scanner
```

## 🛟 Troubleshooting

### Common Issues

**1. Camera not working:**
- Ensure HTTPS connection (required for camera access)
- Check browser permissions for camera
- Try different browsers (Chrome, Firefox, Safari)

**2. QR codes not generating:**
- Check CSV file format and location
- Ensure Python virtual environment is activated
- Verify all required Python packages are installed

**3. Manual USN entry not working:**
- Ensure USN format is correct (e.g., `ABOOBAKKARDS22`)
- Check if USN exists in database
- Try uppercase format

**4. Database errors:**
- Delete `database/food_tokens.db` and regenerate
- Check file permissions in database directory

**4. Duplicate QR codes:**
- Run cleanup script: `python cleanup_duplicates.py`
- Or delete `qr_codes_jpeg/` folder and regenerate

### Useful Commands

```bash
# Test database status
python test_database.py

# Clean up duplicates
python cleanup_duplicates.py

# Check Node.js server logs
npm start

# Reset everything (start fresh)
rm -rf qr_codes_jpeg/ database/
python generate_qr_with_db.py
```

## � Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    food_preference TEXT CHECK(food_preference IN ('veg', 'non-veg')),
    token TEXT UNIQUE NOT NULL,
    qr_code_path TEXT,
    is_scanned BOOLEAN DEFAULT 0,
    scanned_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    class_name TEXT,
    usn TEXT
);
```

### Scan History Table
```sql
CREATE TABLE scan_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    scanned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    scanner_info TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

## 🔒 Security Features

- **Unique tokens**: UUID-based token generation
- **One-time use**: Database validation prevents reuse
- **Server-side validation**: All QR code validation happens on server
- **SQL injection protection**: Parameterized queries
- **XSS protection**: Input sanitization

## � Performance

- **Supports**: 1000+ students
- **Scan speed**: Instant detection (< 1 second)
- **Database**: SQLite (suitable for small-medium deployments)
- **Concurrent users**: 50+ simultaneous scanners

## 🤝 Support

### For Issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Check server logs for error messages

### File Locations:
- **QR Codes**: `qr_codes_jpeg/` directory
- **Database**: `database/food_tokens.db`
- **Logs**: Console output from `npm start`

## 📝 License

This project is developed for educational purposes at Sahyadri College of Engineering & Management.

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Install dependencies | `npm install` |
| Generate QR codes | `python generate_qr_with_db.py` |
| Start server | `npm start` |
| Access scanner | `http://localhost:3000/scanner` |
| Access admin | `http://localhost:3000/admin` |
| Test database | `python test_database.py` |
| Clean duplicates | `python cleanup_duplicates.py` |

**🎉 Your Food Token Scanner System is ready to use!**

### Installation

1. **Clone or download the project**
   ```bash
   cd food-token-app-scanner
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the server**
   ```bash
   npm start
   ```

4. **Access the application**
   - Main page: http://localhost:3000
   - Admin Dashboard: http://localhost:3000/admin
   - Scanner Interface: http://localhost:3000/scanner

## 📋 Usage Guide

### Step 1: Create Google Form

Create a Google Form with the following fields:
- **Name** (required)
- **Email** (optional)
- **Phone** (optional)
- **Food Preference** (required: "Veg" or "Non-Veg")

### Step 2: Export and Upload Data

1. Go to Google Forms responses
2. Click the Google Sheets icon to create a spreadsheet
3. Download the spreadsheet as CSV
4. Upload the CSV file in the Admin Dashboard

### Step 3: Generate QR Codes

1. After uploading CSV, click "Generate QR Codes" in Admin Dashboard
2. Download the QR codes ZIP file
3. Extract and distribute individual QR codes to participants

### Step 4: Scan Tokens

1. Open the Scanner Interface on a mobile device or computer with camera
2. Grant camera permissions
3. Scan participant QR codes at the food counter
4. View participant details and food preference
5. System prevents reuse of scanned tokens

### Step 5: Monitor Progress

- View real-time statistics in Admin Dashboard
- Track total users, scanned count, and food preferences
- Monitor scanning progress and distribution

## 📁 File Structure

```
food-token-app-scanner/
├── public/                 # Frontend files
│   ├── index.html         # Main landing page
│   ├── admin.html         # Admin dashboard
│   └── scanner.html       # QR code scanner
├── uploads/               # Uploaded CSV files (temporary)
├── qr-codes/             # Generated QR code images
├── database/             # SQLite database files
├── server.js             # Main server application
├── database.js           # Database management
├── package.json          # Project dependencies
└── README.md             # This file
```

## 🔧 API Endpoints

### File Upload
- `POST /api/upload-csv` - Upload and process Google Forms CSV

### QR Code Management
- `POST /api/generate-qr-codes` - Generate QR codes for all users
- `GET /api/download-qr-codes` - Download all QR codes as ZIP

### Scanning
- `POST /api/scan` - Process QR code scan and validate token

### Data Management
- `GET /api/users` - Get all users
- `GET /api/stats` - Get scanning statistics
- `DELETE /api/clear-data` - Clear all data (admin only)

## 📊 Database Schema

### Users Table
- `id` - Primary key
- `name` - Participant name
- `email` - Email address (optional)
- `phone` - Phone number (optional)
- `food_preference` - 'veg' or 'non-veg'
- `token` - Unique UUID token
- `qr_code_path` - Path to QR code image
- `is_scanned` - Boolean scan status
- `scanned_at` - Scan timestamp
- `created_at` - Creation timestamp

### Scan History Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `scanned_at` - Scan timestamp
- `scanner_info` - Additional scan information

## 🔒 Security Features

- **One-time Use**: Each token can only be scanned once
- **Unique Tokens**: UUID-based token generation
- **Scan Validation**: Server-side validation prevents tampering
- **Audit Trail**: Complete scan history tracking

## 📱 Mobile Compatibility

- Responsive design works on all screen sizes
- Camera access for QR code scanning
- Touch-friendly interface
- Offline-capable after initial load

## 🛠️ Troubleshooting

### Camera Not Working
- Ensure HTTPS connection (required for camera access)
- Grant camera permissions in browser
- Try different browsers (Chrome, Firefox, Safari)

### CSV Upload Issues
- Ensure CSV has proper column headers
- Check for special characters in data
- Verify food preference values ("Veg" or "Non-Veg")

### QR Code Scanning Problems
- Ensure good lighting
- Hold device steady
- Try manual token entry if camera fails

## 🔄 Development

### Development Mode
```bash
npm run dev
```

### Environment Variables
Create a `.env` file for configuration:
```
PORT=3000
NODE_ENV=development
```

## 📈 Analytics

The system provides comprehensive analytics:
- Total registered users
- Scan completion rate
- Food preference distribution
- Real-time scanning progress
- Historical scan data

## 🚨 Important Notes

1. **Backup Data**: Regularly backup the SQLite database
2. **HTTPS Required**: Camera access requires HTTPS in production
3. **QR Code Distribution**: Ensure QR codes are sent to correct participants
4. **Network**: Scanner interface requires internet connection for validation

## 📞 Support

For technical support or feature requests:
1. Check the troubleshooting section
2. Review browser console for errors
3. Verify network connectivity
4. Ensure proper CSV format

## 🎯 Best Practices

1. **Test First**: Always test with a small group before full deployment
2. **Clear Instructions**: Provide clear instructions to participants
3. **Backup Strategy**: Implement regular database backups
4. **Monitor Usage**: Keep track of scanning progress during events
5. **Security**: Clear sensitive data after events if required

---

**Version**: 1.0.0  
**Author**: Your Name  
**License**: MIT
