import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import sqlite3
import pandas as pd
from pathlib import Path
import time

# Load environment variables
load_dotenv()

class EmailSender:
    def __init__(self):
        self.email_host = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
        self.email_port = int(os.getenv('EMAIL_PORT', '587'))
        self.email_user = os.getenv('EMAIL_USER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.email_from_name = os.getenv('EMAIL_FROM_NAME', 'Food Token System')
        self.email_subject = os.getenv('EMAIL_SUBJECT', 'Your Food Token QR Code')
        
        if not self.email_user or not self.email_password:
            raise ValueError("Please set EMAIL_USER and EMAIL_PASSWORD in .env file")
    
    def create_email_content(self, student_name, class_name, usn, food_preference):
        """Create HTML email content"""
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #2c3e50; margin: 0;">🍽️ Food Token QR Code</h1>
                    <p style="color: #7f8c8d; margin: 10px 0 0 0;">College Food Counter System</p>
                </div>
                
                <div style="background-color: #ecf0f1; padding: 20px; border-radius: 8px; margin-bottom: 25px;">
                    <h2 style="color: #34495e; margin: 0 0 15px 0;">Dear {student_name},</h2>
                    <p style="color: #2c3e50; line-height: 1.6; margin: 0;">
                        Your food token QR code has been generated successfully! Please find your personalized QR code attached to this email.
                    </p>
                </div>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 25px;">
                    <h3 style="color: #2c3e50; margin: 0 0 15px 0;">📋 Your Details:</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr style="border-bottom: 1px solid #dee2e6;">
                            <td style="padding: 8px; font-weight: bold; color: #495057;">Name:</td>
                            <td style="padding: 8px; color: #212529;">{student_name}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #dee2e6;">
                            <td style="padding: 8px; font-weight: bold; color: #495057;">USN:</td>
                            <td style="padding: 8px; color: #212529;">{usn}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #dee2e6;">
                            <td style="padding: 8px; font-weight: bold; color: #495057;">Class:</td>
                            <td style="padding: 8px; color: #212529;">{class_name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; font-weight: bold; color: #495057;">Food Preference:</td>
                            <td style="padding: 8px; color: #212529;">
                                <span style="background-color: {'#27ae60' if food_preference == 'Veg' else '#e74c3c'}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">
                                    {food_preference}
                                </span>
                            </td>
                        </tr>
                    </table>
                </div>
                
                <div style="background-color: #e8f5e8; border-left: 4px solid #27ae60; padding: 15px; margin-bottom: 25px;">
                    <h3 style="color: #27ae60; margin: 0 0 10px 0;">📱 How to use your QR Code:</h3>
                    <ol style="color: #2c3e50; line-height: 1.6; margin: 0; padding-left: 20px;">
                        <li>Save the attached QR code image to your phone</li>
                        <li>Show it at the food counter when you arrive</li>
                        <li>The staff will scan it to confirm your food preference</li>
                        <li><strong>Note:</strong> Each QR code can only be used once</li>
                    </ol>
                </div>
                
                <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin-bottom: 25px;">
                    <h3 style="color: #856404; margin: 0 0 10px 0;">⚠️ Backup Option:</h3>
                    <p style="color: #856404; margin: 0; line-height: 1.6;">
                        If the QR code scanner doesn't work, you can manually provide your USN: <strong>{usn}</strong>
                    </p>
                </div>
                
                <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6;">
                    <p style="color: #6c757d; margin: 0; font-size: 14px;">
                        This is an automated email from the Food Token System.<br>
                        If you have any questions, please contact the college administration.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        return html_content
    
    def send_email_with_qr(self, to_email, student_name, class_name, usn, food_preference, qr_image_path):
        """Send email with QR code attachment"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.email_from_name} <{self.email_user}>"
            msg['To'] = to_email
            msg['Subject'] = f"{self.email_subject} - {student_name}"
            
            # Create HTML content
            html_content = self.create_email_content(student_name, class_name, usn, food_preference)
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Add QR code as attachment
            if os.path.exists(qr_image_path):
                with open(qr_image_path, 'rb') as f:
                    img_data = f.read()
                
                image = MIMEImage(img_data)
                image.add_header('Content-Disposition', f'attachment; filename="{student_name}_{usn}_QR_Code.jpg"')
                msg.attach(image)
            else:
                print(f"Warning: QR code file not found: {qr_image_path}")
                return False
            
            # Send email
            server = smtplib.SMTP(self.email_host, self.email_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            
            text = msg.as_string()
            server.sendmail(self.email_user, to_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Failed to send email to {to_email}: {str(e)}")
            return False

def send_qr_codes_to_all_students():
    """Send QR codes to all students in the database"""
    try:
        email_sender = EmailSender()
        
        # Connect to database
        conn = sqlite3.connect('database/food_tokens.db')
        cursor = conn.cursor()
        
        # Get all users
        cursor.execute('SELECT name, email, usn, class_name, food_preference FROM users')
        users = cursor.fetchall()
        conn.close()
        
        print(f"Starting to send emails to {len(users)} students...")
        
        sent_count = 0
        failed_count = 0
        
        for name, email, usn, class_name, food_preference in users:
            # Find corresponding QR code file
            qr_files = [
                f"qr_codes_jpeg/{name}_{class_name.replace(' ', '_')}_{usn[-8:]}.jpg",
                f"qr_codes_jpeg/{name}_{class_name.replace(' ', '_')}_*.jpg"
            ]
            
            # Find actual QR file
            qr_file_path = None
            for pattern in qr_files:
                if '*' in pattern:
                    # Use glob to find files with pattern
                    import glob
                    matches = glob.glob(pattern)
                    if matches:
                        qr_file_path = matches[0]
                        break
                else:
                    if os.path.exists(pattern):
                        qr_file_path = pattern
                        break
            
            # If still not found, search by name pattern
            if not qr_file_path:
                import glob
                pattern = f"qr_codes_jpeg/{name}_*.jpg"
                matches = glob.glob(pattern)
                if matches:
                    qr_file_path = matches[0]
            
            if qr_file_path and os.path.exists(qr_file_path):
                print(f"Sending email to {name} ({email})...")
                
                success = email_sender.send_email_with_qr(
                    email, name, class_name, usn, food_preference, qr_file_path
                )
                
                if success:
                    sent_count += 1
                    print(f"✅ Email sent successfully to {name}")
                else:
                    failed_count += 1
                    print(f"❌ Failed to send email to {name}")
                
                # Add delay to avoid overwhelming email server
                time.sleep(2)
            else:
                failed_count += 1
                print(f"❌ QR code file not found for {name}")
        
        print(f"\n📊 Email sending completed!")
        print(f"✅ Successfully sent: {sent_count}")
        print(f"❌ Failed: {failed_count}")
        print(f"📧 Total attempts: {len(users)}")
        
    except Exception as e:
        print(f"Error in email sending process: {str(e)}")

if __name__ == "__main__":
    # Check if .env file is properly configured
    load_dotenv()
    if not os.getenv('EMAIL_USER') or not os.getenv('EMAIL_PASSWORD'):
        print("❌ Please configure your email credentials in .env file")
        print("Set EMAIL_USER and EMAIL_PASSWORD variables")
        exit(1)
    
    print("🚀 Starting automated QR code email distribution...")
    send_qr_codes_to_all_students()
