# Email Setup Guide for QR Code Distribution

## 📧 Email Configuration Setup

### Step 1: Configure Gmail App Password (Recommended)

1. **Enable 2-Factor Authentication on Gmail:**
   - Go to [Google Account Settings](https://myaccount.google.com/)
   - Navigate to Security → 2-Step Verification
   - Enable if not already enabled

2. **Generate App Password:**
   - Go to Security → App passwords
   - Select "Mail" and "Other (custom name)"
   - Enter "Food Token System"
   - Copy the generated 16-character password

3. **Update .env file:**
   ```bash
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASSWORD=your-16-char-app-password
   EMAIL_FROM_NAME=College Food Token System
   EMAIL_SUBJECT=Your Food Token QR Code - College Cafeteria
   ```

### Step 2: Alternative Email Providers

#### Yahoo Mail
```bash
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USER=your-email@yahoo.com
EMAIL_PASSWORD=your-app-password
```

#### Outlook/Hotmail
```bash
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USER=your-email@outlook.com
EMAIL_PASSWORD=your-password
```

#### Custom SMTP Server
```bash
EMAIL_HOST=your-smtp-server.com
EMAIL_PORT=587
EMAIL_USER=your-email@domain.com
EMAIL_PASSWORD=your-password
```

## 🚀 Usage Instructions

### Option 1: Generate QR codes WITH automatic email sending
```bash
# Configure .env file first, then run:
python generate_qr_with_emails.py
```

### Option 2: Generate QR codes, then send emails separately
```bash
# Generate QR codes first
python generate_qr_with_db.py

# Then send emails to all students
python send_qr_emails.py
```

### Option 3: Send emails to specific students
```python
# Edit send_qr_emails.py to add email filtering
# Example: Only send to specific class or email pattern
```

## 📋 Email Template Features

The automatic email includes:
- **Professional HTML design** with college branding
- **Student details** (Name, USN, Class, Food Preference)
- **QR code attachment** (high-quality JPEG)
- **Usage instructions** for students
- **Backup USN option** if scanner fails
- **Visual food preference indicators** (Veg/Non-Veg colors)

## 🔧 Troubleshooting

### Common Issues:

1. **"Authentication failed"**
   - Ensure 2FA is enabled on Gmail
   - Use App Password, not regular password
   - Check EMAIL_USER and EMAIL_PASSWORD in .env

2. **"Connection refused"**
   - Check EMAIL_HOST and EMAIL_PORT
   - Ensure internet connection
   - Try different SMTP server

3. **"File not found" for QR codes**
   - Ensure QR codes are generated first
   - Check qr_codes_jpeg/ directory exists
   - Run generate_qr_with_db.py before sending emails

4. **Emails going to spam**
   - Use proper FROM name
   - Don't send too many emails too quickly
   - Add delay between emails (already implemented)

### Testing Email Configuration:
```python
# Test email sending with a single email
from send_qr_emails import EmailSender
sender = EmailSender()
# This will validate your email configuration
```

## 📊 Monitoring

The system provides real-time feedback:
- ✅ Email sent successfully
- ❌ Email failed with error message
- 📊 Success rate statistics
- ⏳ Progress tracking

## 🔒 Security Notes

1. **Never commit .env file to git**
2. **Use App Passwords, not account passwords**
3. **Limit email sending rate** (1-2 seconds delay between emails)
4. **Monitor for bounced emails**
5. **Keep email credentials secure**

## 📈 Scaling for Large Numbers

For 500+ students:
- Use professional email service (SendGrid, Mailgun)
- Implement retry logic for failed emails
- Add email queue system
- Monitor delivery rates
- Consider bulk email limits

## 🎯 Next Steps

After email setup:
1. Test with a few sample emails first
2. Generate and send QR codes to all students
3. Monitor email delivery
4. Handle any bounced emails
5. Set up the scanning system at food counter
