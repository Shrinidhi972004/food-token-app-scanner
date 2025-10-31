import smtplib, sqlite3, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv()
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASSWORD')

new_usns = [
    '4SF24IS008', '4SF23IS055', '4SF23CD404', '4SF22CD044', '4SF24IS081',
    '4SF22CD041', '4SF23IS002', '4SF22CD053', '4SF23IS014', '4SF22CD059'
]

conn = sqlite3.connect('database/food_tokens.db')
cursor = conn.cursor()

sent = []
failed = []

for usn in new_usns:
    cursor.execute('SELECT name, email, usn, class_name, food_preference FROM users WHERE usn = ?', (usn,))
    student = cursor.fetchone()
    
    if not student:
        failed.append((usn, 'not found in DB'))
        continue
        
    name, email, usn, class_name, food_preference = student
    safe_name = ''.join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip().replace(' ', '_')
    qr_filename = f'qr_codes_jpeg/{safe_name}_{usn}.jpg'
    
    if not os.path.exists(qr_filename):
        failed.append((name, f'QR file missing: {qr_filename}'))
        continue
    
    try:
        msg = MIMEMultipart('related')
        msg['From'] = EMAIL_USER
        msg['To'] = email
        msg['Subject'] = 'Your Food Token QR Code - Sahyadri College Food Counter'
        
        html_body = f'''
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
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
                        <h3>�� How to Use Your QR Code:</h3>
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
        
        msg.attach(MIMEText(html_body, 'html'))
        
        with open(qr_filename, 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-Disposition', f'attachment; filename={name}_QR_Code.jpg')
            msg.attach(img)
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, email, msg.as_string())
        server.quit()
        
        sent.append((name, email))
        print(f'✅ Sent to {name} ({email})')
        
    except Exception as e:
        failed.append((name, f'Email error: {str(e)}'))
        print(f'❌ Failed to send to {name}: {e}')

conn.close()

print(f'\n📊 SUMMARY:')
print(f'Emails sent: {len(sent)}')
print(f'Emails failed: {len(failed)}')

if failed:
    print('\nFailed deliveries:')
    for f in failed:
        print(f'  {f}')
