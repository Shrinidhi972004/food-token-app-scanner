#!/usr/bin/env python3
import csv
import qrcode
from PIL import Image, ImageDraw, ImageFont
import uuid
import os
import json
import sqlite3
from datetime import datetime
import time
from send_qr_emails import EmailSender

def create_qr_with_text(data, filename, student_name, food_preference, class_name):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    img_width = 600
    img_height = 700
    
    final_img = Image.new('RGB', (img_width, img_height), 'white')
    
    qr_img = qr_img.resize((400, 400))
    
    qr_x = (img_width - 400) // 2
    qr_y = 50
    final_img.paste(qr_img, (qr_x, qr_y))
    
    draw = ImageDraw.Draw(final_img)
    
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    text_y = 470
    
    draw.text((img_width//2, text_y), student_name, font=font_large, fill='black', anchor='mm')
    text_y += 40
    
    draw.text((img_width//2, text_y), f"Class: {class_name}", font=font_medium, fill='black', anchor='mm')
    text_y += 30
    
    pref_color = 'green' if 'veg' in food_preference.lower() and 'non' not in food_preference.lower() else 'red'
    draw.text((img_width//2, text_y), f"Food: {food_preference}", font=font_medium, fill=pref_color, anchor='mm')
    text_y += 40
    
    draw.text((img_width//2, text_y), "🍽️ FOOD TOKEN 🍽️", font=font_medium, fill='blue', anchor='mm')
    text_y += 30
    
    draw.text((img_width//2, text_y), "Scan at Food Counter", font=font_small, fill='gray', anchor='mm')
    
    final_img.save(filename, 'JPEG', quality=95)

def create_database():
    os.makedirs('database', exist_ok=True)
    conn = sqlite3.connect('database/food_tokens.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            usn TEXT UNIQUE NOT NULL,
            class_name TEXT NOT NULL,
            food_preference TEXT NOT NULL,
            token TEXT UNIQUE NOT NULL,
            qr_code_path TEXT NOT NULL,
            is_scanned BOOLEAN DEFAULT FALSE,
            scanned_at DATETIME NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    return conn

def insert_user_to_db(conn, user_data):
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO users (name, email, usn, class_name, food_preference, token, qr_code_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_data['name'],
            user_data['email'],
            user_data['usn'],
            user_data['class_name'],
            user_data['food_preference'],
            user_data['token'],
            user_data['qr_code_path']
        ))
        
        user_id = cursor.lastrowid
        conn.commit()
        return user_id
        
    except sqlite3.IntegrityError as e:
        if 'UNIQUE constraint failed: users.email' in str(e):
            print(f"⚠️  Duplicate email found: {user_data['email']} - Skipping")
        elif 'UNIQUE constraint failed: users.usn' in str(e):
            print(f"⚠️  Duplicate USN found: {user_data['usn']} - Skipping")
        else:
            print(f"⚠️  Database error for {user_data['name']}: {e}")
        return None

def send_email_after_generation(email_sender, user_data, qr_file_path):
    """Send email immediately after QR code generation"""
    if email_sender and os.path.exists(qr_file_path):
        print(f"📧 Sending email to {user_data['name']} ({user_data['email']})...")
        
        success = email_sender.send_email_with_qr(
            user_data['email'],
            user_data['name'],
            user_data['class_name'],
            user_data['usn'],
            user_data['food_preference'],
            qr_file_path
        )
        
        if success:
            print(f"✅ Email sent successfully to {user_data['name']}")
            return True
        else:
            print(f"❌ Failed to send email to {user_data['name']}")
            return False
    return False

def main():
    csv_file = input("Enter CSV file path (or press Enter for 'food_pref_cleaned.csv'): ").strip()
    if not csv_file:
        csv_file = 'food_pref_cleaned.csv'
    
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        return
    
    # Ask if user wants to send emails automatically
    send_emails = input("Do you want to send QR codes via email automatically? (y/n): ").strip().lower()
    
    email_sender = None
    if send_emails == 'y':
        try:
            email_sender = EmailSender()
            print("✅ Email system initialized successfully!")
        except Exception as e:
            print(f"❌ Email system initialization failed: {e}")
            print("📧 QR codes will be generated without email sending")
            email_sender = None
    
    output_dir = 'qr_codes_jpeg'
    os.makedirs(output_dir, exist_ok=True)
    
    conn = create_database()
    
    tokens_data = []
    emails_sent = 0
    emails_failed = 0
    
    print(f"🚀 Starting QR code generation from {csv_file}...")
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        total_rows = len(rows)
        
        print(f"📊 Found {total_rows} records in CSV")
        
        for i, row in enumerate(rows, 1):
            name = row['name'].strip()
            email = row['email'].strip()
            usn = row['usn'].strip()
            class_name = row['class_name'].strip()
            food_pref = row['food_preference'].strip()
            
            if not all([name, email, usn, class_name, food_pref]):
                print(f"⚠️  Incomplete data for row {i}: {row}")
                continue
            
            token = str(uuid.uuid4())
            
            qr_data = {
                'id': token,
                'name': name,
                'email': email,
                'usn': usn,
                'class': class_name,
                'food_preference': food_pref,
                'type': 'food_token',
                'generated_at': datetime.now().isoformat()
            }
            
            safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_class = class_name.replace(' ', '_')
            
            filename = f"{safe_name}_{safe_class}_{token[:8]}.jpg"
            qr_code_path = os.path.join(output_dir, filename)
            
            create_qr_with_text(json.dumps(qr_data), qr_code_path, name, food_pref, class_name)
            
            user_data = {
                'name': name,
                'email': email,
                'class_name': class_name,
                'food_preference': food_pref,
                'token': token,
                'qr_code_path': qr_code_path,
                'usn': usn
            }
            
            user_id = insert_user_to_db(conn, user_data)
            
            if user_id:
                tokens_data.append({
                    'id': user_id,
                    'name': name,
                    'email': email,
                    'class': class_name,
                    'food_preference': food_pref,
                    'token': token,
                    'filename': filename,
                    'qr_code_path': qr_code_path,
                    'usn': usn
                })
                
                # Send email immediately after QR generation
                if email_sender:
                    email_success = send_email_after_generation(email_sender, user_data, qr_code_path)
                    if email_success:
                        emails_sent += 1
                    else:
                        emails_failed += 1
                    
                    # Add small delay to avoid overwhelming email server
                    time.sleep(1)
            
            # Progress update
            if i % 25 == 0 or i == total_rows:
                print(f"⏳ Progress: {i}/{total_rows} QR codes generated...")
                if email_sender:
                    print(f"   📧 Emails: {emails_sent} sent, {emails_failed} failed")
    
    # Save tokens list
    with open(f'{output_dir}/tokens_list.json', 'w') as f:
        json.dump(tokens_data, f, indent=2)
    
    conn.close()
    
    # Final statistics
    unique_students = len(tokens_data)
    total_rows = len(rows)
    duplicates_skipped = total_rows - unique_students
    
    print(f"\n🎉 QR CODE GENERATION COMPLETED!")
    print(f"✅ Successfully generated: {unique_students} QR codes")
    if duplicates_skipped > 0:
        print(f"⚠️  Skipped duplicates: {duplicates_skipped}")
    
    if email_sender:
        print(f"\n📧 EMAIL SENDING SUMMARY:")
        print(f"✅ Emails sent successfully: {emails_sent}")
        print(f"❌ Emails failed: {emails_failed}")
        print(f"📊 Email success rate: {(emails_sent/(emails_sent+emails_failed)*100):.1f}%" if (emails_sent+emails_failed) > 0 else "No emails attempted")
    
    print(f"\n📁 Files saved in: {output_dir}/")
    print(f"📋 Token list: {output_dir}/tokens_list.json")
    print(f"💾 Database: database/food_tokens.db")
    
    # Food preference breakdown
    veg_count = sum(1 for token in tokens_data if 'veg' in token['food_preference'].lower() and 'non' not in token['food_preference'].lower())
    non_veg_count = sum(1 for token in tokens_data if 'non' in token['food_preference'].lower())
    
    print(f"\n📊 FOOD PREFERENCE BREAKDOWN:")
    print(f"🥗 Vegetarian: {veg_count}")
    print(f"🍖 Non-Vegetarian: {non_veg_count}")
    print(f"📈 Total students: {unique_students}")
    
    print(f"\n🚀 NEXT STEPS:")
    print(f"   1. Start server: npm start")
    print(f"   2. Scanner interface: http://localhost:3000/scanner")
    print(f"   3. Admin dashboard: http://localhost:3000/admin")
    
    if email_sender and emails_sent > 0:
        print(f"   4. ✅ Students have been notified via email!")
    elif not email_sender:
        print(f"   4. 📧 Run 'python send_qr_emails.py' to send emails manually")

if __name__ == "__main__":
    main()
