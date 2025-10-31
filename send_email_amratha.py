import smtplib
import sqlite3
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

def send_qr_email_to_amratha():
    # Load environment variables
    load_dotenv()
    
    # Email configuration
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASS = os.getenv('EMAIL_PASSWORD')
    
    if not EMAIL_USER or not EMAIL_PASS:
        print('❌ Email credentials not found in .env file')
        print(f'EMAIL_USER: {EMAIL_USER}')
        print(f'EMAIL_PASSWORD: {"*" * len(EMAIL_PASS) if EMAIL_PASS else None}')
        return False
    
    # Connect to database and get Amratha's details
    conn = sqlite3.connect('database/food_tokens.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT name, email, usn, class_name, food_preference, token 
        FROM users 
        WHERE usn = ? OR name LIKE ?
    ''', ('4SF24IS085', '%S  Chinmay%'))
    
    student = cursor.fetchone()
    conn.close()
    
    if not student:
        print('❌ Amratha not found in database')
        return False
    
    name, email, usn, class_name, food_preference, token = student
    print(f'📧 Sending email to: {name} ({email})')
    
    # Find QR code file
    qr_filename = f'qr_codes_jpeg/Amratha_D_Kamath_{usn}.jpg'
    if not os.path.exists(qr_filename):
        print(f'❌ QR code file not found: {qr_filename}')
        return False
    
    # Create email
    msg = MIMEMultipart('related')
    msg['From'] = EMAIL_USER
    msg['To'] = email
    msg['Subject'] = 'Your Food Token QR Code - Sahyadri College Food Counter'
    
    # HTML email body
    html_body = f'''
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .qr-section {{ text-align: center; margin: 20px 0; }}
            .info-box {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin: 20px 0; }}
            .instructions {{ background: #e8f5e8; padding: 15px; border-radius: 8px; border-left: 4px solid #4CAF50; }}
            .footer {{ text-align: center; color: #666; font-size: 14px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class=container>
            <div class=header>
                <h1>🍽️ Food Token QR Code</h1>
                <p>Sahyadri College Food Counter System</p>
            </div>
            
            <div class=content>
                <h2>Dear {name},</h2>
                
                <p>Your food token QR code is ready! Please find your personalized QR code attached to this email.</p>
                
                <div class=info-box>
                    <h3>📋 Your Details:</h3>
                    <p><strong>👤 Name:</strong> {name}</p>
                    <p><strong>🎓 USN:</strong> {usn}</p>
                    <p><strong>🏫 Class:</strong> {class_name}</p>
                    <p><strong>🍽️ Food Preference:</strong> {food_preference.title()}</p>
                    <p><strong>📧 Email:</strong> {email}</p>
                </div>
                
                <div class=instructions>
                    <h3>📱 How to Use Your QR Code:</h3>
                    <ol>
                        <li>Download and save the QR code image from this email</li>
                        <li>Show the QR code on your phone screen at the food counter</li>
                        <li>The staff will scan your QR code</li>
                        <li>Collect your food based on your preference</li>
                    </ol>
                </div>
                
                <div class=info-box>
                    <h3>⚠️ Important Notes:</h3>
                    <ul>
                        <li>Each QR code can only be used ONCE</li>
                        <li>Make sure your phone screen is bright and clear</li>
                        <li>Have your college ID ready as backup</li>
                        <li>Report any issues to the food counter staff immediately</li>
                    </ul>
                </div>
                
                <p>If you have any questions or face any issues, please contact the college administration.</p>
                
                <p>Best regards,<br>
                <strong>Sahyadri College Food Counter Team</strong></p>
            </div>
            
            <div class=footer>
                <p>This is an automated message. Please do not reply to this email.</p>
                <p>© 2025 Sahyadri College of Engineering & Management</p>
            </div>
        </div>
    </body>
    </html>
    '''
    
    # Attach HTML body
    msg.attach(MIMEText(html_body, 'html'))
    
    # Attach QR code image
    try:
        with open(qr_filename, 'rb') as f:
            img_data = f.read()
            
        img = MIMEImage(img_data)
        img.add_header('Content-Disposition', f'attachment; filename="{name}_QR_Code.jpg"')
        msg.attach(img)
        
        print(f'✅ QR code attached: {qr_filename}')
        
    except Exception as e:
        print(f'❌ Error attaching QR code: {e}')
        return False
    
    # Send email
    try:
        print('📧 Connecting to SMTP server...')
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        
        print('📧 Sending email...')
        text = msg.as_string()
        server.sendmail(EMAIL_USER, email, text)
        server.quit()
        
        print(f'✅ Email sent successfully to {name} ({email})')
        return True
        
    except Exception as e:
        print(f'❌ Error sending email: {e}')
        return False

if __name__ == '__main__':
    print('🚀 SENDING EMAIL TO AMRATHA D KAMATH')
    print('=' * 50)
    
    success = send_qr_email_to_amratha()
    
    if success:
        print('\n🎉 EMAIL SENT SUCCESSFULLY!')
        print('✅ Amratha should receive her QR code shortly')
    else:
        print('\n❌ EMAIL SENDING FAILED!')
        print('Please check the logs above for errors')
