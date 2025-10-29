#!/usr/bin/env python3
"""
Test script to verify email configuration before sending to all students
"""
import os
from dotenv import load_dotenv
from send_qr_emails import EmailSender
import sqlite3

def test_email_configuration():
    """Test email configuration with sample data"""
    print("🔧 Testing Email Configuration...")
    
    # Load environment variables
    load_dotenv()
    
    # Check if required environment variables are set
    required_vars = ['EMAIL_USER', 'EMAIL_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please configure your .env file with email credentials")
        return False
    
    print(f"✅ Environment variables configured")
    print(f"📧 Email User: {os.getenv('EMAIL_USER')}")
    print(f"🏠 SMTP Host: {os.getenv('EMAIL_HOST', 'smtp.gmail.com')}")
    print(f"🔌 SMTP Port: {os.getenv('EMAIL_PORT', '587')}")
    
    # Initialize email sender
    try:
        email_sender = EmailSender()
        print("✅ Email sender initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize email sender: {e}")
        return False
    
    return email_sender

def test_send_sample_email(email_sender):
    """Send a test email to verify functionality"""
    
    test_email = input("Enter your email address to receive a test QR code: ").strip()
    if not test_email:
        print("❌ No email address provided")
        return False
    
    # Get a sample student from database for testing
    try:
        conn = sqlite3.connect('database/food_tokens.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, email, usn, class_name, food_preference, qr_code_path FROM users LIMIT 1')
        sample_student = cursor.fetchone()
        conn.close()
        
        if not sample_student:
            print("❌ No student data found in database")
            print("Please generate QR codes first using generate_qr_with_db.py")
            return False
        
        name, original_email, usn, class_name, food_preference, qr_code_path = sample_student
        
        print(f"📧 Sending test email to: {test_email}")
        print(f"🧑‍🎓 Using sample student data: {name} ({usn})")
        
        # Check if QR code file exists
        if not os.path.exists(qr_code_path):
            print(f"⚠️  QR code file not found: {qr_code_path}")
            print("Using alternative QR code file...")
            
            # Try to find any QR code file
            import glob
            qr_files = glob.glob("qr_codes_jpeg/*.jpg")
            if qr_files:
                qr_code_path = qr_files[0]
                print(f"📁 Using: {qr_code_path}")
            else:
                print("❌ No QR code files found. Please generate QR codes first.")
                return False
        
        # Send test email
        success = email_sender.send_email_with_qr(
            test_email,  # Send to test email instead of student's email
            name,
            class_name,
            usn,
            food_preference,
            qr_code_path
        )
        
        if success:
            print("✅ Test email sent successfully!")
            print(f"📧 Check your inbox at: {test_email}")
            print("💡 If you don't see the email, check your spam folder")
            return True
        else:
            print("❌ Failed to send test email")
            return False
            
    except Exception as e:
        print(f"❌ Error during test email: {e}")
        return False

def preview_email_template():
    """Show what the email template looks like"""
    print("\n📧 Email Template Preview:")
    print("=" * 50)
    print("Subject: Your Food Token QR Code - Sample Student")
    print("\nEmail Content:")
    print("- Professional HTML design")
    print("- Student details (Name, USN, Class, Food Preference)")
    print("- QR code attachment")
    print("- Usage instructions")
    print("- Backup USN option")
    print("- Visual food preference indicators")
    print("=" * 50)

def main():
    print("🧪 Email Configuration Test Tool")
    print("=" * 40)
    
    # Test email configuration
    email_sender = test_email_configuration()
    if not email_sender:
        print("\n❌ Email configuration test failed!")
        print("Please check your .env file and try again")
        return
    
    print("\n✅ Email configuration test passed!")
    
    # Show email template preview
    preview_email_template()
    
    # Ask if user wants to send test email
    send_test = input("\nDo you want to send a test email? (y/n): ").strip().lower()
    
    if send_test == 'y':
        success = test_send_sample_email(email_sender)
        if success:
            print("\n🎉 Email test completed successfully!")
            print("🚀 You can now use generate_qr_with_emails.py to send to all students")
        else:
            print("\n❌ Email test failed. Please check your configuration.")
    else:
        print("\n✅ Configuration test completed!")
        print("🚀 Email system is ready to use")
    
    print("\n📋 Next Steps:")
    print("1. To send QR codes to all students: python generate_qr_with_emails.py")
    print("2. To send emails separately: python send_qr_emails.py")
    print("3. For help: see EMAIL_SETUP_GUIDE.md")

if __name__ == "__main__":
    main()
