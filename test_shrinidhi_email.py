#!/usr/bin/env python3
"""
Test email sending specifically for Shrinidhi Upadhyaya
"""
import os
from dotenv import load_dotenv
from send_qr_emails import EmailSender
import sqlite3

def test_shrinidhi_email():
    """Send test email specifically to Shrinidhi"""
    print("🧪 Testing email for Shrinidhi Upadhyaya...")
    
    # Load environment variables
    load_dotenv()
    
    # Initialize email sender
    try:
        email_sender = EmailSender()
        print("✅ Email sender initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize email sender: {e}")
        return False
    
    # Get Shrinidhi's data from database
    try:
        conn = sqlite3.connect('database/food_tokens.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, email, usn, class_name, food_preference, qr_code_path 
            FROM users 
            WHERE name LIKE "%shrinidhi%" OR name LIKE "%Shrinidhi%"
        ''')
        shrinidhi_data = cursor.fetchone()
        conn.close()
        
        if not shrinidhi_data:
            print("❌ Shrinidhi's data not found in database")
            return False
        
        name, email, usn, class_name, food_preference, qr_code_path = shrinidhi_data
        
        print(f"📋 Found Shrinidhi's data:")
        print(f"   Name: {name}")
        print(f"   Email: {email}")
        print(f"   USN: {usn}")
        print(f"   Class: {class_name}")
        print(f"   Food Preference: {food_preference}")
        print(f"   QR Code: {qr_code_path}")
        
        # Check if QR code file exists
        if not os.path.exists(qr_code_path):
            print(f"⚠️  QR code file not found: {qr_code_path}")
            # Try to find any QR code file for testing
            import glob
            qr_files = glob.glob("qr_codes_jpeg/Shrinidhi*.jpg")
            if qr_files:
                qr_code_path = qr_files[0]
                print(f"📁 Using alternative QR code: {qr_code_path}")
            else:
                print("❌ No QR code files found for Shrinidhi")
                return False
        
        # Ask for confirmation before sending
        confirm = input(f"\n📧 Send test email to {email}? (y/n): ").strip().lower()
        if confirm != 'y':
            print("❌ Email sending cancelled")
            return False
        
        print(f"\n📧 Sending test email to Shrinidhi...")
        print(f"   From: {os.getenv('EMAIL_USER')}")
        print(f"   To: {email}")
        print(f"   Subject: Your Food Token QR Code - {name}")
        
        # Send the email
        success = email_sender.send_email_with_qr(
            email,
            name,
            class_name,
            usn,
            food_preference,
            qr_code_path
        )
        
        if success:
            print("\n🎉 SUCCESS! Test email sent successfully!")
            print(f"✅ Email delivered to: {email}")
            print("📱 Check Shrinidhi's email inbox (and spam folder)")
            print("\n📧 Email contains:")
            print("   - Professional HTML design")
            print("   - Student details (Name, USN, Class, Food Preference)")
            print("   - QR code attachment")
            print("   - Usage instructions")
            print("   - Backup USN option")
            return True
        else:
            print("\n❌ FAILED! Test email could not be sent")
            print("💡 Check your email configuration in .env file")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

def main():
    print("🧪 SHRINIDHI EMAIL TEST")
    print("=" * 40)
    print("This will send a test email specifically to Shrinidhi Upadhyaya")
    print("to verify the email system works before sending to all students.")
    print()
    
    # Show current email configuration
    load_dotenv()
    print(f"📧 Email Configuration:")
    print(f"   SMTP Host: {os.getenv('EMAIL_HOST', 'Not set')}")
    print(f"   SMTP Port: {os.getenv('EMAIL_PORT', 'Not set')}")
    print(f"   Email User: {os.getenv('EMAIL_USER', 'Not set')}")
    print(f"   From Name: {os.getenv('EMAIL_FROM_NAME', 'Not set')}")
    print()
    
    success = test_shrinidhi_email()
    
    if success:
        print("\n🚀 EMAIL TEST COMPLETED SUCCESSFULLY!")
        print("💡 Ready to send emails to all students using:")
        print("   python generate_qr_with_emails.py")
        print("   or")
        print("   python send_qr_emails.py")
    else:
        print("\n❌ EMAIL TEST FAILED!")
        print("💡 Please check your configuration and try again")

if __name__ == "__main__":
    main()
