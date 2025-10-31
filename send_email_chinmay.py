import smtplib
import sqlite3
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

def send_qr_email():
    # Load environment variables
    load_dotenv()
    
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASS = os.getenv('EMAIL_PASSWORD')
    
    if not EMAIL_USER or not EMAIL_PASS:
        print('❌ Email credentials not found in .env file')
        return False
    
    # Fetch **Vignesh Das** details
    conn = sqlite3.connect('database/food_tokens.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT name, email, usn, class_name, food_preference, token 
        FROM users 
        WHERE usn = ? OR name LIKE ?
    ''', ('0418IS2025', '%Vignesh Das%'))
    
    student = cursor.fetchone()
    conn.close()
    
    if not student:
        print('❌ Student not found in database')
        return False
    
    name, email, usn, class_name, food_preference, token = student
    print(f'📧 Sending email to: {name} ({email})')
    
    # Correct QR file name for Vignesh
    qr_filename = f'qr_codes_jpeg/{name.replace(" ", "_")}_{usn}.jpg'
    if not os.path.exists(qr_filename):
        print(f'❌ QR code not found: {qr_filename}')
        return False
    
    # Create email body
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = email
    msg['Subject'] = 'Your Sahyadri Food Token QR Code'
    
    html_body = f'''
    <html>
    <body style="font-family: Arial;">
        <h2>🍽️ Your Food Token QR Code</h2>
        <p>Hello <strong>{name}</strong>,</p>
        <p>Your food token QR code is attached below.</p>
        <p><strong>USN:</strong> {usn}<br>
        <strong>Class:</strong> {class_name}<br>
        <strong>Preference:</strong> {food_preference.title()}</p>
        <p>Show this QR code at the food counter.</p>
        <p>Regards,<br><strong>Sahyadri College Food Token System</strong></p>
    </body>
    </html>
    '''
    
    msg.attach(MIMEText(html_body, 'html'))
    
    # Attach QR code
    with open(qr_filename, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-Disposition', f'attachment; filename="{name}_QR.jpg"')
        msg.attach(img)

    # Send email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, email, msg.as_string())
        server.quit()
        print(f'✅ Email sent successfully to {email}')
        return True
    except Exception as e:
        print(f'❌ Sending Failed: {e}')
        return False

if __name__ == '__main__':
    print('🚀 Sending Email...')
    send_qr_email()

